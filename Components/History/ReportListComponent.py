from Services.HistoryManager import HistoryManager
from Services.Writers.HTMLReportWriter import HTMLReportWriter
from PySide2.QtWebEngineWidgets import QWebEngineView
from Models.Analysis import Analysis
from PySide2.QtCore import QPoint, QRegExp, Qt, QUrl, Signal, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGroupBox, QInputDialog, QListWidget, QListWidgetItem, QMenu, QMessageBox, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ReportListComponent(QGroupBox):
    currentAnalysisChanged = Signal(object)

    def __init__(self):
        super().__init__()

        self.setTitle("Rapports disponibles")

        main_layout = QVBoxLayout(self)
        self._list = QListWidget()
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._showItemMenu)
        self._list.currentRowChanged.connect(self._currentAnalysisChanged)
        self._list.itemDoubleClicked.connect(lambda item: self._renameItem())

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

    @Slot(int)
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

    @Slot(QPoint)
    def _showItemMenu(self, pos: QPoint):
        globalPos = self._list.mapToGlobal(pos)

        actions_menu = QMenu()
        actions_menu.addAction("Renommer", self._renameItem)
        actions_menu.addAction("Supprimer",  self._eraseItem)

        actions_menu.exec_(globalPos)

    @Slot()
    def _renameItem(self):
        item = self._list.currentItem()
        
        input_dialog = QInputDialog(self.parentWidget(), Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        font = input_dialog.font()
        font.setPixelSize(16)
        input_dialog.setFont(font)
        input_dialog.setMinimumWidth(300)
        input_dialog.setInputMode(QInputDialog.TextInput)
        input_dialog.setWindowTitle("Renommer l'analyse")
        input_dialog.setLabelText("Nouveau nom pour '%s' :" % item.data(Qt.UserRole + 1))
        input_dialog.setTextValue(item.data(Qt.UserRole + 1))
        input_dialog.setOkButtonText("OK")
        input_dialog.setCancelButtonText("Annuler")

        if not input_dialog.exec_():
            return
        
        new_name = input_dialog.textValue()

        if self._analysis is None:
            return

        if new_name == self._analysis.parameters().name():
            return
        
        regexp = QRegExp("^[a-zA-Z0-9_-#éèêëàîï ]{5,30}$")
        
        if not regexp.exactMatch(new_name):
            QMessageBox.warning(self, "Nouveau nom invalide", "Caractères autorisés : alphanumérique, espace, #, - et _ avec une longueur maximale de 30 caractères")
            return


        self._analysis.parameters().setName(new_name)
        HistoryManager.renameAnalysis(item.data(Qt.UserRole), self._analysis)
        
        current_row = self._list.currentRow()
        self.reset(self._analysis)
        self._list.setCurrentRow(current_row)
        self.currentAnalysisChanged.emit(self._analysis)

    @Slot()
    def _eraseItem(self):
        item = self._list.currentItem()

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("Supprimer une analyse ?")
        message_box.setText("Voulez vous vraiment supprimer l'analyse '%s' de façon définitive ?" % item.data(Qt.UserRole + 1))
        message_box.setInformativeText("Assurez vous d'avoir exportez toutes les données dont vous avez besoin.")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        ret = message_box.exec_()
        if ret == QMessageBox.Yes:
            HistoryManager.deleteAnalysis(item.data(Qt.UserRole))
            self._list.takeItem(self._list.currentRow())

        if self._list.currentRow() == -1:
            self.currentAnalysisChanged.emit(None)
