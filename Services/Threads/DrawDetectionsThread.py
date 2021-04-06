from PySide2.QtCore import QSize, Qt, QThread, Signal
from PySide2.QtGui import QPixmap

from Models.ProcessedImage import ProcessedImage
from Services.Images.ImageConverter import ImageConverter
from Services.Images.ImagePainter import ImagePainter

class DrawDetectionsThread(QThread):
    imageLoadedSignal = Signal(ProcessedImage, QPixmap)

    def __init__(self):
        super().__init__()
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
        pixmap = ImagePainter.drawDetections(self._processed_image)

        if self._dest_folder and self._processed_image.hasDetections():
            pixmap.save(self._dest_folder + "/" + self._processed_image.fileName())

        if self._label_size:
            pixmap = pixmap.scaled(self._label_size, Qt.KeepAspectRatio)

        if self._abort:
            return

        self.imageLoadedSignal.emit(self._processed_image, pixmap)