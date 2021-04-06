from math import ceil

from Components.Widgets.ChartLegendItem import ChartLegendItem
from PySide2.QtCore import QMargins, Qt, Slot
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide2.QtWidgets import QGridLayout, QGroupBox, QWidget, QLabel, QVBoxLayout
from PySide2.QtCharts import QtCharts

from Models.Parameters import Parameters
from Models.Analysis import Analysis
from Services.Loader import Loader

class StatComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self._series = {}
        self._legend_items = {}

        self.setTitle("Statistiques")
        self.setProperty("qss-var", "pb-0")

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
        for i,m in parameters.selectedMorphotypes().items():
            self._series[i] = QtCharts.QSplineSeries(self)
            self._series[i].setName(m.name())
            self._series[i].setColor(m.color())

            pen = QPen(m.color(), 3)
            pen.setCapStyle(Qt.RoundCap)
            self._series[i].setPen(pen)
            
            self._series[i].append(0, 0)
            self._chart.addSeries(self._series[i])

            self._legend_items[i] = ChartLegendItem(m.name(), m.color(), self)
            self._legend_items[i].toggled.connect(self._legendItemToggled)

        for i,k in enumerate(self._legend_items.keys()):
            row = i%2 + 1
            col = i//2 + 1

            self._legend_layout.addWidget(self._legend_items[k], row, col)

        axis_pen = QPen(Loader.QSSColor("@dark"))
        axis_pen.setWidth(2)

        grid_line_pen = QPen(Loader.QSSColor("@light-gray"))

        labels_font = QFont(Loader.QSSVariable("@font"))
        labels_font.setPointSize(10)

        self._chart.createDefaultAxes()

        for axis in (self._chart.axisX(), self._chart.axisY()):
            axis.setRange(0, 4)
            axis.setLinePen(axis_pen)
            axis.setGridLinePen(grid_line_pen)
            axis.setLabelFormat("%d")
            axis.setLabelsFont(labels_font)
            

    def _createLineChart(self) -> QtCharts.QChartView:
        self._chart = QtCharts.QChart()
        
        self._chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        self._chart.setTitle("Détections cumulées")
        self._chart.legend().setVisible(False)
        self._chart.setBackgroundBrush(QBrush(QColor("transparent")))
        self._chart.setMargins(QMargins(0, 0, 0, 0))
 
        title_font = QFont(Loader.QSSVariable("@font"))
        title_font.setPointSize(14)
        self._chart.setTitleFont(title_font)
        self._chart.setTitleBrush(QBrush(Loader.QSSColor("@dark")))

        chart_view = QtCharts.QChartView(self._chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def update(self, analysis: Analysis):
        self._analysis = analysis
        #points = list(self._series.values())[0].count()

        for class_id in self._parameters.selectedMorphotypes():
            last_idx = self._series[class_id].count() - 1

            new_x = self._series[class_id].at(last_idx).x() + 1
            new_y = analysis.cumulativeDetectionsFor(class_id)

            if last_idx >= 0:
                if self._series[class_id].at(last_idx).y() == new_y:
                    self._series[class_id].replace(last_idx, new_x, new_y)
                    continue

            self._series[class_id].append(new_x, new_y)
            self._legend_items[class_id].setValue(str(new_y))

        self._total_label.setText("Éponges détectées : %d" % analysis.totalDetections())

        self._recalculateAxis()

    def _recalculateAxis(self):
        #points = list(self._series.values())[0].count()
        last_idx = self._series[0].count() - 1
        x = self._series[0].at(last_idx).x()

        self._chart.axisX().setRange(0, max(x, 4))

        maxY = 0
        for k in self._series:
            if not self._legend_items[k].isChecked():
                continue
            
            maxY = max(maxY, self._analysis.cumulativeDetectionsFor(k))

        maxY = max(maxY, 4)

        # Add 5% to show the top series below the top line
        maxY = round(1.05*maxY)

        self._chart.axisY().setRange(0, maxY)

    @Slot(bool)
    def _legendItemToggled(self, state: bool):
        for k,v in self._legend_items.items():
            if v == self.sender():
                self._series[k].setVisible(state)
                break

        self._recalculateAxis()