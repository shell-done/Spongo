from PyQt5.QtCore import QUrl
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from Services.Writers.ReportWriter import ReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Models.Analysis import Analysis

class PDFReportWriter(ReportWriter):
    def __init__(self, analysis: Analysis):
        super().__init__(analysis)

        self._html_report_writer = HTMLReportWriter(self._analysis)
        self._web_view = QWebEngineView()

    def text(self) -> str:
        return None

    def write(self, filepath: str):
        self._web_view.loadFinished.connect(lambda _: self._web_view.page().printToPdf(filepath))

        self._web_view.setHtml(self._html_report_writer.text(), QUrl("qrc:/"))