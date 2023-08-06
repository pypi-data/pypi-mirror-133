from ..lib import *
from .io import load_imagenet_preprocess


class MIFGSM(nn.Module):
    def __init__(self, m: float, lr: float):
        """MI-FGSM的简单实现

        Args:
            m (float): 动量项，取值范围为[0, 1]
            lr (float): 每次更新步长
        """
        super().__init__()
        self.m = m
        self.lr = lr
        self.h = 0

    @torch.no_grad()
    def forward(self, t: torch.Tensor) -> None:
        """对已经求得梯度的张量进行原地更新

        Args:
            t (torch.Tensor): 待更新的张量
        """
        l1 = t.grad.abs().mean()
        if l1 == 0:
            l1 += 1
        self.h = self.h * self.m + t.grad / l1
        t.data -= self.lr * self.h.sign()
        t.grad.zero_()


class TPatch:
    def __init__(self,
                 h: int,
                 w: int,
                 device: str = "cpu",
                 lr: float = 1 / 255,
                 momentum: float = 0.9,
                 eot: bool = False,
                 eot_angle: float = math.pi / 9,
                 eot_scale: float = 0.8,
                 p: float = 0.5):
        """虽然叫TPatch，其实是AdvPatch的实现，默认使用MI-FGSM优化

        Args:
            h (int): patch的竖边
            w (int): patch的横边
            lr (float, optional): 更新步长. Defaults to 1/255.
            momentum (float, optional): 动量项. Defaults to 0.9.
            eot (bool, optional): 是否进行EoT变换. Defaults to False.
            eot_angle (float, optional): EoT的旋转角度，这里是范围的一半. Defaults to math.pi/9.
            eot_scale (float, optional): EoT的缩放尺寸. Defaults to 0.8.
            p (float, optional): 以一定概率随机进行EoT. Defaults to 0.5.
        """
        if eot:
            assert h == w, "只实现了正方形的EoT"
            s = h
            pre_scale = 1 / (math.cos(eot_angle) + math.sin(eot_angle))
            h = w = math.ceil(s * pre_scale)
            pre_scale = h / s
            self.robust = EoT(angle=eot_angle,
                              scale=eot_scale,
                              pre_scale=pre_scale,
                              p=p)
        self.eot = eot
        self.w = int(w)
        self.h = int(h)
        self.shape = [1, 3, self.h, self.w]
        self.device = device
        self.data = torch.rand(self.shape, device=device, requires_grad=True)
        self.opt = MIFGSM(m=momentum, lr=lr)
        self.pil2tensor = tv.transforms.ToTensor()

    def apply(self,
              img: torch.Tensor,
              pos: Tuple[int, int],
              test_mode: bool = False,
              set_rotate: float = None,
              set_resize: float = None,
              transform: Callable = None) -> torch.Tensor:
        """把patch放到img上

        Args:
            img (torch.Tensor): 背景图像
            pos (Tuple[int, int]): 用于放置的左上角位置坐标，注意这里不是真实坐标
            test_mode (bool, optional): 测试模式开关，用于固定旋转/尺寸进行测试. Defaults to False.
            set_rotate (float, optional): 固定旋转. Defaults to None.
            set_resize (float, optional): 固定尺寸. Defaults to None.
            transform (Callable, optional): 用于特殊的数值变换. Defaults to None.
        """
        assert len(pos) == 2, "pos should be (x, y)"
        if self.eot:
            if test_mode:
                switch, padding, _ = self.robust(self,
                                                 pos,
                                                 img.shape[-2:],
                                                 do_random_rotate=False,
                                                 do_random_color=False,
                                                 do_random_resize=False,
                                                 set_rotate=set_rotate,
                                                 set_resize=set_resize)
            else:
                switch, padding, scale_ratio = self.robust(
                    self, pos, img.shape[-2:])
                if transform:
                    padding = transform(padding)
                return torch.where(switch, img, padding), scale_ratio
        else:
            switch, padding = self.mask(img.shape, pos)
        if transform:
            padding = transform(padding)
        return torch.where(switch, img, padding)

    def update(self, loss: torch.Tensor) -> None:
        """输入loss，更新patch

        Args:
            loss (torch.Tensor): 可以反传梯度的张量
        """
        loss.backward()
        self.opt(self.data)
        self.data.data.clamp_(0, 1)

    def mask(self, shape: torch.Size,
             pos: Tuple[int, int]) -> Tuple[torch.Tensor, torch.Tensor]:
        """产生一个简单的非EoT的mask

        Args:
            shape (torch.Size): 背景图像尺寸
            pos (Tuple[int, int]): 放置的左上角坐标

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: 一个mask和做完padding的patch
        """
        mask = torch.ones(shape, dtype=torch.long, device=self.device)
        mask[..., pos[0]:pos[0] + self.h, pos[1]:pos[1] + self.w] = 0
        padding = torch.zeros(shape, dtype=torch.float, device=self.device)
        padding[..., pos[0]:pos[0] + self.h,
                pos[1]:pos[1] + self.w] = self.data
        return mask == 1, padding

    def random_pos(self, shape: torch.Size) -> Tuple[int, int]:
        """用于获取一个合法的随机放置位置

        Args:
            shape (torch.Size): 背景图像尺寸

        Returns:
            Tuple[int, int]: 位置坐标，(h, w)格式
        """
        h = random.randint(0, shape[-2] - self.h)
        w = random.randint(0, shape[-1] - self.w)
        return h, w

    def save(self, path: str):
        """保存patch
        """
        tv.utils.save_image(self.data, path)

    def load(self, path: str):
        """加载patch
        """
        self.data = self.pil2tensor(Image.open(path))
        self.data = self.data.unsqueeze(0).to(self.device)
        self.shape = list(self.data.shape)
        _, _, self.h, self.w = self.shape


class EoT(nn.Module):
    def __init__(self, angle=math.pi / 9, scale=0.8, pre_scale=0.8, p=0.5):
        """EoT模块

        Args:
            angle ([type], optional): 旋转角度，这里是范围的一半. Defaults to math.pi/9.
            scale (float, optional): 缩放尺寸范围. Defaults to 0.8.
            pre_scale (float, optional): 为了避免旋转过界的预缩放尺寸，可以通过公式计算: 1/(sin(a)+cos(a)). Defaults to 0.8.
            p (float, optional): 以一定概率随机进行EoT. Defaults to 0.5.
        """
        super(EoT, self).__init__()
        self.angle = angle
        self.scale = scale
        self.pre_scale = pre_scale
        self.p = p
        self.color = tv.transforms.ColorJitter(brightness=0.2,
                                               contrast=0.2,
                                               saturation=0.1,
                                               hue=0.1)

    def forward(self,
                patch: TPatch,
                pos: Tuple[int, int],
                img_shape: Tuple[int, int],
                do_random_rotate=True,
                do_random_color=True,
                do_random_resize=True,
                set_rotate=None,
                set_resize=None) -> Tuple[torch.Tensor, torch.Tensor, float]:
        """获取旋转的mask

        Args:
            pos (Tuple[int, int]): 放置的左上角坐标
            img_shape (Tuple[int, int]): 背景图像尺寸
            do_random_rotate (bool, optional): 随机旋转开关. Defaults to True.
            do_random_color (bool, optional): 随机色差开关. Defaults to True.
            do_random_resize (bool, optional): 随机尺寸开关. Defaults to True.
            set_rotate ([type], optional): 设定固定旋转. Defaults to None.
            set_resize ([type], optional): 设定固定尺寸. Defaults to None.

        Returns:
            Tuple[torch.Tensor, torch.Tensor, float]: 一个mask和做完padding的patch，以及随机resize的数值，常用于detector的框位置的确定
        """
        if torch.rand(1) > self.p:
            do_random_rotate = False
            do_random_color = False
            do_random_resize = False

        if do_random_color:
            img = self.color(patch.data)
        else:
            img = patch.data

        if do_random_rotate:
            angle = torch.FloatTensor(1).uniform_(-self.angle, self.angle)
        elif set_rotate is None:
            angle = torch.zeros(1)
        else:
            angle = torch.full(1, set_rotate)

        if do_random_resize:
            scale_ratio = torch.FloatTensor(1).uniform_(self.scale, 1)
        elif set_resize is None:
            scale_ratio = torch.ones(1)
        else:
            scale_ratio = torch.full(1, set_resize)

        # ! 这里实现并不完美，现在是先平均降采样，再双线性插值，目的是避免出现仅关注几个点的问题
        scale = scale_ratio * self.pre_scale
        t = -torch.ceil(torch.log2(scale))
        t = 1 << int(t.item())
        if t > 1:
            size = (patch.h // t, patch.w // t)
            img = F.interpolate(img, size=size, mode="area")
            scale *= t

        angle = angle.to(patch.device)
        scale = scale.to(patch.device)
        sin = torch.sin(angle)
        cos = torch.cos(angle)

        theta = torch.zeros((1, 2, 3), device=patch.device)
        theta[:, 0, 0] = cos / scale
        theta[:, 0, 1] = sin / scale
        theta[:, 0, 2] = 0
        theta[:, 1, 0] = -sin / scale
        theta[:, 1, 1] = cos / scale
        theta[:, 1, 2] = 0

        size = torch.Size((1, 3, patch.h // t, patch.w // t))
        grid = F.affine_grid(theta, size, align_corners=False)
        output = F.grid_sample(img, grid, align_corners=False)

        # * 利用grid_sample的zero填充来实现对应mask的生成
        rotate_mask = torch.ones(size, device=patch.device)
        mask = F.grid_sample(rotate_mask, grid, align_corners=False)

        tw1 = (patch.w - patch.w // t) // 2
        tw2 = patch.w - patch.w // t - tw1
        th1 = (patch.h - patch.h // t) // 2
        th2 = patch.h - patch.h // t - th1

        pad = nn.ZeroPad2d(padding=(
            pos[1] + tw1,
            img_shape[1] - patch.w - pos[1] + tw2,
            pos[0] + th1,
            img_shape[0] - patch.h - pos[0] + th2,
        ))
        mask = pad(mask)
        padding = pad(output)

        return mask == 0, padding, scale_ratio.item()


class TVLoss(nn.Module):
    def __init__(self) -> None:
        """Total Variation，通常用于衡量图像色彩连续程度
        """
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """直接当函数使用

        Args:
            x (torch.Tensor): 输入图像，支持3或4维格式

        Returns:
            torch.Tensor: TV loss
        """
        lr = torch.abs(x[..., :, 1:] - x[..., :, :-1]).mean()
        tb = torch.abs(x[..., 1:, :] - x[..., :-1, :]).mean()
        return lr + tb


class ContentLoss(nn.Module):
    def __init__(self,
                 extractor: nn.Module,
                 ref_fp: str,
                 device: str,
                 extract_layer=20) -> None:
        """计算内容损失，内容损失指神经网络对两张图像所提取特征间距离

        Args:
            extractor (nn.Module): 用于提取的训练好的卷积神经网络，例如vgg网络的backbone
            ref_fp (str): 参考图像的路径
            extract_layer (int, optional): 所参照的第几层特征. Defaults to 20.
        """
        super().__init__()
        self.extractor = extractor
        self.content_hook = extract_layer
        self.preprocess = load_imagenet_preprocess()
        self.resize = tv.transforms.Compose([
            tv.transforms.Resize([224, 224], interpolation=Image.BICUBIC),
            tv.transforms.ToTensor(),
        ])
        self.ref = self.resize(Image.open(ref_fp))[:3]
        self.ref = self.ref.unsqueeze(0).to(device)
        self.ref = self.get_content_layer(self.ref).detach()
        self.upsample = nn.Upsample(size=(224, 224), mode="bilinear")

    def get_content_layer(self, x: torch.Tensor) -> torch.Tensor:
        """提取第几层的特征结果

        Args:
            x (torch.Tensor): 输入图像

        Returns:
            torch.Tensor: 所要的特征向量
        """
        x = self.preprocess(x)
        for i, m in enumerate(self.extractor.children()):
            x = m(x)
            if i == self.content_hook:
                break
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """计算内容损失

        Args:
            x (torch.Tensor): 与参考图像对比的图像

        Returns:
            torch.Tensor: 内容损失
        """
        x = self.upsample(x)
        x = self.get_content_layer(x)
        loss = F.mse_loss(x, self.ref)
        return loss
