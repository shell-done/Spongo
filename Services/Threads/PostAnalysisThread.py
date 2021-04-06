from PySide2.QtCore import QSize, Qt, QMargins, QThread, Signal
from PySide2.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QPixmap
from PySide2.QtCharts import QtCharts

from Models.Analysis import Analysis
from Services.Loader import Loader
from Services.HistoryManager import HistoryManager
from Services.Images.ImageConverter import ImageConverter
from Services.Images.ImagePainter import ImagePainter

class PostAnalysisThread(QThread):
    completed = Signal()

    def __init__(self):
        super().__init__()
        self._abort = False
        self._analysis = None

    def start(self, analysis: Analysis):
        self._abort = True

        if self.isRunning:
            self.wait()

        self._analysis = analysis
        self._abort = False

        self._generateChartImage()

        super().start()

    def run(self):
        self._highlightMostInterestingImages()

        HistoryManager.saveAnalysis(self._analysis)

        self.completed.emit()

    def _highlightMostInterestingImages(self):
        base64_highlighted_images = {}

        for processed_image in self._analysis.mostInterestingImages(4):
            image = ImagePainter.drawDetections(processed_image)
            base64_image = ImageConverter.QPixmapToBase64(image, format="jpeg", width=1080, with_header=True)

            base64_highlighted_images[processed_image.fileName()] = base64_image

        self._analysis.setMostInterestingBase64Images(base64_highlighted_images)

    def _generateChartImage(self):
        chart = QtCharts.QChart()

        chart.legend().setVisible(False)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))
        chart.setMargins(QMargins(0, 0, 0, 0))
        chart.setTitleBrush(QBrush(Loader.QSSColor("@dark")))

        axis_pen = QPen(Loader.QSSColor("@dark"))
        axis_pen.setWidth(4)

        grid_line_pen = QPen(Loader.QSSColor("@light-gray"))

        labels_font = QFont(Loader.QSSVariable("@font"))
        labels_font.setPointSize(18)

        axis_x = QtCharts.QValueAxis()
        axis_y = QtCharts.QValueAxis()

        for axis in (axis_x, axis_y):
            axis.setLinePen(axis_pen)
            axis.setLabelFormat("%d")
            axis.setGridLinePen(grid_line_pen)
            axis.setLabelsFont(labels_font)

        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        

        current_series = {}
        max_s = 0
        for i, m in self._analysis.parameters().selectedMorphotypes().items():
            current_series[i] = QtCharts.QSplineSeries()
            current_series[i].setName(m.name())
            current_series[i].setColor(m.color())

            s = 0
            current_series[i].append(0, 0)
            for k, img in enumerate(self._analysis.processedImages()):
                s += img.detectionsCount().get(i, 0)
                current_series[i].append(k + 1, s)
            max_s = max(s, max_s)
            
            chart.addSeries(current_series[i])

            current_series[i].attachAxis(axis_x)
            current_series[i].attachAxis(axis_y)

            pen = current_series[i].pen()
            pen.setWidth(5)
            current_series[i].setPen(pen)

        chart.axisX().setRange(0, max(len(self._analysis.processedImages()), 4))
        chart.axisY().setRange(0, max(round(max_s*1.05), 4))

        chart_view = QtCharts.QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.resize(QSize(1080, 500))

        chart_pixmap = chart_view.grab()
        self._analysis.setBase64ChartImage(ImageConverter.QPixmapToBase64(chart_pixmap, "png"))
