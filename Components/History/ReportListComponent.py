from Services.HistoryManager import HistoryManager
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PyQt5.QtCore import QPoint, QRegExp, Qt, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QInputDialog, QListWidget, QListWidgetItem, QMenu, QMessageBox, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ReportListComponent(QGroupBox):
    currentAnalysisChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.setTitle("Rapports disponibles")

        main_layout = QVBoxLayout(self)
        self._list = QListWidget()
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._showItemMenu)
        self._list.currentRowChanged.connect(self._currentAnalysisChanged)

        self._analysis = None

        main_layout.addWidget(self._list)

    def reset(self, analysis: Analysis):
        self._current_analysis_file = None
        self._analysis = analysis

        self._list.clear()
        for analysis in HistoryManager.analysisList():
            item = QListWidgetItem("%s (%s)" % (analysis["name"], analysis["date"]))
            item.setData(Qt.UserRole, analysis["file"])
            item.setData(Qt.UserRole + 1, analysis["name"])
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
        self._analysis = HistoryManager.loadAnalysis(new_analysis_file)
        self.currentAnalysisChanged.emit(self._analysis)

    @pyqtSlot(QPoint)
    def _showItemMenu(self, pos: QPoint):
        globalPos = self._list.mapToGlobal(pos)

        actions_menu = QMenu()
        actions_menu.addAction("Renommer", self._renameItem)
        actions_menu.addAction("Supprimer",  self._eraseItem)

        actions_menu.exec(globalPos)

    @pyqtSlot()
    def _renameItem(self):
        item = self._list.currentItem()
        
        new_name, ok = QInputDialog.getText(self, "Renommer l'analyse", "Nouveau nom pour '%s' :" % item.data(Qt.UserRole + 1), text=item.data(Qt.UserRole + 1))
        if not ok or self._analysis is None:
            return
        
        regexp = QRegExp("^[a-zA-Z0-9_-éèêëàîï ]{5,30}$")
        
        if not regexp.exactMatch(new_name):
            QMessageBox.warning(self, "Nouveau nom invalide", "Caractères autorisés : alphanumérique, espace, - et _ avec une longueur maximale de 30 caractères")
            return


        self._analysis.parameters().setName(new_name)
        HistoryManager.renameAnalysis(item.data(Qt.UserRole), self._analysis)
        
        current_row = self._list.currentRow()
        self.reset(self._analysis)
        self._list.setCurrentRow(current_row)
        self.currentAnalysisChanged.emit(self._analysis)

    @pyqtSlot()
    def _eraseItem(self):
        item = self._list.currentItem()

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("Supprimer une analyse ?")
        message_box.setText("Voulez vous vraiment supprimer l'analyse '%s' de façon définitive ?" % item.data(Qt.UserRole + 1))
        message_box.setInformativeText("Assurez vous d'avoir exportez toutes les données dont vous avez besoin.")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        ret = message_box.exec()
        if ret == QMessageBox.Yes:
            HistoryManager.deleteAnalysis(item.data(Qt.UserRole))
            self._list.takeItem(self._list.currentRow())

        if self._list.currentRow() == -1:
            self.currentAnalysisChanged.emit(None)
