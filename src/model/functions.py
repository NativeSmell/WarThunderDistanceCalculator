import cv2, os
import numpy as np
from datetime import datetime
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


def get_date():
    return datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")


def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def noize_filter(digit):
    top = np.vstack((np.zeros((1, 28, 3)), digit[:-1, :, :]))
    bottom = np.vstack((digit[1:, :, :], np.zeros((1, 28, 3))))

    left = np.hstack((np.zeros((28, 1, 3)), digit[:, :-1, :]))
    right = np.hstack((digit[:, 1:, :], np.zeros((28, 1, 3))))

    return np.where((left + digit + right + top + bottom) / 255 < 3, 0, 255)


def sep_digits(coords, img):
    digits = []
    for start, end in coords:
        digit = img[:, start:end, :]
        digit = noize_filter(add_dummy(digit, 28))
        if np.sum(digit) / 255 > 40:
            digits.append(digit)
    return digits


def add_dummy(img, size):
    if 0 in img.shape or img.shape[1] > size:
        return np.zeros((size,size, 3))

    top = (size - img.shape[0]) // 2
    bottom = size - (img.shape[0] + top)

    top = np.zeros((top, img.shape[1], 3))
    bottom = np.zeros((bottom, img.shape[1], 3))

    result = np.vstack([top, img, bottom])

    left = (size - result.shape[1]) // 2
    right = size - (result.shape[1] + left)

    left = np.zeros((result.shape[0], left, 3))
    right = np.zeros((result.shape[0], right, 3))

    return np.hstack([left, result, right])


def crop_image(y_from, y_to, x_from, x_to, img):
    y_from_abs = int((y_from))
    y_to_abs = int((y_to))

    x_from_abs = int((x_from))
    x_to_abs = int((x_to))

    return img[y_from_abs:y_to_abs,
           x_from_abs:x_to_abs].copy()

def bin_img(threshold, img):
    result_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    result_img = np.where(result_img < threshold, 255, 0)

    return bin_to_3_chanel(result_img, img)


def bin_to_3_chanel(bin_img, img):
    gray = img.copy()
    gray[:, :, 0] = bin_img
    gray[:, :, 1] = bin_img
    gray[:, :, 2] = bin_img

    return gray

def moving_average(a, n=10) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def cal_dist(x1, y1, x2, y2, coef):
    dist = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return int(dist * coef)


def cal_angle(cathetus, hypotenuse):
    return np.degrees(np.arccos(cathetus/hypotenuse))
