import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtChart
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from Services.Loader import Loader
from Services.AnalyseThread import AnalyseThread

class StatComponent(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        title = QLabel("Statistiques")
        title.setFont(QFont('Times', 15))

        self.totalLabel = QLabel("Éponges détectées : ")

        self.spongesLabel = QLabel("Aucune éponge détectée")
        self.spongesLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.chartview =  QChartView()
        self.create_linechart()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.totalLabel)
        mainLayout.addWidget(self.spongesLabel)
        mainLayout.addWidget(self.chartview)

        self.setLayout(mainLayout)

    def create_linechart(self):
 
        self.series = QLineSeries(self)

        self.chart = QChart()

        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Line Chart Example")
 
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
 
        self.chartview = QChartView(self.chart)

    def update(self, detected_sponges: dict[int, int]):
        text = ""
        total = 0
        cpt = 2

        for class_id, class_name in Loader.SpongesClasses().items():
            text += "%s : %d\n" % (class_name, detected_sponges[class_id])
            total += detected_sponges[class_id]

        self.totalLabel.setText("Éponges détectées : " + str(total))
        self.spongesLabel.setText(text)

        self.series.append(cpt, cpt)
        cpt += 1

    def reset(self):
        text = ""
        total = 0

        self.totalLabel.setText("Éponges détectées : 0")
        self.spongesLabel.setText("Aucune éponge détectée")
        self.series.remove()