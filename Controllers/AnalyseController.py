import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader
from Models.ProcessedImage import ProcessedImage
from Services.AnalyseThread import AnalyseThread
from Components.Analyse.StatComponent import StatComponent
from Components.Analyse.ImageComponent import ImageComponent
from Components.Analyse.ProgressComponent import ProgressComponent

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.__images = []
        self.__detected_sponges = {key:0 for key in Loader.SpongesClasses()}
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
        self.analyseThread.imageProcessedSignal.connect(self.imageProcessed)

    def startAnalyse(self, path: str, images: list[str]):
        self.__images = images
        self.progressComponent.setMaximum(len(images))
        self.analyseThread.start(path, images)

    def returnClick(self, event):
        self.analyseThread.stop()
        self.clickedChangeWidget.emit("MENU", "", [])

    @pyqtSlot(int, ProcessedImage)
    def imageProcessed(self, image_index: int, processed_image: ProcessedImage):
        next_image = "Pas de prochaine image"
        if image_index + 1 < len(self.__images):
            next_image = self.__images[image_index + 1]

        for k in self.__detected_sponges:
            self.__detected_sponges[k] += processed_image.detectionsCount().get(k, 0)

        self.imageComponent.update(processed_image)
        self.statComponent.update(self.__detected_sponges)
        self.progressComponent.update(next_image, image_index + 1)



