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
from Controllers.CancelController import CancelController
from Components.Analyse.StatComponent import StatComponent
from Components.Analyse.ImageComponent import ImageComponent
from Components.Analyse.ProgressComponent import ProgressComponent

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.__images = []
        self.__detected_sponges = {key:0 for key in Loader.SpongesClasses()}

        self.title = QLabel("Analyse en cours")
        self.title.setFont(QFont("Arial", 20))

        self.statComponent = StatComponent()
        self.imageComponent = ImageComponent()

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.statComponent)
        hLayout.addWidget(self.imageComponent)

        self.progressComponent = ProgressComponent()
        self.progressComponent.sizeHint()

        self.downloadButton = QPushButton("Télécharger les données")
        self.downloadButton.setVisible(False)

        sp_retain = self.downloadButton.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.downloadButton.setSizePolicy(sp_retain)

        self.returnButton = QPushButton("Annuler")
        self.returnButton.clicked.connect(self.returnClick)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addWidget(self.returnButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.title)
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.progressComponent)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

        self.analyseThread = AnalyseThread()
        self.analyseThread.imageProcessedSignal.connect(self.imageProcessed)

        # self.analyseThread.finished.connect(self.isFinishedThread)
        self.analyseThread.onAnalyseFinishedSignal.connect(self.analyseFinished)

    def startAnalyse(self, path: str, images: list[str]):
        self.isAnalyseFinished = False
        self.__images = images
        self.progressComponent.setMaximum(len(images))
        self.analyseThread.start(path, images)

    def returnClick(self, event):
        if self.isAnalyseFinished == False:
            cancel_dialog = CancelController()
            result = cancel_dialog.exec_()

            if result == cancel_dialog.Accepted:
                self.analyseThread.stop()
                self.clickedChangeWidget.emit("MENU", "", [])
                self.resetComponents()
    
        elif self.isAnalyseFinished == True:
            self.clickedChangeWidget.emit("MENU", "", [])
            self.resetComponents()

    @pyqtSlot(int, ProcessedImage)
    def imageProcessed(self, image_index: int, processed_image: ProcessedImage):
        next_image = "Aucune"
        if image_index + 1 < len(self.__images):
            next_image = self.__images[image_index + 1]

        for k in self.__detected_sponges:
            self.__detected_sponges[k] += processed_image.detectionsCount().get(k, 0)

        self.imageComponent.update(processed_image)
        self.statComponent.update(self.__detected_sponges)
        self.progressComponent.update(next_image, image_index + 1)

    def displayButtons(self, returnValue, downloadValue, title):
        self.returnButton.setText(returnValue)
        self.downloadButton.setVisible(downloadValue)
        self.title.setText(title)

    def resetComponents(self):
        self.statComponent.reset()
        self.imageComponent.reset()
        self.progressComponent.reset()
        self.displayButtons("Annuler", False, "Analyse en cours")

        for k in self.__detected_sponges:
            self.__detected_sponges[k] = 0

    # @pyqtSlot()
    # def isFinishedThread(self):
    #     self.displayButtons("Continuer", True)

    @pyqtSlot()
    def analyseFinished(self):
        self.isAnalyseFinished = True
        self.displayButtons("Continuer", True, "Analyse terminée")


