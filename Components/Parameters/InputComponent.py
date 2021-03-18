import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

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
        #self.path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        self.path = "./data/images"
    
        self._filepathText.setText(self.path)

    def setDefaultValues(self, parameters):
        self._nameText.setText(parameters.name())
        self._filepathText.setText(parameters.srcFolder())

    def updateParameters(self, parameters):
        parameters.setName(self._nameText.text())
        parameters.setSrcFolder(self._filepathText.text())

