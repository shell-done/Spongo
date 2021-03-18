from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import Resources.Resources

from Controllers.MenuController import MenuController
from Controllers.ParametersController import ParametersController
from Controllers.AnalyseController import AnalyseController

class WindowController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spongo")
        self.setFixedSize(1400, 750)
        self.setWindowIcon(QIcon(":/img/icon.png"))

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.menu = MenuController()
        self.parameters = ParametersController()
        self.analyse = AnalyseController()

        self.stackedWidget.addWidget(self.menu)
        self.stackedWidget.addWidget(self.parameters)
        self.stackedWidget.addWidget(self.analyse)

        self.stackedWidget.setCurrentWidget(self.menu)

        self.menu.clickedChangeWidget.connect(self.displayWidget)
        self.parameters.clickedChangeWidget.connect(self.displayWidget)
        self.analyse.clickedChangeWidget.connect(self.displayWidget)

    @pyqtSlot(str, str, list)
    def displayWidget(self, nameWidget, path, images):
        if(nameWidget == "MENU"):
            self.stackedWidget.setCurrentWidget(self.menu)
        if(nameWidget == "PARAMETERS"):
            self.stackedWidget.setCurrentWidget(self.parameters)
        if(nameWidget == "ANALYSE"):
            self.stackedWidget.setCurrentWidget(self.analyse)
            self.analyse.startAnalyse(path, images)

