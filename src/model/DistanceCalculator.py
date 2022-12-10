from src.model.functions import *


class DistanceCalculator:

    def __init__(self, target_detector, digit_recognizer, player_detector, path, save_history="yes"):
        self.target_detector = target_detector
        self.digit_recognizer = digit_recognizer
        self.player_detector = player_detector
        self.path = path
        self.date = None
        self.img_to_show = None
        self.save_history = save_history

    def crop_minimap(self, img):
        y_from, y_to = 994 / 1440, 1422 / 1440
        x_from, x_to = 2113 / 2560, 2543 / 2560

        crop_map = crop_image(y_from, y_to, x_from, x_to, img)
        if self.save_history == "yes":
            cv2.imwrite(self.path + f'{self.date}_crop_map.png', cv2.cvtColor(crop_map, cv2.COLOR_RGB2BGR))

        return crop_map

    def convert_xy(self, x_y, img):

        if x_y is None:
            return None

        y_from, y_to = 994 / 1440, 1422 / 1440
        x_from, x_to = 2113 / 2560, 2543 / 2560

        y_from_abs = x_y[1] - int((y_from * img.shape[0]))
        x_from_abs = x_y[0] - int((x_from * img.shape[1]))

        return x_from_abs, y_from_abs

    def detect_target(self, img, x_y=None):
        if x_y is None:
            y_t, x_t = self.target_detector(img)
            h_t, w_t = self.target_detector.get_template().shape[:-1]
        else:
            x_t, y_t = x_y
            h_t = w_t = 2
        cv2.rectangle(self.img_to_show, (x_t, y_t), (x_t + w_t, y_t + h_t), (0, 0, 255), 2)

        return y_t, x_t, h_t, w_t

    def detect_player(self, img, from_friend=False):
        y_p, x_p, h_p, w_p = self.player_detector(img, from_friend=from_friend)
        cv2.rectangle(self.img_to_show, (x_p, y_p), (x_p + w_p, y_p + h_p), (0, 0, 255), 1)

        return y_p, x_p, h_p, w_p

    def recognize_scale(self, img, distance=-1):
        h, w = 1, self.digit_recognizer.calculate_scale_line(img)

        if distance > 0:
            return distance, w

        y_from, y_to = (428 - 24) / 430, 428 / 430
        x_from, x_to = 267 / 430, 432 / 430
        crop = crop_image(y_from, y_to, x_from, x_to, img)

        scale, digits = self.digit_recognizer(crop, w)

        if scale != -1:
            if self.save_history == "yes":
                cv2.imwrite(self.path + f'{self.date}_digits_{scale}.png', np.hstack(digits))

        return scale, w

    def draw_and_save_to_show(self, x_p, y_p, x_t, y_t, w_p, h_p, w_t, h_t):
        cv2.line(self.img_to_show, (x_p + w_p // 2, y_p + h_p // 2), (x_t + w_t // 2, y_t + h_t // 2), (255, 0, 0),
                 thickness=1)
        if self.save_history == "yes":
            cv2.imwrite(self.path + f'{self.date}_show.png', cv2.cvtColor(self.img_to_show, cv2.COLOR_RGB2BGR))


    def cal_azimuth(self, angle, dx, dy):

        if dx <= 0:
            if dy <= 0:
                return 180 - angle
            else:
                return angle
        else:
            if dy <= 0:
                return 180 + angle
            else:
                return 360 - angle


    def run(self, img, distance=-1, x_y=None, from_friend=False):
        img = np.array(img)
        self.date = get_date()
        if self.save_history == "yes":
            cv2.imwrite(self.path + f'{self.date}_full.png', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        crop_map = self.crop_minimap(img)
        self.img_to_show = crop_map.copy()

        y_t, x_t, h_t, w_t = self.detect_target(crop_map, x_y=self.convert_xy(x_y, img))
        y_p, x_p, h_p, w_p = self.detect_player(crop_map, from_friend=from_friend)
        scale, line_w = self.recognize_scale(crop_map, distance=distance)
        self.draw_and_save_to_show(x_p, y_p, x_t, y_t, w_p, h_p, w_t, h_t)

        distance = cal_dist(x_p + w_p // 2, y_p + h_p // 2,
                            x_t + w_t // 2, y_t + h_t // 2,
                            scale / line_w)

        north_line = cal_dist(x_p + w_p // 2, y_p + h_p // 2,
                            x_p + w_p // 2, y_t + h_t // 2,
                            scale / line_w)

        angle = cal_angle(north_line, distance)
        azimuth = self.cal_azimuth(angle, (x_p + w_p // 2) - (x_t + w_t // 2), (y_p + h_p // 2) - (y_t + h_t // 2))

        if self.save_history == "yes":
            with open(self.path + f"{self.date}.txt", "wt") as f:
                f.write(f"{x_p=}\n{y_p=}\n{w_p=}\n{h_p=}\n")
                f.write(f"{x_t=}\n{w_t=}\n{y_t=}\n{h_t=}\n")
                f.write(f"{distance=}\n{scale=}\n{azimuth=}")

        return (distance, azimuth), self.img_to_show, scale

    def __call__(self, img, distance=-1, x_y=None, from_friend=False):
        return self.run(img, distance=distance, x_y=x_y, from_friend=from_friend)
