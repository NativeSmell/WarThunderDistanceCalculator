
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QSize

class SmallMainLayout():
    def __init__(self, widget):
        self.widget = widget
        
    
    def initLayout(self):
        
        self.widget.main.setFixedSize(175, 125)
        self.widget.button.setIconSize(QSize(20, 20))
        
        dist_label = QLabel("""
                               <span style="color: #5e9ca0;">DST:</span>
                            """)

        azimuth_label = QLabel("""
                                       <span style="color: #5e9ca0;">AZ:</span>
                                    """)

        scale_label = QLabel("""
                               <span style="color: #5e9ca0;">Scale:</span>
                            """)

              
        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.widget.button)
        button_hbox.addWidget(scale_label)
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.widget.distance_label)

        hbox = QHBoxLayout()
        hbox.addWidget(dist_label)
        hbox.addWidget(self.widget.lcd)
        hbox.addWidget(azimuth_label)
        hbox.addWidget(self.widget.lcd2)

        vbox = QVBoxLayout()
        vbox.addLayout(button_hbox)
        vbox.addLayout(hbox)
        
        self.widget.setLayout(vbox)