from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController

class MenuController(BaseController):
    clickedChangeWidget = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Main Layout
        title = QLabel("Spongo")
        title.setAlignment(Qt.AlignCenter)

        self.paramsButton = QPushButton("Commencer une analyse")

        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)
        mainLayout.setSpacing(100)
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.paramsButton)

        self.setLayout(mainLayout)

        # Button slots
        self.paramsButton.clicked.connect(self.paramsClick)

    @pyqtSlot()
    def paramsClick(self):
        self.clickedChangeWidget.emit("PARAMETERS")