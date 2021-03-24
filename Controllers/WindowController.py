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
        self.setWindowIcon(QIcon("Resources/img/icon.png"))

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.menu = MenuController()
        self.parameters = ParametersController()
        self.analysis = AnalysisController()
        self.history = HistoryController()

        self.stackedWidget.addWidget(self.menu)
        self.stackedWidget.addWidget(self.parameters)
        self.stackedWidget.addWidget(self.analysis)
        self.stackedWidget.addWidget(self.history)

        self.stackedWidget.setCurrentWidget(self.menu)

        self.menu.clickedChangeWidget.connect(self.changeWidget)
        self.parameters.clickedChangeWidget.connect(self.changeWidget)
        self.parameters.clickedChangeToAnalysisWidget.connect(self.changetoAnalysisWidget)
        self.analysis.clickedChangeWidget.connect(self.changeWidget)
        self.analysis.clickedChangeToHistoryWidget.connect(self.changetoHistoryWidget)
        self.history.clickedChangeWidget.connect(self.changeWidget)

        self.show()

    def closeEvent(self, event: QCloseEvent):
        ask_exit = self.stackedWidget.currentWidget().askExit()

        if ask_exit:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot(Parameters, list)
    def changetoAnalysisWidget(self, parameters, images):
        current_widget = self.stackedWidget.currentWidget()
        current_widget.stop()

        self.stackedWidget.setCurrentWidget(self.analysis)
        self.analysis.start(parameters, images)

    @pyqtSlot(Analysis)
    def changetoHistoryWidget(self, analysis):
        current_widget = self.stackedWidget.currentWidget()
        current_widget.stop()

        self.stackedWidget.setCurrentWidget(self.history)
        self.history.start(analysis)

    @pyqtSlot(str)
    def changeWidget(self, nameWidget):
        next_widget = None
        if(nameWidget == "MENU"):
            next_widget = self.menu
        if(nameWidget == "PARAMETERS"):
            next_widget = self.parameters
        if(nameWidget == "ANALYSIS"):
            next_widget = self.analysis

        if next_widget is None:
            print("[WARNING] Unknown widget : %s" % str(next_widget))
            return
        
        current_widget = self.stackedWidget.currentWidget()
        current_widget.stop()

        self.stackedWidget.setCurrentWidget(next_widget)
        next_widget.start()

