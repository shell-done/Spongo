from PyQt5.QtCore import Qt, QDir, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout

from Models.Parameters import Parameters
from Components.Widgets.PageTitle import PageTitle
from Components.Widgets.StylizedButton import StylizedButton
from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OptionsComponent import OptionsComponent
from Controllers.BaseController import BaseController

class ParametersController(BaseController):
    clickedChangeWidget = pyqtSignal(str)
    clickedChangeToAnalysisWidget = pyqtSignal(Parameters, list)

    def __init__(self):
        super().__init__()

        title = PageTitle("Démarrer une analyse")
        title.backArrowClicked.connect(self._returnClicked)

        self._input_component = InputComponent()
        self._parameters_component = ParametersComponent()
        self._options_component = OptionsComponent()

        self._start_button = StylizedButton("Démarrer", "blue")
        self._start_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.addWidget(self._start_button)

        main_layout = QVBoxLayout()

        main_layout.addWidget(title)
        main_layout.addWidget(self._input_component)
        main_layout.addWidget(self._parameters_component)
        main_layout.addWidget(self._options_component)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button slots
        self._start_button.clicked.connect(self._startClick)

    def start(self):
        self._parameters = Parameters()

        self._input_component.reset(self._parameters)
        self._parameters_component.reset(self._parameters)
        self._options_component.reset(self._parameters)

    @pyqtSlot()
    def _returnClicked(self):
        self.clickedChangeWidget.emit("MENU")

    @pyqtSlot()
    def _startClick(self):
        self._parameters_component.updateParameters(self._parameters)
        self._input_component.updateParameters(self._parameters)
        self._options_component.updateParameters(self._parameters)

        error = self._parameters.checkValidity()
        if error is None:
            images = QDir(self._parameters.srcFolder()).entryList(["*.jpg", "*.jpeg"], filters = QDir.Files)

            if len(images) == 0:
                error = "Le dossier source ne contient aucune image au format .jpg"

        if error is None:
            self.clickedChangeToAnalysisWidget.emit(self._parameters, images)
        else:
            QMessageBox.warning(self, "Erreur", error)
