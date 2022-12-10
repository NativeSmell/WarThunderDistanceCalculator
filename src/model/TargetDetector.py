import cv2
import numpy as np


class TargetDetector:

    def __init__(self, template, color=(212, 212, 7), mask_threshold=40, detect_threshold=0.5):
        self.template = template
        self.color = color
        self.mask_threshold = mask_threshold
        self.detect_threshold = detect_threshold
        self.current_target_template = self.template

    def get_template(self):
        return self.current_target_template

    def calculate_diff(self, img):
        result = img.copy()
        result[np.sum(np.abs(result - np.array(self.color)), axis=-1) > self.mask_threshold] = 0
        result[np.sum(np.abs(result - np.array(self.color)), axis=-1) <= self.mask_threshold] = 255

        return result

    def detect_by_mask(self, mask):
        coef = mask.shape[0] / 434
        dim = (int(self.template.shape[0] * coef), int(self.template.shape[1] * coef))
        template = cv2.resize(self.template, dim, interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(mask, template, cv2.TM_CCOEFF_NORMED)

        self.current_target_template = template

        return np.where(res >= self.detect_threshold)

    def stack_together(self, loc):
        if len(loc[0]):
            return np.mean(loc, axis=-1).astype(int)
        return np.zeros(2).astype(int)

    def run(self, img):
        mask = self.calculate_diff(img)
        loc = self.detect_by_mask(mask)
        return self.stack_together(loc)

    def __call__(self, img):
        return self.run(img)
