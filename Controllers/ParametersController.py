from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Components.Parameters.InputComponent import InputComponent
# from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OutputComponent import OutputComponent

class ParametersController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        title = QLabel("Démarrer une analyse")
        title.setFont(QFont("Arial", 20))
        
        self.inputComponent = InputComponent()
        self.outputComponent = OutputComponent()

        self.startButton = QPushButton("Démarrer")

        mainLayout = QVBoxLayout()
        
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.inputComponent)
        mainLayout.addWidget(self.outputComponent)
        mainLayout.addWidget(self.startButton)

        self.setLayout(mainLayout)

        # Button slots
