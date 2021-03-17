import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader
from Services.AnalyseThread import AnalyseThread
from Services.TextReportWriter import TextReportWriter
from Services.CSVReportWriter import CSVReportWriter
from Models.ProcessedImage import ProcessedImage
from Models.Analyse import Analyse
from Controllers.CancelController import CancelController
from Components.Analyse.StatComponent import StatComponent
from Components.Analyse.ImageComponent import ImageComponent
from Components.Analyse.ProgressComponent import ProgressComponent

class AnalyseController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self._analyse = None

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
        self.downloadButton.clicked.connect(self.downloadReport)

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

        self.analyseThread.onAnalyseFinishedSignal.connect(self.analyseFinished)

    def startAnalyse(self, path: str, images: list[str]):
        self._analyse = Analyse(images, Loader.SpongesClasses())
        self.progressComponent.setMaximum(self._analyse.imagesCount())

        self.analyseThread.start(path, images)

    @pyqtSlot()
    def returnClick(self):
        if self._analyse.isFinished():
            self.clickedChangeWidget.emit("MENU", "", [])
            self.resetComponents()
        else:
            cancel_dialog = CancelController()
            result = cancel_dialog.exec_()

            if result == cancel_dialog.Accepted:
                self.analyseThread.stop()
                self.clickedChangeWidget.emit("MENU", "", [])
                self.resetComponents()

    @pyqtSlot()
    def downloadReport(self):
        writer = TextReportWriter(self._analyse)
        writer.writeSummary("report.txt")

        writer = CSVReportWriter(self._analyse, shape="rectangle")
        writer.write("report.csv")

    @pyqtSlot(ProcessedImage)
    def imageProcessed(self, processed_image: ProcessedImage):
        self._analyse.addProcessedImage(processed_image)

        next_image = self._analyse.nextImageName()
        if next_image is None:
            next_image = "Pas de prochaine image"

        self.imageComponent.update(processed_image)
        self.statComponent.update(self._analyse.cumulativeDetections())
        self.progressComponent.update(next_image, self._analyse.currentImageIndex(), self._analyse.estimateTimeLeft())

    def displayButtons(self, returnValue: str, showDownload: bool, title: str):
        self.returnButton.setText(returnValue)
        self.downloadButton.setVisible(showDownload)
        self.title.setText(title)

    def resetComponents(self):
        self.statComponent.reset()
        self.imageComponent.reset()
        self.progressComponent.reset()
        self.displayButtons("Annuler", False, "Analyse en cours")

    @pyqtSlot()
    def analyseFinished(self):
        self._analyse.finish()
        self.displayButtons("Continuer", True, "Analyse terminée")

