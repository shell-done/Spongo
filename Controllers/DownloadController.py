from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QGridLayout, QVBoxLayout

from Models.Analysis import Analysis
from Components.Widgets.PageTitle import PageTitle
from Components.Download.DownloadComponent import DownloadComponent
from Components.Download.PreviewComponent import PreviewComponent

class DownloadController(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Spongo")
        self.setFixedSize(950, 550)
        self.setWindowIcon(QIcon(":/img/spongo_icon.png"))

        title = PageTitle("Téléchargement des données")
        title.backArrowClicked.connect(self._returnClicked)

        components_layout = QGridLayout()
        components_layout.setContentsMargins(10, 10, 10, 10)
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

    @Slot(bool)
    def _saveCompleted(self, success: bool):
        self.close()

    @Slot()
    def _returnClicked(self):
        self.close()
