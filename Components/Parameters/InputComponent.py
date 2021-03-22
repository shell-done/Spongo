from Models.Parameters import Parameters
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class InputComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_label = QLabel("Entrée")
        title_label.setFont(QFont('Times', 15))

        # Name layout
        name_label = QLabel("Nom de l'analyse : ")
        self._nameText = QLineEdit()

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self._nameText)

        # Filepath layout
        filepath_label = QLabel("Dossier d'images à analyser : ")
        self._filepath_text = QLineEdit()
        filepath_button = QPushButton("Charger")

        filepath_layout = QHBoxLayout()
        filepath_layout.addWidget(filepath_label)
        filepath_layout.addWidget(self._filepath_text)
        filepath_layout.addWidget(filepath_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(filepath_layout)

        self.setLayout(main_layout)

        # Button slots
        filepath_button.clicked.connect(self.filepathClick)

    def reset(self, parameters: Parameters):
        self._nameText.setText(parameters.name())
        self._filepath_text.setText(parameters.srcFolder())

    def updateParameters(self, parameters: Parameters):
        parameters.setName(self._nameText.text())
        parameters.setSrcFolder(self._filepath_text.text())

    @pyqtSlot()
    def filepathClick(self):
        #dialog = QFileDialog()
        #path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        path = "./data/images"
    
        self._filepath_text.setText(path)