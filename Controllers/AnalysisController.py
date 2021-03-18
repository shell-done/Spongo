from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Models.Parameters import Parameters
from Services.Loader import Loader
from Services.AnalysisThread import AnalysisThread
from Services.TextReportWriter import TextReportWriter
from Services.CSVReportWriter import CSVReportWriter
from Models.ProcessedImage import ProcessedImage
from Models.Analysis import Analysis
from Controllers.BaseController import BaseController
from Controllers.Dialogs.CancelDialog import CancelDialog
from Components.Analysis.StatComponent import StatComponent
from Components.Analysis.ImageComponent import ImageComponent
from Components.Analysis.ProgressComponent import ProgressComponent

class AnalysisController(BaseController):
    clickedChangeWidget = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._analysis = None

        self._title = QLabel("Analyse en cours")
        self._title.setFont(QFont("Arial", 20))

        self._stat_component = StatComponent()
        self._image_component = ImageComponent()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self._stat_component)
        h_layout.addWidget(self._image_component)

        self._progress_component = ProgressComponent()
        self._progress_component.sizeHint()

        self._export_button = QPushButton("Télécharger les données")
        self._export_button.setVisible(False)
        self._export_button.clicked.connect(self._exportReport)

        sp_retain = self._export_button.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self._export_button.setSizePolicy(sp_retain)

        self._return_button = QPushButton("Annuler")
        self._return_button.clicked.connect(self._returnClick)

        _button_layout = QHBoxLayout()
        _button_layout.addWidget(self._export_button)
        _button_layout.addWidget(self._return_button)

        _main_layout = QVBoxLayout()
        _main_layout.addWidget(self._title)
        _main_layout.addLayout(h_layout)
        _main_layout.addWidget(self._progress_component)
        _main_layout.addLayout(_button_layout)

        self.setLayout(_main_layout)

        self._analysis_thread = AnalysisThread()
        self._analysis_thread.imageProcessedSignal.connect(self._imageProcessed)
        self._analysis_thread.onAnalysisFinishedSignal.connect(self._analysisFinished)

    def start(self, parameters: Parameters, images: list[str]):
        self._analysis = Analysis(images, Loader.SpongesClasses())

        self._stat_component.reset()
        self._image_component.reset()
        self._progress_component.reset(self._analysis.imagesCount())
        self._displayButtons("Annuler", False, "Analyse en cours")

        self._analysis_thread.start(parameters, images)

    def stop(self):
        self._progress_component.stop()


    def _displayButtons(self, returnValue: str, showDownload: bool, title: str):
        self._return_button.setText(returnValue)
        self._export_button.setVisible(showDownload)
        self._title.setText(title)


    @pyqtSlot()
    def _returnClick(self):
        if self._analysis.isFinished():
            self.clickedChangeWidget.emit("MENU")
        else:
            cancel_dialog = CancelController()
            result = cancel_dialog.exec_()

            if result == cancel_dialog.Accepted:
                self._analysis_thread.stop()
                self.clickedChangeWidget.emit("MENU")

    @pyqtSlot()
    def _exportReport(self):
        writer = TextReportWriter(self._analysis)
        writer.writeSummary("report.txt")

        writer = CSVReportWriter(self._analysis, shape="rectangle")
        writer.write("report.csv")

    @pyqtSlot(ProcessedImage)
    def _imageProcessed(self, processed_image: ProcessedImage):
        self._analysis.addProcessedImage(processed_image)

        next_image = self._analysis.nextImageName()
        if next_image is None:
            next_image = "Pas de prochaine image"

        self._image_component.update(processed_image)
        self._stat_component.update(self._analysis)
        self._progress_component.update(next_image, self._analysis.currentImageIndex(), self._analysis.estimateTimeLeft())

    @pyqtSlot()
    def _analysisFinished(self):
        self._analysis.finish()
        self._displayButtons("Continuer", True, "Analyse terminée")

