from math import ceil

from Components.Widgets.ChartLegendItem import ChartLegendItem
from PyQt5.QtCore import QMargins, Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QWidget, QLabel, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QSplineSeries

from Models.Parameters import Parameters
from Models.Analysis import Analysis
from Services.Loader import Loader

class StatComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self._series = {}
        self._legend_items = {}

        self.setTitle("Statistiques")

        self._total_label = QLabel()
        
        self._legend_layout = QGridLayout()
        self._legend_layout.setVerticalSpacing(0)
        self._legend_layout.setHorizontalSpacing(50)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._total_label)
        main_layout.addLayout(self._legend_layout)
        main_layout.addSpacing(5)
        main_layout.addWidget(self._createLineChart(), 1)

        self.setLayout(main_layout)

    def reset(self, parameters: Parameters):
        self._parameters = parameters

        self._total_label.setText("Éponges détectées : 0")

        for i in reversed(range(self._legend_layout.count())): 
            self._legend_layout.itemAt(i).widget().setParent(None)

        self._chart.removeAllSeries()
        self._legend_items = {}
        self._series = {}
        for i,n in parameters.morphotypesNames().items():
            self._series[i] = QSplineSeries(self)
            self._series[i].setName(n)
            self._series[i].pen().setWidth(2)
            self._series[i].append(0, 0)
            self._chart.addSeries(self._series[i])

            self._legend_items[i] = ChartLegendItem(n, self._series[i].color(), self)
            self._legend_items[i].toggled.connect(self._legendItemToggled)

        for i,k in enumerate(self._legend_items.keys()):
            row = i%2 + 1
            col = i//2 + 1

            self._legend_layout.addWidget(self._legend_items[k], row, col)

        axis_pen = QPen(QColor(Loader.QSSVariable("@dark")))
        axis_pen.setWidth(2)

        grid_line_pen = QPen(QColor(Loader.QSSVariable("@light-gray")))

        labels_font = QFont(Loader.QSSVariable("@font"))
        labels_font.setPointSize(10)

        self._chart.createDefaultAxes()

        for axis in (self._chart.axisX(), self._chart.axisY()):
            axis.setRange(0, 4)
            axis.setLinePen(axis_pen)
            axis.setGridLinePen(grid_line_pen)
            axis.setLabelFormat("%d")
            axis.setLabelsFont(labels_font)
            

    def _createLineChart(self) -> QChartView:
        self._chart = QChart()
        
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

        self._chart.setTitle("Détections cumulées")
        self._chart.legend().setVisible(False)
        self._chart.setBackgroundBrush(QBrush(QColor("transparent")))
        self._chart.setMargins(QMargins(0, 0, 0, 0))
 
        title_font = QFont(Loader.QSSVariable("@font"))
        title_font.setPointSize(14)
        self._chart.setTitleFont(title_font)
        self._chart.setTitleBrush(QBrush(QColor(Loader.QSSVariable("@dark"))))

        chart_view = QChartView(self._chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    @pyqtSlot(bool)
    def _legendItemToggled(self, state: bool):
        for k,v in self._legend_items.items():
            if v == self.sender():
                self._series[k].setVisible(state)
                break

        self._recalculateAxis()

    def _recalculateAxis(self):
        points = len(list(self._series.values())[0])
        self._chart.axisX().setRange(0, max(points - 1, 4))

        maxY = 0
        for k in self._series:
            if not self._legend_items[k].isChecked():
                continue
            
            maxY = max(maxY, self._analysis.cumulativeDetectionsFor(k))

        maxY = max(maxY, 4)
        self._chart.axisY().setRange(0, maxY)

    def update(self, analysis: Analysis):
        self._analysis = analysis
        points = len(list(self._series.values())[0])

        for class_id in self._parameters.morphotypesNames():
            self._series[class_id].append(points, analysis.cumulativeDetectionsFor(class_id))
            self._legend_items[class_id].setValue(str(analysis.cumulativeDetectionsFor(class_id)))

        self._total_label.setText("Éponges détectées : %d" % analysis.totalDetections())

        self._recalculateAxis()
