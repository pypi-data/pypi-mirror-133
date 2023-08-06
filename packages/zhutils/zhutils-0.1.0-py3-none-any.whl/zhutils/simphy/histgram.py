from ..lib import *


def colormap2D(img, ax):
    values = img.flatten().astype(np.float32)
    df = pd.DataFrame({"values": values})
    sns.histplot(data=df, x="values", bins=50, ax=ax)


def colormap3D(img, ax):
    img = img.reshape(-1, 3).astype(np.float32)
    l = img.shape[0]
    values = np.concatenate([img[:, 0], img[:, 2], img[:, 1]])
    colors = ["Blue"] * l + ["Red"] * l + ["Green"] * l
    df = pd.DataFrame({"values": values, "colors": colors})
    sns.histplot(data=df, x="values", hue="colors", bins=50, ax=ax)


def compare_colors(img1, img2, save_path):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colormap3D(img1, axes[0])
    colormap3D(img2, axes[1])
    fig.savefig(save_path)
    plt.close(fig)


def show_diff(difimg, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(21, 5))
    titles = ["Blue", "Green", "Red"]
    for i in range(3):
        colormap2D(difimg[..., i], axes[i])
        axes[i].set_title(titles[i])
    fig.savefig(save_path)
    plt.close(fig)


def heatmap(img, ax):
    sns.heatmap(img,
                ax=ax,
                cmap="YlGnBu",
                center=0,
                xticklabels=8,
                yticklabels=8,
                square=True)


def show_diff_heatmap(difimg, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    titles = ["Blue", "Green", "Red"]
    for i in range(3):
        heatmap(difimg[..., i], axes[i])
        axes[i].set_title(titles[i])
    fig.savefig(save_path)
    plt.close(fig)


def cut_tail(x: np.ndarray, percentage: float) -> np.ndarray:
    x = x.reshape(-1, 3)
    n = x.shape[0]
    l = [(i, x[i]) for i in range(n)]
    remove_set = set()
    for i in range(3):
        l.sort(key=lambda x: x[1][i])
        for j in range(int(math.ceil(n * percentage))):
            remove_set.add(l[j][0])
        for j in range(int(math.floor(n * (1 - percentage))), n):
            remove_set.add(l[j][0])
    y = []
    for i in range(n):
        if i not in remove_set:
            y.append(x[i])
    y = np.array(y)
    return y


def show_all_channels(x: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(21, 5))
    for i in range(3):
        axes[i].imshow(x[..., i])


