# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import *

from Controllers.WindowController import WindowController

if __name__ == "__main__":
    App = QApplication(sys.argv)

    window = WindowController()
    window.show()

    sys.exit(App.exec())
