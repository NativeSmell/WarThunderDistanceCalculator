import numpy as np
import cv2

class PlayerDetector:

    def __init__(self, model, color=(245, 201, 54), friend_marker_color=(103, 215, 86), mask_threshold=75, friend_mask_threshold=20, detect_threshold=0.25, search_step=2):
        self.model = model
        self.color = color
        self.friend_marker_color = friend_marker_color
        self.mask_threshold = mask_threshold
        self.friend_mask_threshold = friend_mask_threshold
        self.detect_threshold = detect_threshold
        self.search_step = search_step

    def diff_mask(self, img):
        result = img.copy()

        result[np.sum(np.abs(result - np.array(self.color)), axis=-1) > self.mask_threshold] = 0
        result[np.sum(np.abs(result - np.array(self.color)), axis=-1) <= self.mask_threshold] = 255

        return result

    def find_poi(self, img, mask):
        size = int((22 / 434) * img.shape[0])
        coords = []
        data = []
        for i in range(0, img.shape[0] - size, self.search_step):
            for j in range(0, img.shape[0] - size, self.search_step):
                if np.sum(mask[i:i + size, j:j + size]) > 0:
                    cp_im = img[i:i + size, j:j + size]
                    if cp_im.shape[-1] != 22:
                        cp_im = cv2.resize(cp_im, (22, 22), interpolation=cv2.INTER_AREA)
                    data.append(cp_im)
                    coords.append((i, j))

        return coords, data

    def detect(self, img):
        mask = self.diff_mask(img)
        coords, data = self.find_poi(img, mask)
        if not data:
            return np.array([[0, 0]])
        data = np.array(data)

        labels = np.squeeze(self.model.predict(data, verbose=0))
        if self.detect_threshold == "max":
            return np.array(coords)[labels == np.max(labels)]
        return np.array(coords)[labels > self.detect_threshold]

    def detect_friend(self, img):
        result = img.copy()

        result[np.sum(np.abs(result - np.array(self.friend_marker_color)), axis=-1) > self.friend_mask_threshold] = 0
        result[np.sum(np.abs(result - np.array(self.friend_marker_color)), axis=-1) <= self.friend_mask_threshold] = 255

        if result[:, :, 0].sum() == 0:
            return 0, 0, 1, 1

        y = np.min(np.arange(result.shape[0])[result[:, :, 0].sum(axis=1) > 0])
        x = np.min(np.arange(result.shape[1])[result[:, :, 0].sum(axis=0) > 0])

        w = len(np.arange(result.shape[1])[result[:, :, 0].sum(axis=0) > 0])
        h = len(np.arange(result.shape[0])[result[:, :, 0].sum(axis=1) > 0])

        return y, x, h, w

    def run(self, img, from_friend=False):
        if from_friend:
            return self.detect_friend(img)

        result = self.detect(img)
        h = w = int((22 / 434) * img.shape[0])
        y, x = np.median(result, axis=0).astype(int)
        return y, x, h, w

    def __call__(self, img, from_friend=False):
        return self.run(img, from_friend=from_friend)
