from Components.History.ReportListComponent import ReportListComponent
from Models.Analysis import Analysis
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from Services.Writers.ReportWriter import ReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Components.Widgets.PageTitle import PageTitle
from PyQt5.QtCore import QDir, QFile, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout
from PyQt5.QtPrintSupport import QPrinter
from shutil import copyfile

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController
from Components.History.ReportComponent import ReportComponent

class HistoryController(BaseController):

    def __init__(self):
        super().__init__()

        title = PageTitle("Historique des analyses")
        title.backArrowClicked.connect(self._returnClicked)

        components_layout = QHBoxLayout()
        components_layout.setSpacing(20)

        self._report_component = ReportComponent()
        self._report_list_component = ReportListComponent()

        components_layout.addWidget(self._report_list_component, 2)
        components_layout.addWidget(self._report_component, 4)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(components_layout)

        self.setLayout(main_layout)

    def start(self, analysis):
        self._report_list_component.reset()
        self._report_component.reset(analysis)

    @pyqtSlot()
    def _returnClicked(self):
        self.changeWidget.emit("/menu")
