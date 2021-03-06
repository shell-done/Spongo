from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QGroupBox, QVBoxLayout
from PySide2.QtWebEngineWidgets import QWebEngineView

from Models.Analysis import Analysis
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from Components.Widgets.StylizableWidget import StylizableWidget

class ReportComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Rapport d'analyse")

        main_layout = QVBoxLayout(self)

        self._web_view = QWebEngineView(self)
        self._web_view.setContextMenuPolicy(Qt.NoContextMenu)

        web_view_container = StylizableWidget()
        web_view_container.setObjectName("WebView")
        web_view_container.setLayout(QVBoxLayout())
        web_view_container.layout().setContentsMargins(1, 1, 1, 1)
        web_view_container.layout().addWidget(self._web_view)

        main_layout.addWidget(web_view_container)

    def reset(self, analysis: Analysis):
        if analysis is None:
            self._web_view.setHtml("<html></html>", QUrl("qrc:/"))
            return

        html_report_writer = HTMLReportWriter(analysis)
        html = html_report_writer.text()
        self._web_view.setHtml(html, QUrl("qrc:/"))
        self._web_view.setZoomFactor(1)
