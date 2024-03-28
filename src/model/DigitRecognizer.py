import numpy as np

from src.model.functions import *
from skimage.feature import hog


class DigitRecognizer:

    def __init__(self, model, hog_params, bin_threshold=25, digit_sep_threshold=1):
        self.model = model
        self.bin_threshold = bin_threshold
        self.digit_sep_threshold = digit_sep_threshold * 3 * 255
        self.hog_params = hog_params


    def check_dists_on_seasons(self, dists):
        result = []
        for el in np.unique(dists):
            temp = np.array(dists) % el
            result += [el] * (len(temp[temp == 0]))
        return result

    def find_square(self, lines):
        result = []
        for l in lines:
            if l[0] == l[2]:
                temp_lines = lines[lines[:, 0 ] != lines[:, 2], 0:2]
                temp_lines[:,0] = l[0]
                result += temp_lines.tolist()

        return np.array(result)
    
    def calculate_scale_line(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 100, apertureSize=5)
        
        minLineLength = img.shape[0] * 0.975
        maxLineGap = img.shape[0] * .1
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100,
                                lines=np.array([]), minLineLength=minLineLength,
                                maxLineGap=maxLineGap)

        if lines is None:
            return -1

        lines = lines[(lines[:, :, 0] == lines[:, :, 2]) | (lines[:, :, 1] == lines[:, :, 3])]
        dists = []
        
        cross = self.find_square(lines)
    
        for cr in cross:
            np.abs(np.sum(cross - cr, axis = -1))
            dists += np.abs(np.sum(cross - cr, axis = -1)).tolist()
        
        # for x,y in lines[:, 0:2]:
        #     dists += list(np.abs(lines[:, 0] - x))
        #     dists += list(np.abs(lines[:, 1] - y))
        

        dists = list(filter(lambda el: img.shape[0] // 8 < el < img.shape[0] // 2, dists))
        dists = self.check_dists_on_seasons(dists)

        return max(set(dists), key=dists.count) if len(dists) else -1

    def crop_to_digits(self, img, w):
        bin = bin_img(self.bin_threshold, img)
        col_sum = np.sum(bin[:, :, 0], axis=0)
        threshold = np.mean(col_sum[col_sum > 0]) / 4
        x_from = np.arange(len(col_sum))[col_sum > threshold][0] - 10

        if np.mean(bin[-1, x_from + 10:x_from + 10 + w, 0]) > 200:
            bin[-2:,:,:] = 0
        bin = bin[np.sum(bin[:,:,0], axis = 1) > 255]
        return bin[:,x_from:,:]

    def find_digit_edges(self, img):
        index = []
        space = False
        start = 0
        for i in range(img.shape[1]):
            if np.sum(img[:, i, :]) <= self.digit_sep_threshold:
                if not space:
                    index.append([start, i])
                    space = True
            else:
                if space:
                    start = i
                space = False
        return index

    def calculate_hog(self, digits):
        return np.array([hog(digit[:, :, -1], **self.hog_params) for digit in digits])

    def make_prediction(self, x):
        if not len(x):
            return -1
        return int("".join(self.model.predict(x).astype(str)))

    def run(self, img, w):
        if not len(img):
            return -1, [np.random.randint(0, 255, size=(28, 28, 3))] * 3
        crop = self.crop_to_digits(img, w)
        coords = self.find_digit_edges(crop)
        digits = sep_digits(coords, crop)
        x = self.calculate_hog(digits[:3])

        return self.make_prediction(x), digits

    def __call__(self, img, w):
        return self.run(img, w)
