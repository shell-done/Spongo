import cv2

from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from Models.ProcessedImage import ProcessedImage
from Services.Images.AnalysisImagesGenerator import AnalysisImagesGenerator

class HighlightDetectionsThread(QThread):
    imageLoadedSignal = pyqtSignal(QPixmap)

    def __init__(self):
        super(QThread, self).__init__()
        self._abort = False
        self._processed_image = None

    def start(self, processed_image: ProcessedImage, label_size: QSize = None, dest_folder: str = None):
        self._abort = True

        if self.isRunning:
            self.wait()

        self._processed_image = processed_image
        self._label_size = label_size
        self._dest_folder = dest_folder
        self._abort = False

        super().start()

    def run(self):
        #qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)

        # pixmap = QPixmap(500, 200) #QPixmap(self._processed_image.filePath())
        pixmap = AnalysisImagesGenerator.highlightDetections(self._processed_image)

        if self._abort:
            return

        if self._dest_folder:
            pixmap.toImage().save(self._dest_folder + "/" + self._processed_image.fileName(), quality=85)

        if self._label_size:
            pixmap = pixmap.scaled(self._label_size, Qt.KeepAspectRatio)

        if self._abort:
            return

        self.imageLoadedSignal.emit(pixmap)