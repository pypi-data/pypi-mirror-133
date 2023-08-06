from ..lib import *
from .patch import TPatch


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
