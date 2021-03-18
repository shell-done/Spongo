import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)
from PyQt5.QtWinExtras import QWinTaskbarButton

class ProgressComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Progression")
        titleLabel.setFont(QFont('Times', 15))

        self._max_value = 1
        self._taskbar_button = None

        self.currentImageLabel = QLabel()
        self.timeLabel = QLabel()
        self.nextImageLabel = QLabel()

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
        self.reset()
    
    def setMaximum(self, max_value: int):
        self._max_value = max_value
        self.progressBar.setMaximum(self._max_value)
    
    def update(self, next_image: str, value: int, time_left: QTime):
        self.progressBar.setValue(value)
        self.currentImageLabel.setText("Image : " + str(value) + "/" + str(self._max_value))

        time_left_str = ""
        if time_left is None:
            time_left_str = "Estimation..."
        else:
            time_left_str = "%dh %dm %ds" % (time_left.hour(), time_left.minute(), time_left.second())

        self.timeLabel.setText("Temps restant : " + time_left_str)
        self.nextImageLabel.setText("Prochaine image : " + next_image)

        if self._taskbar_button is not None:
            self._taskbar_button.progress().setVisible(True)
            self._taskbar_button.progress().setRange(0, self._max_value)
            self._taskbar_button.progress().setValue(value)

    def initWinTaskbarProgress(self):
        window = self.window().windowHandle()
        if window is None:
            self._taskbar_button = None
        
        self._taskbar_button = QWinTaskbarButton(self)
        self._taskbar_button.setWindow(window)

    def reset(self):
        self.progressBar.setValue(0)
        self.currentImageLabel.setText("Image : 0/0")
        self.timeLabel.setText("Temps restant : ")
        self.nextImageLabel.setText("Prochaine image : ")


