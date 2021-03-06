import cv2
from numpy import array, ndarray

from PySide2.QtCore import QBuffer, QByteArray
from PySide2.QtGui import QImage, QPixmap

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
    def CVToQImage(array: ndarray) -> QImage:
        height, width, channel = array.shape
        cv2.cvtColor(array, cv2.COLOR_BGR2RGB, array)
        bytesPerLine = 3 * width
        
        image = QImage(array.data, width, height, bytesPerLine, QImage.Format_RGB888)

        return image

    @staticmethod
    def CVToQPixmap(array: ndarray) -> QPixmap:
        return QPixmap.fromImage(ImageConverter.CVToQImage(array))

    @staticmethod
    def QImageToCV(image: QImage) -> ndarray:
        if image.format() != QImage.Format_RGB888:
            image = image.convertToFormat(QImage.Format_RGB888)

        width = image.width()
        height = image.height()

        ptr = image.bits()
        arr = array(ptr).reshape(height, width, 3)

        return arr

    @staticmethod
    def QPixmapToCV(pixmap: QPixmap) -> ndarray:
        return ImageConverter.QImageToCV(pixmap.toImage())