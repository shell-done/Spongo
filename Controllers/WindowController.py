from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

import Resources.Resources

from Models.Parameters import Parameters
from Models.Analysis import Analysis
from Controllers.MenuController import MenuController
from Controllers.ParametersController import ParametersController
from Controllers.AnalysisController import AnalysisController
from Controllers.HistoryController import HistoryController

class WindowController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spongo")
        self.setFixedSize(1280, 720)
        self.setWindowIcon(QIcon("Resources/img/spongo_icon.png"))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self._widgets = {
            "/menu": MenuController(),
            "/parameters": ParametersController(),
            "/analysis": AnalysisController(),
            "/history": HistoryController()
        }

        for w in self._widgets.values():
            self.stacked_widget.addWidget(w)
            w.changeWidget[str].connect(self._route)
            w.changeWidget[str, object].connect(self._route)

        self._route("/menu")

        self.show()

    def closeEvent(self, event: QCloseEvent):
        ask_exit = self.stacked_widget.currentWidget().askExit()

        if ask_exit:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot(str)
    @pyqtSlot(str, object)
    def _route(self, route_name: str, parameters: object = None):
        next_widget = None
        
        for r,w in self._widgets.items():
            if r == route_name:
                next_widget = w
                break

        if next_widget is None:
            print("[WARNING] Unknown widget : %s" % str(next_widget))
            return

        current_widget = self.stacked_widget.currentWidget()
        current_widget.stop()

        self.stacked_widget.setCurrentWidget(next_widget)

        if route_name == "/analysis":
            next_widget.start(parameters[0], parameters[1])
        elif route_name == "/history":
            next_widget.start(parameters)
        else:
            next_widget.start()
