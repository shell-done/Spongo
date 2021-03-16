import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader
from Models.ProcessedImage import ProcessedImage
from Services.AnalyseThread import AnalyseThread

class ImageComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Dernière détection")
        titleLabel.setFont(QFont('Times', 15))

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # self.filenameLabel = QLabel("Aucune image")
        # self.filenameLabel.setAlignment(QtCore.Qt.AlignCenter)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.imageLabel)
        # vLayout.addWidget(self.filenameLabel)

        self.statLabel = QLabel()
        self.statLabel.setAlignment(QtCore.Qt.AlignCenter)

        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.addWidget(self.statLabel)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)

        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.imageLabel)

        self.setLayout(mainLayout)
        self.reset()

    def update(self, processed_image: ProcessedImage):
        pixmap = QPixmap(processed_image.hightlightedImage())
        
        detections_count = processed_image.detectionsCount()
        text = ""
        
        for class_id, class_name in Loader.SpongesClasses().items():
            text += "%s : %d\n" % (class_name, detections_count.get(class_id, 0))

        scaled = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(scaled)

        # self.filenameLabel.setText(processed_image.filePath())
        self.statLabel.setText(text)

    def reset(self):
        self.imageLabel.setText("Image loading...")
        # self.filenameLabel.setText("Aucune image")
        self.statLabel.setText("Stats loading...")