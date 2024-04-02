
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

class BigMainLayout():
    def __init__(self, widget):
        self.widget = widget
        
    
    def initLayout(self):
        
        self.widget.main.setFixedSize(750, 600)
        self.widget.button.setIconSize(QSize(125, 125))
        
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

        pixmap = QPixmap('assets/map.png')
        self.widget.result_pict.setPixmap(pixmap)

        self.widget.lcd.setFixedSize(225, 225 //2)
        self.widget.lcd2.setFixedSize(225, 225 // 2)
        self.widget.button.setFixedSize(125, 125)
        dist_label.setFixedSize(225, 40)
        azimuth_label.setFixedSize(225, 40)
        self.widget.result_pict.setFixedSize(434, 434)

        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.widget.button)
        button_hbox.addStretch(1)

        status_hbox = QHBoxLayout()
        status_hbox.addStretch(1)
        status_hbox.addWidget(self.widget.status_label)
        status_hbox.addStretch(1)

        scale_hbox = QHBoxLayout()
        scale_hbox.addWidget(scale_label)
        scale_hbox.addStretch(1)
        scale_hbox.addWidget(self.widget.distance_label)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)
        vbox.addLayout(status_hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.widget.scale_is_manual)
        vbox.addLayout(scale_hbox)
        vbox.addWidget(dist_label)
        vbox.addWidget(self.widget.lcd)
        vbox.addWidget(azimuth_label)
        vbox.addWidget(self.widget.lcd2)

        hbox_right = QHBoxLayout()
        hbox_right.addStretch(1)
        hbox_right.addWidget(donation_label)
        hbox_right.addWidget(donation_qr)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.widget.result_pict)
        vbox_right.addStretch(1)
        vbox_right.addLayout(hbox_right)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vbox_right)

        self.widget.setLayout(hbox)