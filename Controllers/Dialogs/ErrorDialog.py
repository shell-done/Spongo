from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

class ErrorDialog(QDialog):
    def __init__(self, message = "Un champ n'est pas correctement rempli", parent = None):
        super().__init__(parent = parent)

        self.setWindowTitle("Erreur !")

        messageLabel = QLabel(message)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(messageLabel)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)
