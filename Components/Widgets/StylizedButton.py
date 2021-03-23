from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton

class StylizedButton(QPushButton):
    def __init__(self, text: str, object_name: str = None):
        super().__init__(text)

        self.setCursor(Qt.PointingHandCursor)

        if object_name:
            self.setObjectName(object_name)

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0,0,0, 0.25*255))
        effect.setOffset(2, 4)
        effect.setBlurRadius(4)
        self.setGraphicsEffect(effect)