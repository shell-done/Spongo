from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QStyle, QStyleOption, QWidget

class BaseController(QWidget):
    changeWidget = pyqtSignal([str], [str, object])

    def __init__(self):
        super().__init__()

    def start(self):
        pass

    def stop(self):
        pass

    def askExit(self) -> bool:
        return True

    def paintEvent(self, a0: QPaintEvent):
        o = QStyleOption()
        o.initFrom(self)

        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

        return super().paintEvent(a0)