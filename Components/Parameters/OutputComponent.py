import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

class OutputComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Sortie")
        titleLabel.setFont(QFont('Times', 15))

        # Save layout
        saveLabel = QLabel("Sauvegarder les images avec les boîtes de détection : ")
        self._saveCBox = QCheckBox()

        saveLayout = QHBoxLayout()
        saveLayout.addWidget(saveLabel)
        saveLayout.addWidget(self._saveCBox)

        # Filepath layout
        filepathLabel = QLabel("Dossier de destination des images avec les boîtes de détection : ")
        self._filepathText = QLineEdit()
        filepathButton = QPushButton("Charger")

        filepathLayout = QHBoxLayout()
        filepathLayout.addWidget(filepathLabel)
        filepathLayout.addWidget(self._filepathText)
        filepathLayout.addWidget(filepathButton)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(saveLayout)
        mainLayout.addLayout(filepathLayout)

        self.setLayout(mainLayout)

        # Button slots
        filepathButton.clicked.connect(self.filepathClick)

    @pyqtSlot()
    def filepathClick(self):
        #dialog = QFileDialog()
        #path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        path = "./data/predictions"
        
        self._filepathText.setText(path)

    def setDefaultValues(self, parameters):
        self._saveCBox.setChecked(parameters.saveProcessedImages())
        self._filepathText.setText(parameters.destFolder())

    def updateParameters(self, parameters):
        parameters.setSaveProcessedImages(self._saveCBox.isChecked())
        parameters.setDestFolder(self._filepathText.text())


