from PyQt5.QtCore import QThread, pyqtSignal

from Models.Analysis import Analysis
from Services.Images.ImageConverter import ImageConverter
from Services.Images.ImagePainter import ImagePainter

class PostAnalysisThread(QThread):
    completed = pyqtSignal()

    def __init__(self):
        super(QThread, self).__init__()
        self._abort = False
        self._analysis = None

    def start(self, analysis: Analysis):
        self._abort = True

        if self.isRunning:
            self.wait()

        self._analysis = analysis
        self._abort = False

        super().start()

    def run(self):
        base64_highlighted_images = {}

        for processed_image in self._analysis.mostInterestingImages(4):
            image = ImagePainter.drawDetections(processed_image)
            base64_image = ImageConverter.QPixmapToBase64(image, format="jpeg", width=1080, with_header=True)

            base64_highlighted_images[processed_image] = base64_image

        self._analysis.setMostInterestingBase64Images(base64_highlighted_images)

        self.completed.emit()