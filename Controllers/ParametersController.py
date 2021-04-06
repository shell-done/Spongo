from PySide2.QtCore import Qt, QDir, Signal, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout

from Models.Parameters import Parameters
from Components.Widgets.PageTitle import PageTitle
from Components.Widgets.StylizedButton import StylizedButton
from Components.Parameters.InputComponent import InputComponent
from Components.Parameters.ParametersComponent import ParametersComponent
from Components.Parameters.OptionsComponent import OptionsComponent
from Controllers.BaseController import BaseController

class ParametersController(BaseController):

    def __init__(self):
        super().__init__()

        title = PageTitle("Démarrer une analyse")
        title.backArrowClicked.connect(self._returnClicked)

        self._input_component = InputComponent()
        self._parameters_component = ParametersComponent()
        self._options_component = OptionsComponent()

        self._input_component.analysisNameStateChanged.connect(self._analysisNameStateChanged)

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

    @Slot(bool)
    def _analysisNameStateChanged(self, ok: bool):
        self._start_button.setEnabled(ok)

    @Slot()
    def _returnClicked(self):
        self.changeWidget.emit("/menu", None)

    @Slot()
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
            self.changeWidget.emit("/analysis", (self._parameters, images))
        else:
            QMessageBox.warning(self, "Erreur", error)
