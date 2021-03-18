from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController
from Controllers.Dialogs.ErrorDialog import ErrorDialog
from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OutputComponent import OutputComponent

class ParametersController(BaseController):
    clickedChangeWidget = pyqtSignal(str)
    clickedChangeToAnalysisWidget = pyqtSignal(Parameters, list)

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

        src_dir = self._parameters.srcFolder()
        images = QDir(src_dir).entryList(["*.jpg"], filters = QDir.Files)

        dest_dir = self._parameters.destFolder()

        morphotypes_selected = 0
        morphotypes = self._parameters.morphotypes()
        for k, v in morphotypes.items():
            if v == True:
                morphotypes_selected += 1

        if src_dir == "":
            self.createErrorDialog("Vous n'avez pas sélectionné de dossier source")
        elif len(images) == 0:
            self.createErrorDialog("Le dossier source ne contient aucune image au format .jpg")
        elif morphotypes_selected == 0:
            self.createErrorDialog("Aucun morphotype n'a été sélectionné")
        elif dest_dir == "":
            self.createErrorDialog("Vous n'avez pas sélectionné de dossier destination")
        else:
            self.clickedChangeToAnalysisWidget.emit(self._parameters, images)

    def createErrorDialog(self, message):
        error_dialog = ErrorDialog(message)
        error_dialog.exec_()