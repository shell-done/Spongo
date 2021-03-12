import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from threading import Lock

from Components.Analyse.DataComponent import DataComponent
from Components.Analyse.ImageComponent import ImageComponent
from Components.Analyse.ProgressBarComponent import ProgressBarComponent
from Services.AnalyseThread import AnalyseThread

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.dataComponent = DataComponent()
        self.imageComponent = ImageComponent()

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.dataComponent)
        hLayout.addWidget(self.imageComponent)

        self.progressComponent = ProgressBarComponent()

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
            self.imageComponent.update(image)
            self.dataComponent.update(sponges)

        self.progressComponent.update(progressValue)


