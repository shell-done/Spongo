from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QListWidget, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ReportListComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Rapports disponibles")

        main_layout = QVBoxLayout(self)
        self._list = QListWidget()
        main_layout.addWidget(self._list)

    def reset(self):
        self._list.addItem("Item 1")
        self._list.addItem("Item 2")
        self._list.addItem("Item 3")