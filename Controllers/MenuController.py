from Services.AppInfo import AppInfo
from Services.Loader import Loader
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QBoxLayout, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QSpacerItem, QVBoxLayout

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

        center_layout = QGridLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setVerticalSpacing(24)
        center_layout.setHorizontalSpacing(30)

        center_layout.addWidget(title, 0, 0, 1, 2)
        center_layout.addWidget(subtitle, 1, 0, 1, 2)
        center_layout.addWidget(start_button, 2, 0, 1, 2)
        center_layout.addWidget(self._history_button, 3, 0, 1, 2)
        center_layout.addWidget(about_button, 4, 0)
        center_layout.addWidget(exit_button, 4, 1)
        center_layout.addItem(QSpacerItem(0, 40), 5, 0)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 11, 0, 5)

        left_layout = QVBoxLayout()
        version_label = QLabel(AppInfo.version())
        version_label.setObjectName("version")
        left_layout.addWidget(version_label, alignment=Qt.AlignBottom)

        right_layout = QVBoxLayout()

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(center_layout, 3)
        main_layout.addLayout(right_layout, 1)

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