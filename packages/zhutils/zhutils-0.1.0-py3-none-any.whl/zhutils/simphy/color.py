from ..lib import *
from string import ascii_uppercase


def smooth_color():
    patch = np.zeros((64, 64, 3), dtype=np.uint8)
    for r in range(16):
        for g in range(16):
            for b in range(16):
                starth = r // 4
                startl = r % 4
                if starth % 2 == 0:
                    if startl % 2 == 0:
                        c = (r * 17, g * 17, b * 17)
                    else:
                        c = (r * 17, g * 17, (15 - b) * 17)
                else:
                    if startl % 2 == 0:
                        c = (r * 17, (15 - g) * 17, b * 17)
                    else:
                        c = (r * 17, (15 - g) * 17, (15 - b) * 17)
                patch[starth * 16 + g, startl * 16 + b] = c
    return patch


def _ascii_mask():
    mask = np.zeros((64, 64, 3), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_COMPLEX
    fontsize = 0.5
    white = (255, 255, 255)
    bold = 2
    text = ascii_uppercase[:5]
    mask = cv2.putText(mask, text, (4, 16), font, fontsize, white, bold)
    text = ascii_uppercase[5:10]
    mask = cv2.putText(mask, text, (4, 30), font, fontsize, white, bold)
    text = ascii_uppercase[10:15]
    mask = cv2.putText(mask, text, (4, 44), font, fontsize, white, bold)
    text = ascii_uppercase[15:20]
    mask = cv2.putText(mask, text, (4, 58), font, fontsize, white, bold)
    return mask


def _test_colors():
    colors = []
    for i in range(0, 256, 17):
        for j in range(0, 256, 17):
            for k in range(0, 256, 17):
                colors.append((i, j, k))
    return colors


def ascii_color():
    mask = _ascii_mask()
    patch1 = np.zeros_like(mask)
    patch2 = np.ones_like(mask) * 255
    sep = np.ones((64, 8, 3), dtype=np.uint8) * 255
    mask = np.mean(mask, axis=2)
    white = []
    black = []
    for i in range(64):
        for j in range(64):
            if mask[i, j] == 0:
                black.append((i, j))
            else:
                white.append((i, j))
    n = len(white)
    colors = _test_colors()
    colors.sort(key=lambda x: sum(x), reverse=True)
    whites = colors[:n]
    blacks = colors[n:]
    random.seed(0)
    random.shuffle(whites)
    random.shuffle(blacks)
    for (i, j), c in zip(white, whites):
        patch1[i, j] = c
    for (i, j), c in zip(black, blacks):
        patch2[i, j] = c
    patch = np.concatenate([patch1, sep, patch2], axis=1)
    return patch


def upscale(img, x: int):
    h, w, c = img.shape
    img_u = np.zeros((h * x, w * x, c), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            img_u[i * x:(i + 1) * x, j * x:(j + 1) * x] = img[i:i + 1, j:j + 1]
    return img_u

