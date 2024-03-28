from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QApplication, QLabel, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QCheckBox

class SettingsDialog(QDialog):
    def __init__(self, main):  # <1>
        super().__init__(main)
        
        self.main = main
        
        self.setWindowTitle("Settings")

        QBtn = QDialogButtonBox.Ok 
        group_box = QGroupBox("Map coordinates")

        coord1 = QHBoxLayout()
        self.label1 = QLabel("Top Left corner:")
        self.corner1 = QLineEdit(str(self.main.params.get_param("top_left_corner")))
        self.setButton1 = QPushButton("set", self)

        self.setButton1.clicked.connect(lambda x: self.setButtonClicked("top_left_corner"))
        
        coord1.addWidget(self.label1)
        coord1.addWidget(self.corner1)
        coord1.addWidget(self.setButton1)

        coord2 = QHBoxLayout()
        self.label2 = QLabel("Bottom Right corner:")
        self.corner2 = QLineEdit(str(self.main.params.get_param("bottom_right_corner")))
        self.setButton2 = QPushButton("set", self)
        
        self.setButton2.clicked.connect(lambda x: self.setButtonClicked("bottom_right_corner"))
        
        coord2.addWidget(self.label2)
        coord2.addWidget(self.corner2)
        coord2.addWidget(self.setButton2)
        
        coord_layout = QVBoxLayout()
        
        coord_layout.addLayout(coord1)
        coord_layout.addLayout(coord2)

        group_box.setLayout(coord_layout)


        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        
        self.save_history = QCheckBox("Save history")
        self.save_history.setChecked(self.main.params.get_param("save_history") == "yes")
        self.save_history.toggled.connect(lambda x: self.toggleSave(x, "save_history"))
        
        layout.addWidget(self.save_history)
        layout.addWidget(group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    
    def toggleSave(self,x , key):
        self.main.params.update_param(key, "yes" if x else "no")
    
    def setButtonClicked(self, key):    
        self.main.mouseController.set_coords_output(lambda x: self.set_coords(key, x))        
        self.main.mouseController.set_coords(True)
    
    def set_coords(self, key, x):
        if key == "top_left_corner":
            self.corner1.setText(x)
        elif key == "bottom_right_corner":
           self.corner2.setText(x)

        self.main.params.update_param(key, x)
        
if __name__ == "__main__":
    app = QApplication([])

    dlg = SettingsDialog()
    dlg.exec_()