from PyQt5.QtGui import QRegExpValidator
from Services.Loader import Loader
from PyQt5.QtCore import QPoint, QRegExp, QStandardPaths, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QSizePolicy, QHBoxLayout, QLineEdit, QPushButton, QToolTip

from Models.Parameters import Parameters

class InputComponent(QGroupBox):
    analysisNameStateChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setTitle("Entrée")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout = QFormLayout(self)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(14)

        self._name_text = QLineEdit()
        self._name_validator = QRegExpValidator(QRegExp("[a-zA-Z0-9_-éèêëàîï ]{5,30}"))
        self._name_text.setValidator(self._name_validator)
        self._name_text.inputRejected.connect(self._analysisNameError)
        self._name_text.textChanged.connect(self._analysisNameChanged)
        main_layout.addRow("Nom de l'analyse :", self._name_text)

        self._filepath_text = QLineEdit()
        self._filepath_button = QPushButton(" Parcourir... ")
        
        filepath_layout = QHBoxLayout()
        filepath_layout.setSpacing(8)
        filepath_layout.addWidget(self._filepath_text)
        filepath_layout.addWidget(self._filepath_button)

        main_layout.addRow("Dossier d'images à analyser :", filepath_layout)

        self.setLayout(main_layout)

        # Button slots
        self._filepath_button.clicked.connect(self.filepathBrowse)

    def reset(self, parameters: Parameters):
        self._name_text.setText(parameters.name())
        self._filepath_text.setText(parameters.srcFolder())

    def updateParameters(self, parameters: Parameters):
        parameters.setName(self._name_text.text())
        parameters.setSrcFolder(self._filepath_text.text())

    @pyqtSlot(str)
    def _analysisNameChanged(self, text: str):
        self.analysisNameStateChanged.emit(self._name_text.hasAcceptableInput())

    @pyqtSlot()
    def _analysisNameError(self):
        text = "Caractères autorisés : alphanumérique, espace, - et _\nLongueur maximale : 30 caractères"
        QToolTip.showText(self._name_text.mapToGlobal(QPoint()) + self._name_text.cursorRect().topLeft(), text, self)

    @pyqtSlot()
    def filepathBrowse(self):
        path = None

        if Loader.isDevMode():
            path = "./data/images"
        else:
            img_dir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", img_dir)
    
        self._filepath_text.setText(path)