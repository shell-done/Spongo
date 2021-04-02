from Services.HistoryManager import HistoryManager
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ReportListComponent(QGroupBox):
    currentAnalysisChanged = pyqtSignal(Analysis)

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
            item = QListWidgetItem("%s (%s)" % (analysis["name"], analysis["date"]))
            item.setData(Qt.UserRole, analysis["file"])
            self._list.addItem(item)
        
        self._list.setCurrentRow(0)

    @pyqtSlot(int)
    def _currentAnalysisChanged(self, row: int):
        if row < 0:
            return
        
        new_analysis_file = self._list.item(row).data(Qt.UserRole)

        if self._current_analysis_file == new_analysis_file:
            return

        if self._current_analysis_file is None:
            self._current_analysis_file = new_analysis_file
            return

        self._current_analysis_file = new_analysis_file
        self.currentAnalysisChanged.emit(HistoryManager.loadAnalysis(new_analysis_file))