from PyQt5.QtWidgets import QWidget

class BaseController(QWidget):
    def __init__(self):
        super().__init__()

    def start(self):
        pass

    def stop(self):
        pass