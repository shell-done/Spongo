from cv2 import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Models.ProcessedImage import ProcessedImage

class HighlightDetectionsThread(QThread):
    imageLoadedSignal = pyqtSignal(QImage)

    def __init__(self):
        super(QThread, self).__init__()
        self._abort = False
        self._processed_image = None

    def start(self, processed_image: ProcessedImage):
        self._abort = True

        if self.isRunning:
            self.wait()

        self._processed_image = processed_image
        self._abort = False

        super().start()

    def run(self):
        img = cv2.imread(self._processed_image.filePath())

        if self._abort:
            return

        colors = [
            [76, 177, 34],
            [164, 73, 163],
            [155, 105, 0],
            [0, 0, 230],
            [0, 168, 217],
            [100, 0, 0]
        ]

        for d in self._processed_image.detections():
            x, y, w, h = d.boundingBox()
            label = "%s : %.2f" % (d.className(), d.confidence())

            color = colors[d.classId()]
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 6)
            cv2.rectangle(img, (x - 3, y - labelSize[1] - 20), (x + labelSize[0], y), color, -1)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if self._abort:
                return

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        q_img = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        if self._abort:
            return

        self.imageLoadedSignal.emit(q_img)