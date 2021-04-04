from Components.Widgets.StylizableWidget import StylizableWidget
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

class ReportComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Rapport d'analyse")

        main_layout = QVBoxLayout(self)

        self._web_view = QWebEngineView(self)
        self._web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self._web_view.setZoomFactor(1)

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