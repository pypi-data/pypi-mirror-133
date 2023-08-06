from ..lib import *


def get_new_name(x, y="crop"):
    _, ext = os.path.splitext(x)
    return x.replace(ext, "_" + y + ext)


def get_new_extension(x, y=".png"):
    x, _ = os.path.splitext(x)
    return x + y


def sift_align(sim, phy, save_path=None):
    _h, _w = sim.shape[:2]
    bgr1 = cv2.resize(sim, (_w * 8, _h * 8), interpolation=cv2.INTER_NEAREST)
    bgr2 = phy

    img1 = cv2.cvtColor(bgr1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(bgr2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    patch = None
    MINIMAL_POINTS = 10
    if len(good) < MINIMAL_POINTS:
        if save_path is not None:
            img_match = cv2.drawMatches(img1, kp1, img2, kp2, good, None)
            name = get_new_name(save_path, "fail")
            cv2.imwrite(name, img_match)
        print(f"Too Less Matching Points. filename: {save_path}")
    else:
        src_pts = np.float32([kp1[m.queryIdx].pt
                              for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt
                              for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = img1.shape
        patch = cv2.warpPerspective(bgr2,
                                    np.linalg.inv(M), (w, h),
                                    flags=cv2.INTER_NEAREST)

        if save_path is not None:
            pts = np.array([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]],
                           dtype=np.float).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3,
                                 cv2.LINE_AA)
            matchesMask = mask.ravel().tolist()
            draw_params = dict(
                matchColor=(0, 255, 0),  # draw matches in green color
                singlePointColor=None,
                matchesMask=matchesMask,  # draw only inliers
                flags=2)

            name = get_new_name(save_path, "succ")
            img_match = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                                        **draw_params)
            cv2.imwrite(name, img_match)

            name = get_new_name(save_path, "crop")
            name = get_new_extension(name, ".png")
            cv2.imwrite(name, patch)
    return patch
