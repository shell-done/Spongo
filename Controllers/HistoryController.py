from Services.Writers.HTMLReportWriter import HTMLReportWriter
from Services.Writers.ReportWriter import ReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Components.Widgets.PageTitle import PageTitle
from PyQt5.QtCore import QDir, QFile, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout
from PyQt5.QtPrintSupport import QPrinter
import html
from shutil import copyfile

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController
from Components.History.ResumeComponent import ResumeComponent

class HistoryController(BaseController):

    def __init__(self):
        super().__init__()

        title = PageTitle("Historique des analyses")
        title.backArrowClicked.connect(self._returnClicked)

        self._web_view = QWebEngineView(self)
        self._web_view.loadFinished.connect(self._viewLoaded)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self._web_view)

        self.setLayout(main_layout)

    def start(self, analysis):
        html_report_writer = HTMLReportWriter(analysis)
        html = html_report_writer.text()
        self._web_view.setHtml(html, QUrl("qrc:/"))


    @pyqtSlot()
    def _viewLoaded(self):
        self._web_view.page().printToPdf("test.pdf")

    @pyqtSlot()
    def _returnClicked(self):
        self.changeWidget.emit("/menu")
