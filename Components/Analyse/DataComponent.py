import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.AnalyseThread import AnalyseThread

class DataComponent(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        self.label = QLabel("Data sur les éponges")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        font = QFont("Arial", 10)
        self.label.setFont(font)
        self.mainLayout.addWidget(self.label)

        self.setLayout(self.mainLayout)

    def update(self, sponges):
        self.label.setText("")

        for key, value in sponges.items():
            self.label.setText(self.label.text() + key + " : " + str(value) + "\n")


