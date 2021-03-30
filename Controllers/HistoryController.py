from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from Controllers.BaseController import BaseController
from Components.Widgets.StylizedButton import StylizedButton
from Components.Widgets.PageTitle import PageTitle
from Components.History.ReportListComponent import ReportListComponent
from Components.History.ReportComponent import ReportComponent

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

    def start(self, analysis):
        self._report_list_component.reset()
        self._report_component.reset(analysis)

    @pyqtSlot()
    def _returnClicked(self):
        self.changeWidget.emit("/menu")

    @pyqtSlot(str)
    def _currentAnalysisChanged(self, file: str):
        print(file)