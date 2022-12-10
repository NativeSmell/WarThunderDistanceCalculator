import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')


import pickle
from keras.models import load_model

from src.model.TargetDetector import *
from src.model.DigitRecognizer import *
from src.model.PlayerDetector import *
from src.model.DistanceCalculator import *
from src.model.ParamsReader import *

from src.view.MainView import *

from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener

if __name__ == "__main__":

    saving_path = "history_data/"

    hog_params = {"orientations": 6,
                  "pixels_per_cell": (2, 2),
                  "cells_per_block": (1, 1),
                  "block_norm": "L2"}

    with open('target_assets/target_map.npy', 'rb') as f:
        target_template = np.load(f)


    params = ParamsReader()
    params.load_params()

    digit_model = pickle.load(open('models/digit_classifire_model.sav', 'rb'))
    player_model = load_model("models/player_cnn")

    target_detector = TargetDetector(template=target_template,
                                     color=(212, 212, 7),
                                     mask_threshold=40,
                                     detect_threshold=0.5)

    player_detector = PlayerDetector(player_model,
                                     color=(245, 201, 54),
                                     friend_marker_color=(103, 215, 86),
                                     friend_mask_threshold=20,
                                     mask_threshold=75,
                                     detect_threshold="max", # 0.75,
                                     search_step=2)

    digit_recognizer = DigitRecognizer(digit_model, hog_params,
                                       bin_threshold=40,
                                       digit_sep_threshold=1)

    distance_calculator = DistanceCalculator(target_detector,
                                             digit_recognizer,
                                             player_detector,
                                             saving_path,
                                             save_history=params.get_param("save_history", str))

    mouseController = MouseControllerPredictor(distance_calculator, params,
                                               button="Button.middle",
                                               alt_button="Key.alt_l",
                                               friend_button="Key.ctrl_l")

    with KeyboardListener(on_press=mouseController.on_press, on_release=mouseController.on_release) as k_listener:
        with Listener(on_click=mouseController.on_click) as listener:
            app = QApplication(sys.argv)
            app.aboutToQuit.connect(params.save_params)
            ex = MainView(mouseController, params)
            sys.exit(app.exec_())

