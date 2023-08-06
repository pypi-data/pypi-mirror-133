from ..lib import *
from torch.utils.data import random_split


class ImageOnlyLoader:
    def __init__(self,
                 glob_path: str,
                 transform: Callable,
                 shuffle: bool = True) -> None:
        """一个仅输出图像的简易加载器，所要加载的图像依赖`glob`库进行索引

        Args:
            glob_path (str): glob匹配字符
            transform (Callable): 对转为Tensor格式后的原图片的预处理函数
            shuffle (bool, optional): 是否打乱加载顺序. Defaults to True.
        """
        self.img_names = sorted(glob(glob_path))
        self.length = len(self.img_names)
        self.shuffle = shuffle
        if self.shuffle:
            random.shuffle(self.img_names)
        self.pil2tensor = tv.transforms.ToTensor()
        self.transform = transform

    def __getitem__(self, key: int) -> torch.Tensor:
        img = self.transform(self.pil2tensor(Image.open(
            self.img_names[key]))).unsqueeze(dim=0)
        return img

    def __len__(self) -> int:
        return self.length


def load_imagenet_preprocess() -> tv.transforms.Normalize:
    """加载imagenet的归一化函数
    """
    return tv.transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    )


def load_imagenet_val(dataset: str,
                      batch_size: int = 1,
                      size: int = 50000,
                      shuffle: bool = True,
                      inc: bool = False) -> DataLoader:
    """加载ImageNet验证集

    Args:
        dataset (str): 存放数据集的位置，该位置下应该存在1000个文件夹，序号从0~999，存放各类图片
        size (int, optional): 所要加载的数据集大小，最大不超过50000，采用随机切分方法. Defaults to 50000.
        shuffle (bool, optional): 是否打乱加载顺序. Defaults to True.
        inc (bool, optional): 是否是Inception格式（299*299），默认是224*224. Defaults to False.
    """
    imagenet = tv.datasets.ImageFolder(dataset,
                                       transform=tv.transforms.Compose([
                                           tv.transforms.Resize(299),
                                           tv.transforms.CenterCrop(
                                               (299, 299)),
                                           tv.transforms.ToTensor(),
                                       ]) if inc else tv.transforms.Compose([
                                           tv.transforms.Resize(256),
                                           tv.transforms.CenterCrop(
                                               (224, 224)),
                                           tv.transforms.ToTensor(),
                                       ]))
    if size != 50000:
        partial = [size, 50000 - size]
        imagenet, _ = random_split(imagenet, partial)
    return DataLoader(
        imagenet,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=5 if batch_size >= 10 else 0,
    )


def read_img(path:str, device:str, crop_size:int=None)->torch.Tensor:
    """加载单张图像

    Args:
        path (str): 图像所存储的路径
        crop_size (int, optional): 中心裁剪尺寸，默认是原图
    """    
    if crop_size is None:
        tr = tv.transforms.ToTensor()
    else:
        tr = tv.transforms.Compose([
            tv.transforms.Resize(crop_size),
            tv.transforms.CenterCrop((crop_size, crop_size)),
            tv.transforms.ToTensor(),
        ])
    return tr(Image.open(path)).unsqueeze(0).to(device)
