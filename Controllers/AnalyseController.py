import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.AnalyseThread import AnalyseThread

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.analyseThread = AnalyseThread()

        self.mainLayout = QVBoxLayout()

        self.label = QLabel("Lancement de l'analyse...")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.label)

        self.progressBar = QProgressBar()
        self.mainLayout.addWidget(self.progressBar)

        self.returnButton = QPushButton("Retour")
        self.mainLayout.addWidget(self.returnButton)

        self.setLayout(self.mainLayout)

        self.returnButton.clicked.connect(self.returnClick)

        self.analyseThread.analyseThreadSignal.connect(self.updateDisplay)

    def startAnalyse(self, path, images):
        self.progressBar.setMaximum(len(images))
        print("nb images : " + str(len(images)))

        self.analyseThread.setParams(path, images)
        self.analyseThread.start()

    def returnClick(self, event):
        self.clickedChangeWidget.emit("MENU", "", [])

    @pyqtSlot(str, int)
    def updateDisplay(self, image, progressValue):
        # update image displayed
        if image != "":
            pixmap = QPixmap("data/predictions/" + image)
            self.label.setPixmap(pixmap.scaled(self.label.size()))

        # update progress bar
        self.progressBar.setValue(progressValue)


