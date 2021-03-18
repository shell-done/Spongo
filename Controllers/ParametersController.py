from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re

from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OutputComponent import OutputComponent

from Models.Parameters import Parameters

class ErrorDialog(QDialog):
    def __init__(self, message = "Un champ n'est pas correctement rempli", parent = None):
        super().__init__(parent = parent)

        self.setWindowTitle("Erreur !")

        messageLabel = QLabel(message)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(messageLabel)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

class ParametersController(QWidget):
    clickedChangeWidget = pyqtSignal(str)
    clickedChangeToAnalyseWidget = pyqtSignal(Parameters, list)

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

        self._returnButton = QPushButton("Retour")
        self._startButton = QPushButton("Démarrer")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._returnButton)
        buttonLayout.addWidget(self._startButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(title)
        mainLayout.addWidget(self._inputComponent)
        mainLayout.addWidget(self._parametersComponent)
        mainLayout.addWidget(self._outputComponent)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

        # Button slots
        self._returnButton.clicked.connect(self.returnClick)
        self._startButton.clicked.connect(self.startClick)

    @pyqtSlot()
    def returnClick(self):
        self.clickedChangeWidget.emit("MENU")

    @pyqtSlot()
    def startClick(self):
        self._parametersComponent.updateParameters(self._parameters)
        self._inputComponent.updateParameters(self._parameters)
        self._outputComponent.updateParameters(self._parameters)

        directory = QDir(self._parameters.srcFolder())
        print(self._parameters.srcFolder())
        images = directory.entryList(["*.jpg"], filters = QDir.Files)

        if len(images) == 0:
            error_dialog = ErrorDialog("Aucune image n'a été chargé !")
            error_dialog.exec_()
        else:
            self.clickedChangeToAnalyseWidget.emit(self._parameters, images)

