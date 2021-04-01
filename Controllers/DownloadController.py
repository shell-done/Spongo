from Services.Writers.ReportWriter import ReportWriter
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QVBoxLayout

from Controllers.BaseController import BaseController
from Components.Widgets.StylizedButton import StylizedButton
from Components.Widgets.PageTitle import PageTitle
from Components.Download.DownloadComponent import DownloadComponent
from Components.Download.PreviewComponent import PreviewComponent
from Models.Analysis import Analysis

class DownloadController(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Spongo")
        self.setFixedSize(1000, 600)
        self.setWindowIcon(QIcon("Resources/img/spongo_icon.png"))

        title = PageTitle("Téléchargement des données")
        title.backArrowClicked.connect(self._returnClicked)

        components_layout = QGridLayout()
        components_layout.setSpacing(20)
        components_layout.setColumnStretch(0, 4)
        components_layout.setColumnStretch(1, 3)

        self._download_component = DownloadComponent()
        self._preview_component = PreviewComponent()

        components_layout.addWidget(self._download_component, 0, 0)
        components_layout.addWidget(self._preview_component, 0, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(components_layout)

        self.setLayout(main_layout)

        # Slots
        self._download_component.reportFormatChanged.connect(self._preview_component.update)
        self._download_component.saveCompleted.connect(self._saveCompleted)

    def start(self, analysis: Analysis):
        self._analysis = analysis

        self._download_component.reset(self._analysis)

    @pyqtSlot(bool)
    def _saveCompleted(self, sucess: bool):
        self.close()

    @pyqtSlot()
    def _returnClicked(self):
        self.close()
