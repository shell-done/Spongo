import cv2
import numpy as np

from PyQt5.QtCore import QBuffer, QByteArray
from PyQt5.QtGui import QImage, QPixmap

class ImageConverter:
    @staticmethod
    def QImageToBase64(image: QImage, format: str ="jpeg", width: int = 1080, with_header: bool = True) -> str:
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        image.scaledToWidth(width).save(buffer, format)
        
        result = ""
        if with_header:
            result += "data:image/%s;base64," % format
        
        result += str(byte_array.toBase64())[2:-1]

        return result

    @staticmethod
    def QPixmapToBase64(pixmap: QPixmap, format: str ="jpeg", width: int = 1080, with_header: bool = True) -> str:
        return ImageConverter.QImageToBase64(pixmap.toImage(), format, width, with_header)

    @staticmethod
    def CVToQImage(array: np.ndarray) -> QImage:
        height, width, channel = array.shape
        cv2.cvtColor(array, cv2.COLOR_BGR2RGB, array)
        bytesPerLine = 3 * width
        
        image = QImage(array.data, width, height, bytesPerLine, QImage.Format_RGB888)

        return image

    @staticmethod
    def CVToQPixmap(array: np.ndarray) -> QPixmap:
        return QPixmap.fromImage(ImageConverter.CVToQImage(array))

    @staticmethod
    def QImageToCV(image: QImage) -> np.ndarray:
        if image.format() != QImage.Format_RGB888:
            image = image.convertToFormat(QImage.Format_RGB888)

        image = image.convertToFormat(4)

        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)

        return arr

    @staticmethod
    def QPixmapToCV(pixmap: QPixmap) -> np.ndarray:
        return ImageConverter.QImageToCV(pixmap.toImage())