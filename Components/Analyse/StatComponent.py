import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.AnalyseThread import AnalyseThread

class StatComponent(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        title = QLabel("Statistiques")
        title.setFont(QFont('Times', 15))

        self.label = QLabel("Stats sur les éponges")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.label)

        self.setLayout(mainLayout)

    def update(self, sponges):
        self.label.setText("")

        for key, value in sponges.items():
            self.label.setText(self.label.text() + key + " : " + str(value) + "\n")


