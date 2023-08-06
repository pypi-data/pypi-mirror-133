from ..lib import *
from .robust import EoT


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
