import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader
from Services.AnalyseThread import AnalyseThread

class StatComponent(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        self.total = []

        title = QLabel("Statistiques")
        title.setFont(QFont('Times', 15))

        self.label = QLabel("Stats sur les éponges")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.label)
        self.setLayout(mainLayout)

    def update(self, detected_sponges: dict[int, int]):
        text = ""

        for class_id, class_name in Loader.SpongesClasses().items():
            text += "%s : %d\n" % (class_name, detected_sponges[class_id])

        print("\n")

        # if self.total == []:
        #     for i in range(len(sponges)):
        #         self.total.append(0)

        # for key, value in sponges.items():
        #     index = list(sponges.keys()).index(key)
        #     self.total[index] += value

        #     self.label.setText(self.label.text() + key + " : " + str(self.total[index]) + "\n")
