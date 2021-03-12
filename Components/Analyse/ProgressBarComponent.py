import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

class ProgressBarComponent(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        self.progressBar = QProgressBar()
        self.mainLayout.addWidget(self.progressBar)

        self.setLayout(self.mainLayout)
    
    def setMaximum(self, max):
        self.progressBar.setMaximum(max)
    
    def update(self, value):
        self.progressBar.setValue(value)


