# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from Services.Loader import Loader
from Controllers.WindowController import WindowController

if __name__ == "__main__":
    App = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("Resources/fonts/mulish.ttf")
    App.setStyleSheet(Loader.PreprocessedQSS())

    window = WindowController()

    sys.exit(App.exec())
