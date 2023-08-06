from ..lib import *


class Pixel2Pixel(Dataset):
    def __init__(self, sim_img: Union[str, np.ndarray],
                 phy_img: Union[str, np.ndarray]) -> None:
        super().__init__()
        if isinstance(sim_img, str):
            sim_img = self.default_load(sim_img)
        if isinstance(phy_img, str):
            phy_img = self.default_load(phy_img)
        self.src = sim_img.reshape(-1, 3).astype(np.float32) / 255 - 0.5
        self.src = torch.from_numpy(self.src)
        self.dst = phy_img.reshape(-1, 3).astype(np.float32) / 255 - 0.5
        self.dst = torch.from_numpy(self.dst)
        self.length = self.src.shape[0]

    def default_load(self, path: str) -> np.ndarray:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def __getitem__(self, index):
        return self.src[index], self.dst[index]

    def __len__(self):
        return self.length


class ColorModel(nn.Module):
    def __init__(self, n_neuron: int) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, n_neuron),
            nn.ReLU(),
            nn.Linear(n_neuron, n_neuron),
            nn.ReLU(),
            nn.Linear(n_neuron, 3),
        )

    def forward(self, x: Union[np.ndarray, torch.Tensor]):
        if self.training:
            x = self.model(x)
        elif isinstance(x, torch.Tensor):
            x = x.permute(0, 2, 3, 1).view(-1, 3)
            x = self.model(x - 0.5)
            x = x + 0.5
        elif isinstance(x, np.ndarray):
            h, w = x.shape[:2]
            x = x.reshape(-1, 3).astype(np.float32)
            x = x / 255 - 0.5
            x = torch.from_numpy(x)
            x = self.model(x)
            x = ((x + 0.5) * 255).cpu().detach().numpy()
            x = np.clip(x, 0, 255).astype(np.uint8)
            x = x.reshape(h, w, 3)
        else:
            raise NotImplementedError
        return x

    def pickle_dump(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.model.state_dict(), f, protocol=2)

    def pickle_load(self, path: str):
        with open(path, "rb") as f:
            params = pickle.load(f)
        self.model.load_state_dict(params)


def _train(model, metric, opt, sch, loader, epoch, device):
    for i in range(epoch):
        log_loss = 0
        for src, dst in loader:
            src, dst = src.to(device), dst.to(device)
            pred = model(src)
            loss = metric(pred, dst)
            opt.zero_grad()
            loss.backward()
            opt.step()
            log_loss += loss.detach()
        sch.step()
        print(i, log_loss)


def train_color_model(sim_img: Union[str, np.ndarray],
                      phy_img: Union[str, np.ndarray],
                      device: str = "cpu",
                      n_neuron: int = 16) -> ColorModel:
    model = ColorModel(n_neuron)
    model.to(device).train()
    loader = DataLoader(Pixel2Pixel(sim_img, phy_img),
                        batch_size=16,
                        shuffle=True)
    metric = nn.MSELoss()
    opt = optim.SGD(model.parameters(), 1, 0.9)
    sch = optim.lr_scheduler.StepLR(opt, 30, 0.1)
    epoch = 100
    _train(model, metric, opt, sch, loader, epoch, device)
    model.eval()
    return model
