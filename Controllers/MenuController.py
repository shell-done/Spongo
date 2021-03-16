from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ErrorDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.setWindowTitle("Erreur !")

        message = QLabel("Aucune image n'a été chargé !")

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

class MenuController(QWidget):
    clickedChangeWidget = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        # Directory Layout
        self.dirLayout = QVBoxLayout()

        self.loadButton = QPushButton("Charger un dossier")

        self.dirLabel = QLabel("Aucun dossier sélectionné")
        self.dirLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.dirLayout.addWidget(self.loadButton)
        self.dirLayout.addWidget(self.dirLabel)

        # Main Layout

        self.startButton = QPushButton("Démarrer")
        self.paramsButton = QPushButton("Paramètres")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.dirLayout)
        self.mainLayout.addWidget(self.paramsButton)
        self.mainLayout.addWidget(self.startButton)


        self.setLayout(self.mainLayout)

        self.images = ""

        # Button slots
        self.loadButton.clicked.connect(self.loadClick)
        self.paramsButton.clicked.connect(self.paramsClick)
        self.startButton.clicked.connect(self.startClick)

    def filterFiles(self, extensions):
        images = self.directory.entryList(extensions, filters = QDir.Files)

        self.dirLabel.setText("Images chargées :\n")

        if len(images) == 0:
            self.dirLabel.setText(self.dirLabel.text() + "Le dossier ne contient aucun fichier ")
            for extension in extensions:
                self.dirLabel.setText(self.dirLabel.text() + str(extension))

        else:
            for image in images:
                self.dirLabel.setText(self.dirLabel.text() + image + "\n")

        return images

    def loadClick(self, event):
        #dialog = QFileDialog()
        #self.path = dialog.getExistingDirectory(self, 'Sélectionner un dossier')
        self.path = "./data/images"

        self.directory = QDir(self.path)
        self.images = self.filterFiles(["*.jpg"])

    def paramsClick(self, event):
        self.clickedChangeWidget.emit("PARAMETERS", "", [])

    def startClick(self, event):
        if len(self.images) == 0:
            error_dialog = ErrorDialog()
            error_dialog.exec_()
        else:
            self.clickedChangeWidget.emit("ANALYSE", self.path, self.images)