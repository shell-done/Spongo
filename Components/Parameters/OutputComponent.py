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

        titleLabel = QLabel("Entrée")
        titleLabel.setFont(QFont('Times', 15))

        # Save layout
        saveLabel = QLabel("Sauvegarder les images avec les boîtes de détection : ")
        saveCBox = QCheckBox()

        saveLayout = QHBoxLayout()
        saveLayout.addWidget(saveLabel)
        saveLayout.addWidget(saveCBox)

        # Filepath layout
        filepathLabel = QLabel("Dossier de destination des images avec les boîtes de détection : ")
        filepathText = QTextEdit()

        filepathLayout = QHBoxLayout()
        filepathLayout.addWidget(filepathLabel)
        filepathLayout.addWidget(filepathText)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(saveLayout)
        mainLayout.addLayout(filepathLayout)

        self.setLayout(mainLayout)


