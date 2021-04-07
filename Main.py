import sys

from PySide2.QtGui import QFontDatabase
from PySide2.QtWidgets import QApplication

from Resources import Resources
from Services.Loader import Loader
from Controllers.WindowController import WindowController

if __name__ == "__main__":
    App = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(":/fonts/mulish.ttf")
    QFontDatabase.addApplicationFont(":/fonts/inconsolata.ttf")
    
    App.setStyleSheet(Loader.PreprocessedQSS())
    Loader.SpongesMorphotypes()

    window = WindowController()

    sys.exit(App.exec_())
