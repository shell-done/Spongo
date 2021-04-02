from Services.Loader import Loader
from PyQt5.QtCore import QStandardPaths, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QSizePolicy, QHBoxLayout, QLineEdit, QPushButton

from Models.Parameters import Parameters

class InputComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Entrée")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout = QFormLayout(self)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(14)

        self._name_text = QLineEdit()
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

    @pyqtSlot()
    def filepathBrowse(self):
        path = None

        if Loader.isDevMode():
            path = "./data/images"
        else:
            img_dir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", img_dir)
    
        self._filepath_text.setText(path)