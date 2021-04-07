from PySide2.QtCore import Signal

from Components.Widgets.StylizableWidget import StylizableWidget

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
