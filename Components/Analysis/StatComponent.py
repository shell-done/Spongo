from PyQt5 import QtCore, QtGui, QtChart
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)
from PyQt5.QtChart import QChart, QChartView, QSplineSeries

from Models.Analysis import Analysis
from Services.Loader import Loader
from PyQt5.QtWinExtras import QWinTaskbarButton

class StatComponent(QWidget):

    def __init__(self):
        super().__init__()

        self._series = {}

        title = QLabel("Statistiques")
        title.setFont(QFont('Times', 15))

        self._total_label = QLabel()
        self._sponges_label = QLabel()
        self._sponges_label.setAlignment(QtCore.Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self._total_label)
        main_layout.addWidget(self._sponges_label)
        main_layout.addWidget(self._createLineChart())

        self.setLayout(main_layout)

    def reset(self):
        self._total_label.setText("Éponges détectées : 0")
        self._sponges_label.setText("Aucune éponge détectée")

        self._chart.removeAllSeries()
        for i,n in Loader.SpongesClasses().items():
            self._series[i] = QSplineSeries(self)
            self._series[i].setName(n)
            self._series[i].pen().setWidth(2)
            self._series[i].append(0, 0)
            self._chart.addSeries(self._series[i])

        self._chart.createDefaultAxes()
        self._chart.axisX().setRange(0, 1)
        self._chart.axisY().setRange(0, 1)

    def _createLineChart(self) -> QChartView:
        self._chart = QChart()
        
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self._chart.setTitle("Détection cumulées")
 
        self._chart.legend().setVisible(True)
        self._chart.legend().setAlignment(Qt.AlignBottom)
 
        chart_view = QChartView(self._chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def update(self, analysis: Analysis):
        text = ""
        points = len(list(self._series.values())[0])

        for class_id, class_name in Loader.SpongesClasses().items():
            text += "%s : %d\n" % (class_name, analysis.cumulativeDetectionsFor(class_id))
            self._series[class_id].append(points, analysis.cumulativeDetectionsFor(class_id))

        self._total_label.setText("Éponges détectées : %d" % analysis.totalDetections())
        self._sponges_label.setText(text)

        self._chart.axisX().setRange(0, points)
        self._chart.axisY().setRange(0, max(analysis.cumulativeDetections().values()))
