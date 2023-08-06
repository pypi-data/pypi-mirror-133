from ..lib import *


def _gamma_correction(imgs: torch.Tensor, gamma: float) -> torch.Tensor:
    """模拟运动模糊过程中图像的gamma校正影响

    Args:
        imgs (torch.Tensor): 需要有多张不同平移的图像作为输入
        gamma (float): gamma校正系数，通常取2.2

    Returns:
        torch.Tensor: 考虑gamma校正后生成的模糊图像
    """
    n = imgs.shape[0]
    out = 0
    for img in imgs:
        # 从RGB到光
        out += (1e-6 + img)**gamma
    # 从光到RGB
    out = (1e-6 + out / n)**(1 / gamma)
    return out


def _sine_grid(div: int, device: str) -> torch.Tensor:
    """正弦运动采样格点

    Args:
        div (int): 总共格点数

    Returns:
        torch.Tensor: 表征半个正弦运动过程的格点
    """
    # 此处假设是从两峰之间的半周期运动
    grid = torch.linspace(-0.5 * math.pi, 0.5 * math.pi, div, device=device)
    grid = (torch.sin(grid) + 1) / 2
    return grid


def _stn_blur_linear(img: torch.Tensor, div: int, x: float, y: float,
                     blur_grid: torch.Tensor, mean_func: Callable,
                     device: str) -> torch.Tensor:
    """pytorch基于STN实现线性模糊的方法

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        div (int): 使用多少张图像叠加生成模糊效果
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        blur_grid (torch.Tensor): 不同运动方式的采样格点，线性或正弦
        mean_func (Callable): 不同的合成方式，平均或考虑gamma校正
    """
    ones = torch.ones_like(blur_grid, device=device)
    zeros = torch.zeros_like(blur_grid, device=device)
    x = x * blur_grid
    y = y * blur_grid
    affine_tensor = torch.stack([
        torch.stack([ones, zeros, x]),
        torch.stack([zeros, ones, y]),
    ]).permute(2, 0, 1)
    grid = F.affine_grid(affine_tensor, [div, *img.shape[1:]],
                         align_corners=False)
    imgs = img.unsqueeze(dim=1).expand(-1, div, -1, -1, -1)
    res = []
    for i in range(img.shape[0]):
        samples = F.grid_sample(imgs[i],
                                grid,
                                padding_mode="border",
                                align_corners=False)
        blur_img = mean_func(samples)
        res.append(blur_img)
    res = torch.cat(res, dim=0)
    return res


def stn_blur_2d(img: torch.Tensor, x: float, y: float, div: int,
                device: str) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
    """
    blur_grid = torch.linspace(0, 1, div, device=device)
    mean_func = lambda x: torch.mean(x, dim=0, keepdim=True)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_gamma(img: torch.Tensor,
                      x: float,
                      y: float,
                      div: int,
                      device: str,
                      gamma: float = 2.2) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了gamma校正

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
        gamma (float, optional): gamma校正系数，通常取2.2
    """
    blur_grid = torch.linspace(0, 1, div, device=device)
    mean_func = lambda x: _gamma_correction(x, gamma).unsqueeze(0)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_sin(img: torch.Tensor, x: float, y: float, div: int,
                    device: str) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了半周期正弦运动

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
    """
    blur_grid = _sine_grid(div, device)
    mean_func = lambda x: torch.mean(x, dim=0, keepdim=True)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_gamma_sin(img: torch.Tensor,
                          x: float,
                          y: float,
                          div: int,
                          device: str,
                          gamma: float = 2.2) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了半周期正弦运动和gamma校正

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
        gamma (float, optional): gamma校正系数，通常取2.2
    """
    blur_grid = _sine_grid(div, device)
    mean_func = lambda x: _gamma_correction(x, gamma).unsqueeze(0)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res
