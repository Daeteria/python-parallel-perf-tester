import cv2
import numpy as np


def img_manipulation_task(imgs: list[np.ndarray], work_index: int) -> list[np.ndarray]:
    imgs_out = []
    for img in imgs:
        img_out = img_crop(img, 1.0)
        img_out = img_resize(img_out, 512)
        img_out = img_enhance_contrast(img_out, 2.0)
        imgs_out.append(img_out)

    return imgs_out


def img_resize(img: np.ndarray, max_size: int) -> np.ndarray:
    h, w = img.shape[:2]
    if h > w:
        img = cv2.resize(img, (int(w * max_size / h), max_size))
    else:
        img = cv2.resize(img, (max_size, int(h * max_size / w)))
    return img


def img_crop(img: np.ndarray, aspect_ratio: float) -> np.ndarray:
    h, w = img.shape[:2]
    if h > w:
        crop_h = int(w * aspect_ratio)
        crop_y = (h - crop_h) // 2
        img = img[crop_y : crop_y + crop_h, :]
    else:
        crop_w = int(h * aspect_ratio)
        crop_x = (w - crop_w) // 2
        img = img[:, crop_x : crop_x + crop_w]
    return img


def img_enhance_contrast(img: np.ndarray, amount: float = 2.0) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=amount, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return enhanced_img
