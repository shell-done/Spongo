import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.AnalyseThread import AnalyseThread

class ImageComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Dernière détection")
        titleLabel.setFont(QFont('Times', 15))

        self.imageLabel = QLabel("Image loading...")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.statLabel = QLabel("Stats loading...")
        self.statLabel.setAlignment(QtCore.Qt.AlignCenter)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.imageLabel)
        hLayout.addWidget(self.statLabel)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.imageLabel)

        self.setLayout(mainLayout)

    def update(self, image, sponges):
        pixmap = QPixmap("data/predictions/" + image)
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size()))

        self.statLabel.setText("")
        for key, value in sponges.items():
            self.statLabel.setText(self.statLabel.text() + key + " : " + str(value) + "\n")


