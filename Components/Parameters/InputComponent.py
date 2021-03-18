from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class InputComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Entrée")
        titleLabel.setFont(QFont('Times', 15))

        # Name layout
        nameLabel = QLabel("Nom de l'analyse : ")
        self._nameText = QLineEdit()

        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self._nameText)

        # Filepath layout
        filepathLabel = QLabel("Dossier d'images à analyser : ")
        self._filepathText = QLineEdit()
        filepathButton = QPushButton("Charger")

        filepathLayout = QHBoxLayout()
        filepathLayout.addWidget(filepathLabel)
        filepathLayout.addWidget(self._filepathText)
        filepathLayout.addWidget(filepathButton)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(filepathLayout)

        self.setLayout(mainLayout)

        # Button slots
        filepathButton.clicked.connect(self.filepathClick)

    @pyqtSlot()
    def filepathClick(self):
        #dialog = QFileDialog()
        #path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        path = "./data/images"
    
        self._filepathText.setText(path)

    def setDefaultValues(self, parameters):
        self._nameText.setText(parameters.name())
        self._filepathText.setText(parameters.srcFolder())

    def updateParameters(self, parameters):
        parameters.setName(self._nameText.text())
        parameters.setSrcFolder(self._filepathText.text())

