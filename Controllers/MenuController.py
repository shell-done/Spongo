from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout

from Services.AppInfo import AppInfo
from Services.HistoryManager import HistoryManager
from Components.Widgets.StylizedButton import StylizedButton
from Controllers.BaseController import BaseController
from Controllers.MessageBox.AboutMessageBox import AboutMessageBox

class MenuController(BaseController):

    def __init__(self):
        super().__init__()

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Sp<font color='#419DD1'>o</font>ng<font color='#F4D05C'>o</font>")
        title.setObjectName("title")

        subtitle = QLabel("Outil de classification et de reconnaissance de morphotypes d’éponges marines")
        subtitle.setObjectName("subtitle")

        start_button = StylizedButton("Commencer une analyse", "blue")
        self._history_button = StylizedButton("Historique des analyses", "blue")
        about_button = StylizedButton("À propos", "blue")
        exit_button = StylizedButton("Quitter", "yellow")

        buttons_layout = QGridLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setVerticalSpacing(24)
        buttons_layout.setHorizontalSpacing(30)

        buttons_layout.addWidget(start_button, 0, 0, 1, 2)
        buttons_layout.addWidget(self._history_button, 1, 0, 1, 2)
        buttons_layout.addWidget(about_button, 2, 0)
        buttons_layout.addWidget(exit_button, 2, 1)

        version_label = QLabel(AppInfo.version())
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setObjectName("version")

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(15, 15, 15, 15)
        center_layout.addStretch(4)
        center_layout.addWidget(title)
        center_layout.addWidget(subtitle)
        center_layout.addLayout(buttons_layout)
        center_layout.addStretch(5)
        center_layout.addWidget(version_label)

        isen_logo = QLabel()
        isen_logo.setPixmap(QPixmap(":/img/isen_logo.png").scaledToWidth(180, Qt.SmoothTransformation))

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(isen_logo, alignment=Qt.AlignBottom)

        ifremer_logo = QLabel()
        ifremer_logo.setAlignment(Qt.AlignRight)
        ifremer_logo.setPixmap(QPixmap(":/img/ifremer_logo.png").scaledToWidth(180, Qt.SmoothTransformation))

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(ifremer_logo, alignment=Qt.AlignBottom)


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

    @Slot()
    def _startButtonClicked(self):
        self.changeWidget.emit("/parameters", None)

    @Slot()
    def _historyButtonClicked(self):
        last_analysis = HistoryManager.loadLastAnalysis()
        self.changeWidget.emit("/history", last_analysis)

    @Slot()
    def _aboutButtonClicked(self):
        AboutMessageBox.show(self)

    @Slot()
    def _exitButtonClicked(self):
        QApplication.exit(0)