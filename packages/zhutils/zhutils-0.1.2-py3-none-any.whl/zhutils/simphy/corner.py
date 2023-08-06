from ..lib import *


class CornerFinder:
    def __init__(self, img) -> None:
        self.img = img.copy()
        self.cnt = 0
        self.ratio = self.adjust_image_ratio()
        self.points = []
        self.winname = "image"
        cv2.imshow(self.winname, self.img)
        cv2.setMouseCallback(self.winname, self.click_event)
        while self.cnt < 4:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyWindow(self.winname)
        self.sort()

    def adjust_image_ratio(self):
        h_lim, w_lim = 1080, 1920
        h, w = self.img.shape[:2]
        ratio = max(h/h_lim, w/w_lim)
        h, w = int(h/ratio), int(w/ratio)
        self.img = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_AREA)
        return ratio

    def sort(self):
        pts = np.array(self.points)
        x_m = pts[:, 0].mean()
        y_m = pts[:, 1].mean()
        new_pts = [None] * 4
        for p in self.points:
            if p[0] - x_m < 0 and p[1] - y_m < 0:
                new_pts[0] = p
            elif p[0] - x_m > 0 and p[1] - y_m < 0:
                new_pts[1] = p
            elif p[0] - x_m > 0 and p[1] - y_m > 0:
                new_pts[2] = p
            elif p[0] - x_m < 0 and p[1] - y_m > 0:
                new_pts[3] = p
            else:
                raise NotImplementedError
        self.points = new_pts

    def click_event(self, event, x, y, flags, params):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 0.5
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
            cv2.putText(self.img,
                        str(x) + ',' + str(y), (x, y), font, font_size,
                        (255, 0, 0), 2)
            cv2.imshow(self.winname, self.img)
            self.cnt += 1
            self.points.append((x*self.ratio, y*self.ratio))
        elif event == cv2.EVENT_RBUTTONDOWN:
            print(x, y)
            b = self.img[y, x, 0]
            g = self.img[y, x, 1]
            r = self.img[y, x, 2]
            cv2.putText(self.img,
                        str(b) + ',' + str(g) + ',' + str(r), (x, y), font,
                        font_size, (255, 255, 0), 2)
            cv2.imshow(self.winname, self.img)

