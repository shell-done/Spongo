from Services.AppInfo import AppInfo
from Services.Loader import Loader
from PySide2.QtCore import QStandardPaths, Slot
from PySide2.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QSizePolicy, QCheckBox, QLineEdit, QPushButton, QHBoxLayout

from Models.Parameters import Parameters

class OptionsComponent(QGroupBox):

    def __init__(self):
        super().__init__()
        
        self.setTitle("Options")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout = QFormLayout(self)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(14)

        self._save_cbox = QCheckBox()
        main_layout.addRow("Sauvegarder les images avec les boîtes de détection :", self._save_cbox)

        self._filepath_text = QLineEdit()
        self._filepath_button = QPushButton(" Parcourir... ")
        
        filepath_layout = QHBoxLayout()
        filepath_layout.setSpacing(8)
        filepath_layout.addWidget(self._filepath_text)
        filepath_layout.addWidget(self._filepath_button)

        main_layout.addRow("Dossier de destination des images avec les boîtes de détection :", filepath_layout)

        self.setLayout(main_layout)

        # Button slots
        self._save_cbox.toggled.connect(self._saveCBoxToggled)
        self._filepath_button.clicked.connect(self._filepathClick)

    def reset(self, parameters: Parameters):
        self._save_cbox.setChecked(parameters.saveProcessedImages())
        self._saveCBoxToggled(parameters.saveProcessedImages())
        self._filepath_text.setText(parameters.destFolder())

    def updateParameters(self, parameters: Parameters):
        parameters.setSaveProcessedImages(self._save_cbox.isChecked())
        parameters.setDestFolder(self._filepath_text.text())

    @Slot(bool)
    def _saveCBoxToggled(self, checked: bool):
        self._filepath_text.setEnabled(checked)
        self._filepath_button.setEnabled(checked)

    @Slot()
    def _filepathClick(self):
        path = None

        if AppInfo.isDevMode():
            path = "./data/predictions"
        else:
            img_dir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", img_dir)
        
        self._filepath_text.setText(path)

