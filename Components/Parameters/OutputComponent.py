from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from Models.Parameters import Parameters

class OutputComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_tabel = QLabel("Sortie")
        title_tabel.setFont(QFont('Times', 15))

        # Save layout
        save_label = QLabel("Sauvegarder les images avec les boîtes de détection : ")
        self._saveCBox = QCheckBox()
        self._saveCBox.toggled.connect(self._saveCBoxToggled)

        save_layout = QHBoxLayout()
        save_layout.addWidget(save_label)
        save_layout.addWidget(self._saveCBox)

        # Filepath layout
        filepath_label = QLabel("Dossier de destination des images avec les boîtes de détection : ")
        self._filepath_text = QLineEdit()
        self._filepath_button = QPushButton("Charger")

        filepath_layout = QHBoxLayout()
        filepath_layout.addWidget(filepath_label)
        filepath_layout.addWidget(self._filepath_text)
        filepath_layout.addWidget(self._filepath_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_tabel)
        main_layout.addLayout(save_layout)
        main_layout.addLayout(filepath_layout)

        self.setLayout(main_layout)

        # Button slots
        self._filepath_button.clicked.connect(self._filepathClick)

    def reset(self, parameters: Parameters):
        self._saveCBox.setChecked(parameters.saveProcessedImages())
        self._saveCBoxToggled(parameters.saveProcessedImages())
        self._filepath_text.setText(parameters.destFolder())

    def updateParameters(self, parameters: Parameters):
        parameters.setSaveProcessedImages(self._saveCBox.isChecked())
        parameters.setDestFolder(self._filepath_text.text())

    @pyqtSlot(bool)
    def _saveCBoxToggled(self, checked: bool):
        self._filepath_text.setEnabled(checked)
        self._filepath_button.setEnabled(checked)

    @pyqtSlot()
    def _filepathClick(self):
        #dialog = QFileDialog()
        #path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        path = "./data/predictions"
        
        self._filepath_text.setText(path)

