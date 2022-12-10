import sys, os
from src.view.MainWidget import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtGui import QIcon

from src.controller.MouseController import *


class MainView(QMainWindow):

    def __init__(self, mouseController, params):
        super().__init__()

        self.mouseController = mouseController
        self.params = params
        self.initUI()


    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.setCentralWidget(MainWidget(self))

        self.setFixedSize(750, 600)
        self.center()
        self.setWindowTitle('WarThunderDistanceFucker')
        self.setWindowIcon(QIcon('assets/icon.png'))

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    mouseController = MouseControllerTester()

    os.chdir("D:\PythonProjects\WarThunderDistanceFuckerApp")
    app = QApplication(sys.argv)
    ex = MainView(mouseController)
    sys.exit(app.exec_())