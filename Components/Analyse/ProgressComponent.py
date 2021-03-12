import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

class ProgressComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Progression")
        titleLabel.setFont(QFont('Times', 15))

        self.currentImageLabel = QLabel("Image : 0/0")
        self.timeLabel = QLabel("Temps restant : ")
        self.nextImageLabel = QLabel("Prochaine image : ")


        infoLayout = QHBoxLayout()
        infoLayout.addWidget(self.currentImageLabel)
        infoLayout.addWidget(self.timeLabel)
        infoLayout.addWidget(self.nextImageLabel)

        self.progressBar = QProgressBar()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(infoLayout)
        mainLayout.addWidget(self.progressBar)

        self.setLayout(mainLayout)
    
    def setMaximum(self, max: int):
        self.maxValue = max
        self.progressBar.setMaximum(self.maxValue)
    
    def update(self, next_image: str, value: int):
        self.progressBar.setValue(value)
        self.currentImageLabel.setText("Image : " + str(value) + "/" + str(self.maxValue))
        self.nextImageLabel.setText("Prochaine image : " + next_image)

    # def minimumSizeHint(self):
    #     return QSize(100, 600)


