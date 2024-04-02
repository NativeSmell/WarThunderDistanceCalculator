from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLCDNumber, QLineEdit, QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QIcon, QIntValidator
from PyQt5.QtCore import QSize

from src.view.BigMainLayout import *
from src.view.SmallMainLayout import *

class MainWidget(QWidget):

    def __init__(self, main, useSmall=False):
        super().__init__()

        self.main = main

        self.lcd = QLCDNumber(self)
        self.lcd2 = QLCDNumber(self)
        self.result_pict = QLabel(self)
        self.button = QPushButton("", self)

        self.status_label = QLabel('')

        self.powerOn = QIcon('assets/poweron.png')
        self.powerOff = QIcon('assets/poweroff.png')
        self.distance_label = QLineEdit()
        self.scale_is_manual = QCheckBox("Manual scale")
      
        self.useSmall = useSmall
        
        self.initUI()

    def initUI(self):
        
        if not self.main.ready_status:
            self.main.statusBar().showMessage('Ready')
            self.button.setToolTip('<b>Start</b> button starts listening to the mouse')
            self.button.setIcon(self.powerOn)

        else:
            self.main.statusBar().showMessage('Started')
            self.button.setToolTip('<b>Stop</b> button stops listening to the mouse')
            self.button.setIcon(self.powerOff)

        
        self.button.clicked.connect(self.buttonClicked)
                
        self.scale_is_manual.setChecked(True)
        self.scale_is_manual.toggled.connect(self.checkBoxClicked)
        self.distance_label.setValidator(QIntValidator(-1, 999, self))
        self.distance_label.setText(str(225))

        self.checkBoxClicked()

        self.main.mouseController.set_output(self.view_result)
        self.main.mouseController.set_input(self.get_distance)
        self.main.mouseController.set_status(self.print_status)
        
        if self.useSmall:
            layout = SmallMainLayout(self)
        else:
            layout = BigMainLayout(self)
            
        layout.initLayout()
        
 
    def print_status(self, status):
        self.status_label.setText(status)

    def convert_cv_to_qt(self, img):
        h, w, ch = img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)

    def get_distance(self):
        return self.distance_label.text() if self.scale_is_manual.isChecked() else -1

    def view_result(self, result):
        self.lcd.display(result[0][0])
        self.lcd2.display(round(result[0][1], 2))
        if not self.useSmall:
            self.result_pict.setPixmap(self.convert_cv_to_qt(result[1]))
        if not self.scale_is_manual.isChecked():
            self.distance_label.setText(str(result[2]))

    def button_toggle(self):
        self.main.ready_status = not self.main.ready_status

    def buttonClicked(self):

        if self.main.ready_status:
            self.main.mouseController.stop()
            self.main.statusBar().showMessage('Ready')
            self.button.setToolTip('<b>Start</b> button starts listening to the mouse')
            self.button.setIcon(self.powerOn)
            self.button_toggle()

        elif not self.main.ready_status:
            self.main.mouseController.start()
            self.main.statusBar().showMessage('Started')
            self.button.setToolTip('<b>Stop</b> button stops listening to the mouse')
            self.button.setIcon(self.powerOff)
            self.button_toggle()

    def checkBoxClicked(self):
        self.distance_label.setReadOnly(not self.scale_is_manual.isChecked())

