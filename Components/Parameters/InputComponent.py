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
        nameText = QTextEdit()

        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(nameText)

        # Filepath layout
        filepathLabel = QLabel("Dossier d'images à analyser : ")
        filepathText = QTextEdit()

        filepathLayout = QHBoxLayout()
        filepathLayout.addWidget(filepathLabel)
        filepathLayout.addWidget(filepathText)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(filepathLayout)

        self.setLayout(mainLayout)


