from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QBoxLayout, QGridLayout, QLabel, QMessageBox, QVBoxLayout

from Services.HistoryManager import HistoryManager
from Controllers.BaseController import BaseController
from Components.Widgets.StylizedButton import StylizedButton

class MenuController(BaseController):

    def __init__(self):
        super().__init__()

        # Main Layout
        title = QLabel("Sp<font color='#419DD1'>o</font>ng<font color='#F4D05C'>o</font>")
        title.setObjectName("title")

        subtitle = QLabel("Outil de classification et de reconnaissance de morphotypes d’éponges marines")
        subtitle.setObjectName("subtitle")

        start_button = StylizedButton("Commencer une analyse", "blue")
        self._history_button = StylizedButton("Historique des analyses", "blue")
        about_button = StylizedButton("À propos", "blue")
        exit_button = StylizedButton("Quitter", "yellow")

        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setVerticalSpacing(24)
        main_layout.setHorizontalSpacing(30)

        main_layout.addWidget(title, 0, 0, 1, 2)
        main_layout.addWidget(subtitle, 1, 0, 1, 2)
        main_layout.addWidget(start_button, 2, 0, 1, 2)
        main_layout.addWidget(self._history_button, 3, 0, 1, 2)
        main_layout.addWidget(about_button, 4, 0)
        main_layout.addWidget(exit_button, 4, 1)

        self.setLayout(main_layout)

        # Button slots
        start_button.clicked.connect(self._startButtonClicked)
        self._history_button.clicked.connect(self._historyButtonClicked)
        about_button.clicked.connect(self._aboutButtonClicked)
        exit_button.clicked.connect(self._exitButtonClicked)

    def start(self):
        self._history_button.setEnabled(HistoryManager.hasAnalysis())

    @pyqtSlot()
    def _startButtonClicked(self):
        self.changeWidget.emit("/parameters")

    @pyqtSlot()
    def _historyButtonClicked(self):
        last_analysis = HistoryManager.loadLastAnalysis()
        self.changeWidget[str, object].emit("/history", last_analysis)

    @pyqtSlot()
    def _aboutButtonClicked(self):
        QMessageBox.aboutQt(self, "About qt")

    @pyqtSlot()
    def _exitButtonClicked(self):
        QApplication.exit(0)