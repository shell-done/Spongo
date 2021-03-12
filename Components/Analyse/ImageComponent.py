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

        self.mainLayout = QVBoxLayout()

        self.label = QLabel("Lancement de l'analyse...")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.label)

        self.setLayout(self.mainLayout)

    def update(self, image):
        pixmap = QPixmap("data/predictions/" + image)
        self.label.setPixmap(pixmap.scaled(self.label.size()))


