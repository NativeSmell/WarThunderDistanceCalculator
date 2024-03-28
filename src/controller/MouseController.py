import pyautogui
from time import sleep
from threading import Thread

class MouseControllerPredictor:

    def __init__(self, predictor, params, button="Button.middle", alt_button="Key.alt_l", friend_button="Key.ctrl_l", output=print, _input=input, status=print, coords_output=print):
        self.button = button
        self.alt_button = alt_button
        self.friend_button = friend_button
        self.predictor = predictor
        self.input = _input
        self.output = output
        self.params = params
        self.status = status
        self.isPaused = True
        self.altPressed = False
        self.friendPressed = False

        self.setCoords = False
        self.coords_output = coords_output
        
    def start(self):
        self.isPaused = False

    def stop(self):
        self.isPaused = True

    def set_output(self, output):
        self.output = output

    def set_input(self, _input):
        self.input = _input

    def set_status(self, status):
        self.status = status

    def set_coords(self,status):
        self.setCoords = status

    def set_coords_output(self, output):
        self.coords_output = output
    
    def make_prediction(self, x, y):
        sleep(0.15)
        result = self.predictor(pyautogui.screenshot(), distance=int(self.input()),
                                x_y=(x, y) if self.altPressed else None,
                                from_friend=self.friendPressed)
        self.output(result)

    def on_click(self, x, y, button, pressed):
        self.status(str(button) + " mouse pressed: " + str(pressed))
        if not self.isPaused and pressed and str(button) == self.button:
            x = Thread(target=self.make_prediction, args=[x, y])
            x.start()
        if self.setCoords and self.altPressed:
            self.coords_output(f"{x},{y}")
            self.setCoords = False

    def on_press(self, key):
        self.status(str(key) + " keyboard pressed")
        if not self.altPressed and str(key) == self.alt_button:
            self.altPressed = True
        if not self.friendPressed and str(key) == self.friend_button:
            self.friendPressed = True

    def on_release(self, key):
        self.status(str(key) + " keyboard release")
        if self.altPressed and str(key) == self.alt_button:
            self.altPressed = False
        if self.friendPressed and str(key) == self.friend_button:
            self.friendPressed = False

class MouseControllerTester:

    def __init__(self, button="Button.middle", output=print):
        self.button = button
        self.output = output
        self.isPaused = True

    def start(self):
        self.isPaused = False

    def stop(self):
        self.isPaused = True

    def set_output(self, output):
        self.output = output

    def make_prediction(self):
        import numpy as np
        print("Make prediction")
        self.output((120, np.random.randint(0, 255, size=(512, 512, 3))))

    def on_click(self, x, y, button, pressed):
        if not self.isPaused and pressed and str(button) == self.button:
            return self.make_prediction()
