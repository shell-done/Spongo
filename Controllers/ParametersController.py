from PyQt5.QtCore import QDir, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController
from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OutputComponent import OutputComponent

class ParametersController(BaseController):
    clickedChangeWidget = pyqtSignal(str)
    clickedChangeToAnalysisWidget = pyqtSignal(Parameters, list)

    def __init__(self):
        super().__init__()

        title = QLabel("Démarrer une analyse")
        title.setFont(QFont("Arial", 20))
        
        self._input_component = InputComponent()
        self._parameters_component = ParametersComponent()
        self._output_component = OutputComponent()

        self._return_button = QPushButton("Retour")
        self._start_button = QPushButton("Démarrer")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self._return_button)
        button_layout.addWidget(self._start_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self._input_component)
        main_layout.addWidget(self._parameters_component)
        main_layout.addWidget(self._output_component)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button slots
        self._return_button.clicked.connect(self._returnClick)
        self._start_button.clicked.connect(self._startClick)

    def start(self):
        self._parameters = Parameters()

        self._input_component.reset(self._parameters)
        self._parameters_component.reset(self._parameters)
        self._output_component.reset(self._parameters)

    @pyqtSlot()
    def _returnClick(self):
        self.clickedChangeWidget.emit("MENU")

    @pyqtSlot()
    def _startClick(self):
        self._parameters_component.updateParameters(self._parameters)
        self._input_component.updateParameters(self._parameters)
        self._output_component.updateParameters(self._parameters)

        src_dir = self._parameters.srcFolder()
        images = QDir(src_dir).entryList(["*.jpg"], filters = QDir.Files)

        dest_dir = self._parameters.destFolder()

        error_message = None
        if src_dir == "":
            error_message = "Vous n'avez pas sélectionné de dossier source"
        elif len(images) == 0:
            error_message = "Le dossier source ne contient aucune image au format .jpg"
        elif not any(self._parameters.morphotypes().values()):
            error_message = "Aucun morphotype n'a été sélectionné"
        elif dest_dir == "" and self._parameters.saveProcessedImages():
            error_message = "Vous n'avez pas sélectionné de dossier destination"
        
        if error_message:
            QMessageBox.warning(self, "Erreur", error_message)
        else:
            self.clickedChangeToAnalysisWidget.emit(self._parameters, images)
