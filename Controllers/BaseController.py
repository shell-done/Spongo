from Components.Widgets.StylizableWidget import StylizableWidget
from PySide2.QtCore import Signal
from PySide2.QtGui import QPaintEvent, QPainter
from PySide2.QtWidgets import QStyle, QStyleOption, QWidget

class BaseController(StylizableWidget):
    changeWidget = Signal(str, object)

    def __init__(self):
        super().__init__()

    def start(self):
        pass

    def stop(self):
        pass

    def askExit(self) -> bool:
        return True
