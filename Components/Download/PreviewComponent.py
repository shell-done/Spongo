from Components.Widgets.StylizableWidget import StylizableWidget
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

class PreviewComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Aperçu")

        main_layout = QVBoxLayout(self)

        self._web_view = QWebEngineView(self)
        self._web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self._web_view.setZoomFactor(0.5)

        web_view_container = StylizableWidget()
        web_view_container.setObjectName("WebView")
        web_view_container.setLayout(QVBoxLayout())
        web_view_container.layout().setContentsMargins(1, 1, 1, 1)
        web_view_container.layout().addWidget(self._web_view)

        main_layout.addWidget(web_view_container)

    def reset(self, analysis: Analysis):
        self._analysis = analysis

        self.update("PDF")

    def update(self, format):

        if format == "PDF":
            html_report_writer = HTMLReportWriter(self._analysis)
            html = html_report_writer.text()
            self._web_view.setHtml(html, QUrl("qrc:/"))
        else:
            html_report_writer = HTMLReportWriter(self._analysis)
            html = ""
            self._web_view.setHtml(html, QUrl("qrc:/"))