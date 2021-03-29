from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QStyle, QStyleOption, QWidget

class StylizableWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def paintEvent(self, a0: QPaintEvent):
        o = QStyleOption()
        o.initFrom(self)

        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

        return super().paintEvent(a0)
