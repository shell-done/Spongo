import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from threading import Lock

from Components.Analyse.StatComponent import StatComponent
from Components.Analyse.ImageComponent import ImageComponent
from Components.Analyse.ProgressComponent import ProgressComponent
from Services.AnalyseThread import AnalyseThread

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.statComponent = StatComponent()
        self.imageComponent = ImageComponent()

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.statComponent)
        hLayout.addWidget(self.imageComponent)

        self.progressComponent = ProgressComponent()
        self.progressComponent.sizeHint()

        self.returnButton = QPushButton("Retour")
        self.returnButton.clicked.connect(self.returnClick)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.progressComponent)
        mainLayout.addWidget(self.returnButton)

        self.setLayout(mainLayout)

        self.analyseThread = AnalyseThread()
        self.analyseThread.analyseThreadSignal.connect(self.updateDisplay)

    def startAnalyse(self, path, images):
        self.progressComponent.setMaximum(len(images))

        self.analyseThread.setParams(path, images)
        self.analyseThread.start()

    def returnClick(self, event):
        self.clickedChangeWidget.emit("MENU", "", [])

    @pyqtSlot(str, int, dict)
    def updateDisplay(self, image, progressValue, sponges):
        if image != "" and sponges != []:
            self.imageComponent.update(image, sponges)
            self.statComponent.update(sponges)

        self.progressComponent.update(image, progressValue)


