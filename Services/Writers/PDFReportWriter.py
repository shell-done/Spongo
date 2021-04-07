from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView

from Models.Analysis import Analysis
from Services.Writers.HTMLReportWriter import HTMLReportWriter

class PDFReportWriter(HTMLReportWriter):
    def __init__(self, analysis: Analysis):
        super().__init__(analysis)
        self._web_view = QWebEngineView()

    def text(self) -> str:
        return super().text()

    def write(self, filepath: str):
        self._web_view.page().loadFinished.connect(lambda _: self._web_view.page().printToPdf(filepath))
        self._web_view.page().pdfPrintingFinished.connect(lambda fp, success: self.writingCompleted.emit(success))

        self._web_view.setHtml(self.text(), QUrl("qrc:/"))

    def isAsync(self) -> bool:
        return True