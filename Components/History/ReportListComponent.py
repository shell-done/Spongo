from Services.HistoryManager import HistoryManager
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ReportListComponent(QGroupBox):
    currentAnalysisChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setTitle("Rapports disponibles")

        main_layout = QVBoxLayout(self)
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._currentAnalysisChanged)

        main_layout.addWidget(self._list)

    def reset(self):
        self._current_analysis_file = None

        self._list.clear()
        for analysis in HistoryManager.analysisList():
            item = QListWidgetItem(analysis["name"])
            item.setData(Qt.UserRole, analysis["file"])
            self._list.addItem(item)
        
        self._list.setCurrentRow(0)

    @pyqtSlot(int)
    def _currentAnalysisChanged(self, row: int):
        new_analysis = self._list.item(row).data(Qt.UserRole)

        if self._current_analysis_file == new_analysis:
            return

        if self._current_analysis_file is None:
            self._current_analysis_file = new_analysis
            return

        self._current_analysis_file = new_analysis
        self.currentAnalysisChanged.emit(new_analysis)