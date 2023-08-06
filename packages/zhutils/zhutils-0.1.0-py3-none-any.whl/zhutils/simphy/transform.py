from ..lib import *


class AdaptiveCropper:
    def __init__(self, img, corner, save_path) -> None:
        self.img = img
        self.save_path = save_path
        self.winname = "adaptive crop"
        self.dsize = (512, 512)
        dst = [[0, 0], [511, 0], [511, 511], [0, 511]]
        self.dst = np.array(dst, dtype=np.float32)
        self.src = np.array(corner, dtype=np.float32)
        self.bias = np.zeros((1, 2), dtype=np.float32)
        self.crop()

    def crop(self):
        while True:
            self.mat = cv2.getPerspectiveTransform(self.src + self.bias,
                                                   self.dst)
            patch = cv2.warpPerspective(self.img, self.mat, self.dsize)
            cv2.imshow(self.winname, patch)
            key = cv2.waitKey(0) & 0xFF
            if key == ord("w"):
                self.bias[0, 1] -= 1
            elif key == ord("s"):
                self.bias[0, 1] += 1
            elif key == ord("a"):
                self.bias[0, 0] -= 1
            elif key == ord("d"):
                self.bias[0, 0] += 1
            elif key == ord("q"):
                cv2.imwrite(self.save_path, patch)
                cv2.destroyWindow(self.winname)
                break




