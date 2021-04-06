from Services.Writers.ReportWriter import ReportWriter
from Components.Widgets.StylizableWidget import StylizableWidget
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QUrl, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGroupBox, QVBoxLayout

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

    @Slot(ReportWriter)
    def update(self, report_writer: ReportWriter):
        html = report_writer.toHTML()
        self._web_view.setHtml(html, QUrl("qrc:/"))
    