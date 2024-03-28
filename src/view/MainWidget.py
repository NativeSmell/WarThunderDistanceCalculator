from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLCDNumber, QLineEdit, QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QIcon, QIntValidator
from PyQt5.QtCore import QSize

class MainWidget(QWidget):

    def __init__(self, main):
        super().__init__()

        self.main = main

        self.lcd = QLCDNumber(self)
        self.lcd2 = QLCDNumber(self)
        self.result_pict = QLabel(self)
        self.button = QPushButton("", self)

        self.button_status = False
        self.status_label = QLabel('')

        self.powerOn = QIcon('assets/poweron.png')
        self.powerOff = QIcon('assets/poweroff.png')
        self.distance_label = QLineEdit()
        self.scale_is_manual = QCheckBox("Set scale manually")

        self.initUI()

    def initUI(self):

        self.button.clicked.connect(self.buttonClicked)
        self.button.setToolTip('<b>Start</b> button starts listening to the mouse')
        self.button.setIcon(self.powerOn)
        self.button.setIconSize(QSize(125, 125))
        self.scale_is_manual.setChecked(True)
        self.scale_is_manual.toggled.connect(self.checkBoxClicked)
        self.distance_label.setValidator(QIntValidator(-1, 999, self))
        self.distance_label.setText(str(225))
        
        self.checkBoxClicked()

        dist_label = QLabel("""
                               <h1 style="text-align: center;">
                               <span style="color: #5e9ca0;">Distance:</span>
                               </h1>
                            """)

        azimuth_label = QLabel("""
                                       <h1 style="text-align: center;">
                                       <span style="color: #5e9ca0;">Azimuth:</span>
                                       </h1>
                                    """)

        scale_label = QLabel("""
                               <h2 style="text-align: center;">
                               <span style="color: #5e9ca0;">Scale:</span>
                               </h2>
                            """)

        donation_label = QLabel("""
                                       <h2 style="text-align: center;">
                                       <span style="color: #DD741C;">Support the author:</span>
                                       </h2>
                                    """)
        donation_qr = QLabel("qiwi.com/n/MARTTRAIN")
        donation_qr.setPixmap(QPixmap("assets/qr.png"))

        self.main.mouseController.set_output(self.view_result)
        self.main.mouseController.set_input(self.get_distance)
        self.main.mouseController.set_status(self.print_status)

        pixmap = QPixmap('assets/map.png')
        self.result_pict.setPixmap(pixmap)

        self.lcd.setFixedSize(225, 225 //2)
        self.lcd2.setFixedSize(225, 225 // 2)
        self.button.setFixedSize(125, 125)
        dist_label.setFixedSize(225, 40)
        azimuth_label.setFixedSize(225, 40)
        self.result_pict.setFixedSize(434, 434)

        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.button)
        button_hbox.addStretch(1)

        status_hbox = QHBoxLayout()
        status_hbox.addStretch(1)
        status_hbox.addWidget(self.status_label)
        status_hbox.addStretch(1)

        scale_hbox = QHBoxLayout()
        scale_hbox.addWidget(scale_label)
        scale_hbox.addStretch(1)
        scale_hbox.addWidget(self.distance_label)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)
        vbox.addLayout(status_hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.scale_is_manual)
        vbox.addLayout(scale_hbox)
        vbox.addWidget(dist_label)
        vbox.addWidget(self.lcd)
        vbox.addWidget(azimuth_label)
        vbox.addWidget(self.lcd2)

        hbox_right = QHBoxLayout()
        hbox_right.addStretch(1)
        hbox_right.addWidget(donation_label)
        hbox_right.addWidget(donation_qr)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.result_pict)
        vbox_right.addStretch(1)
        vbox_right.addLayout(hbox_right)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vbox_right)

        self.setLayout(hbox)

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
        self.result_pict.setPixmap(self.convert_cv_to_qt(result[1]))
        if not self.scale_is_manual.isChecked():
            self.distance_label.setText(str(result[2]))

    def button_toggle(self):
        self.button_status = not self.button_status

    def buttonClicked(self):

        if self.button_status:
            self.main.mouseController.stop()
            self.main.statusBar().showMessage('Ready')
            self.button.setToolTip('<b>Start</b> button starts listening to the mouse')
            self.button.setIcon(self.powerOn)
            self.button_toggle()

        elif not self.button_status:
            self.main.mouseController.start()
            self.main.statusBar().showMessage('Started')
            self.button.setToolTip('<b>Stop</b> button stops listening to the mouse')
            self.button.setIcon(self.powerOff)
            self.button_toggle()

    def checkBoxClicked(self):
        self.distance_label.setReadOnly(not self.scale_is_manual.isChecked())

