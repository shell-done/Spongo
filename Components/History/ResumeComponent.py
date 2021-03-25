from Models.Analysis import Analysis
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ResumeComponent(QWidget):

    def __init__(self):
        super().__init__()

        self._title_label = QLabel()

        main_layout = QVBoxLayout()

        self.setLayout(main_layout)

    def reset(self, analysis):
        pass