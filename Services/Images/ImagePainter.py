import cv2
from numpy import ndarray, fromfile, uint8

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap

from Models.ProcessedImage import ProcessedImage
from Services.Loader import Loader
from Services.Images.ImageConverter import ImageConverter

class ImagePainter:
    @staticmethod
    def drawDetections(processed_image: ProcessedImage, pre_loaded_image: ndarray = None, width=2048) -> QPixmap:
        cv_mat = None

        if pre_loaded_image is None:
            cv_mat = cv2.imdecode(fromfile(processed_image.filePath(), dtype=uint8), cv2.IMREAD_UNCHANGED)
            #cv_mat = cv2.imread(processed_image.filePath())
        else:
            cv_mat = pre_loaded_image

        pixmap = ImageConverter.CVToQPixmap(cv_mat)

        original_width = pixmap.width()
        original_height = pixmap.height()

        pixmap = pixmap.scaledToWidth(width)

        x_ratio = pixmap.width()/original_width
        y_ratio = pixmap.height()/original_height

        painter = QPainter(pixmap)
        painter.setFont(QFont(Loader.QSSVariable("@font"), 20))
        
        pen = QPen()
        pen.setWidth(8)
        pen.setJoinStyle(Qt.MiterJoin)
        pen.setColor(QColor("red"))
        painter.setPen(pen)

        fill_brush = QBrush()
        fill_brush.setStyle(Qt.SolidPattern)

        for d in processed_image.detections():
            x, y, w, h = d.boundingBox()
            x *= x_ratio
            w *= x_ratio
            y *= y_ratio
            h *= y_ratio
            label = "%s : %.2f" % (d.className(), d.confidence())
            
            morphotype_color = Loader.SpongesMorphotypes()[d.classId()].color()
            bounding_rect = painter.boundingRect(x, y - 44, 200, 40, Qt.AlignLeft, label)

            pen.setColor(morphotype_color)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(x, y, w, h)
            
            fill_brush.setColor(morphotype_color)
            painter.setBrush(fill_brush)
            painter.drawRect(bounding_rect)

            pen.setColor(QColor("white"))
            painter.setPen(pen)
            painter.drawText(bounding_rect, Qt.AlignLeft, label)

        painter.end()

        return pixmap
