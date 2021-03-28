# This Python file uses the following encoding: utf-8
from Services.NeuralNetwork.NeuralNetwork import NeuralNetwork
from PyQt5.QtCore import QThread, QUrl, pyqtSlot
import sys
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

from Services.Loader import Loader
from Controllers.WindowController import WindowController

# def save():
#    w.page().printToPdf("test.pdf")

if __name__ == "__main__":
    App = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("Resources/fonts/mulish.ttf")
    App.setStyleSheet(Loader.PreprocessedQSS())
    Loader.SpongesMorphotypes()

    #w = QWebEngineView()
    # w.load(QUrl("https://www.alexandre-thomas.fr"))
    # content = open("Resources/documents/report_template.html", encoding="utf-8").read()
    # w.loadFinished.connect(save)
    # w.setHtml(content, QUrl("qrc:/"))
    # w.show()

    window = WindowController()

    sys.exit(App.exec())
