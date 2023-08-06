from ..lib import *
from .io import load_imagenet_preprocess


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
