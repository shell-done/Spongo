from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap

from Models.ProcessedImage import ProcessedImage
from Services.Loader import Loader

class HighlightDetections:
    @staticmethod
    def generate(processed_image: ProcessedImage) -> QPixmap:
        img = QPixmap(processed_image.filePath())
        painter = QPainter(img)
        painter.setFont(QFont(Loader.QSSVariable("@font"), 30))
        
        pen = QPen()
        pen.setWidth(14)
        pen.setJoinStyle(Qt.MiterJoin)
        pen.setColor(QColor("red"))
        painter.setPen(pen)

        fill_brush = QBrush()
        fill_brush.setStyle(Qt.SolidPattern)

        for d in processed_image.detections():
            x, y, w, h = d.boundingBox()
            label = "%s : %.2f" % (d.className(), d.confidence())
            
            morphotype_color = Loader.SpongesMorphotypes()[d.classId()].color()
            bounding_rect = painter.boundingRect(x, y - 57, 200, 50, Qt.AlignLeft, label)

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

        return img