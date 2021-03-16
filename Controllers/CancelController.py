from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

class CancelController(QDialog):
    clickedCancelEvent = pyqtSignal(bool)

    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.setWindowTitle("Attention !")

        message1 = QLabel("Êtes-vous sûr de vouloir arrêter l'analyse des images ?")
        message2 = QLabel("Cette analyse sera perdue et devra être recommencée depuis le début.")

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        buttons.button(QDialogButtonBox.Cancel).setText("Reprendre")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message1)
        self.layout.addWidget(message2)
        self.layout.addWidget(buttons)

        self.setLayout(self.layout)