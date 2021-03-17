from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OutputComponent import OutputComponent

from Models.Parameters import Parameters

class ParametersController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self._parameters = Parameters()

        title = QLabel("Démarrer une analyse")
        title.setFont(QFont("Arial", 20))
        
        self._inputComponent = InputComponent()
        self._inputComponent.setDefaultValues(self._parameters)
        self._parametersComponent = ParametersComponent()
        self._parametersComponent.setDefaultValues(self._parameters)
        self._outputComponent = OutputComponent()
        self._outputComponent.setDefaultValues(self._parameters)

        self._startButton = QPushButton("Démarrer")

        mainLayout = QVBoxLayout()
        
        mainLayout.addWidget(title)
        mainLayout.addWidget(self._inputComponent)
        mainLayout.addWidget(self._parametersComponent)
        mainLayout.addWidget(self._outputComponent)
        mainLayout.addWidget(self._startButton)

        self.setLayout(mainLayout)

        # Button slots
        self._startButton.clicked.connect(self.startClick)

    @pyqtSlot()
    def startClick(self):
        self._parametersComponent.updateParameters(self._parameters)
        self._inputComponent.updateParameters(self._parameters)
        self._outputComponent.updateParameters(self._parameters)

        directory = QDir(self._parameters.srcFolder())
        images = self.directory.entryList(["*.jpg"], filters = QDir.Files)

        # self.clickedChangeWidget.emit("ANALYSE", self._parameters, images)

