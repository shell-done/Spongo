from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout

from Models.Analysis import Analysis
from Components.Widgets.StylizedButton import StylizedButton
from Components.Widgets.PageTitle import PageTitle
from Components.History.ReportListComponent import ReportListComponent
from Components.History.ReportComponent import ReportComponent
from Controllers.BaseController import BaseController
from Controllers.DownloadController import DownloadController

class HistoryController(BaseController):

    def __init__(self):
        super().__init__()

        title = PageTitle("Historique des analyses")
        title.backArrowClicked.connect(self._returnClicked)

        components_layout = QHBoxLayout()
        components_layout.setSpacing(20)

        self._report_list_component = ReportListComponent()
        self._report_list_component.currentAnalysisChanged.connect(self._currentAnalysisChanged)

        self._report_component = ReportComponent()

        components_layout.addWidget(self._report_list_component, 2)
        components_layout.addWidget(self._report_component, 4)

        self._export_button = StylizedButton("Exporter les données", "blue")

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.setSpacing(35)
        button_layout.addWidget(self._export_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(components_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Signals
        self._export_button.clicked.connect(self._exportReport)

    def start(self, analysis):
        self._analysis = analysis

        self._report_list_component.reset(self._analysis)
        self._report_component.reset(self._analysis)
        self._export_button.setEnabled(True)

    @Slot()
    def _exportReport(self):
        download_dialog = DownloadController(self)
        download_dialog.start(self._analysis)

        download_dialog.exec_()

    @Slot()
    def _returnClicked(self):
        self.changeWidget.emit("/menu", None)

    @Slot(Analysis)
    def _currentAnalysisChanged(self, analysis: Analysis):
        self._analysis = analysis
        self._report_component.reset(analysis)

        has_analysis = True if analysis else False
        self._export_button.setEnabled(has_analysis)
