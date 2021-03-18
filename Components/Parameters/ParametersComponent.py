from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader

class ParametersComponent(QWidget):

    def __init__(self):
        super().__init__()

        titleLabel = QLabel("Paramètres")
        titleLabel.setFont(QFont('Times', 15))

        # Threshold layout
        thresholdLabel = QLabel("Seuil de détection : ")
        self._thresholdSBox = QDoubleSpinBox()
        self._thresholdSBox.setMinimum(0.01)
        self._thresholdSBox.setMaximum(0.99)
        self._thresholdSBox.setSingleStep(0.01)

        thresholdLayout = QHBoxLayout()
        thresholdLayout.addWidget(thresholdLabel)
        thresholdLayout.addWidget(self._thresholdSBox)

        # Filepath layout
        detectionBoxLabel = QLabel("Afficher les boîtes de détection en direct : ")
        self._detectionBoxCBox = QCheckBox()

        detectionBoxLayout = QHBoxLayout()
        detectionBoxLayout.addWidget(detectionBoxLabel)
        detectionBoxLayout.addWidget(self._detectionBoxCBox)

        # Left layout
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(thresholdLayout)
        leftLayout.addLayout(detectionBoxLayout)

        # Morphotypes layout
        morphotypeLabel = QLabel("Morphotypes à détecter : ")

        morphotypeLayout = QVBoxLayout()
        morphotypeLayout.addWidget(morphotypeLabel)

        self._tabCBox = []
        for k, v in Loader.SpongesClasses().items():
            self._spongeCBox = QCheckBox()
            self._tabCBox.append(self._spongeCBox)

            spongeLabel = QLabel(v)

            spongeLayout = QHBoxLayout()
            spongeLayout.addWidget(self._tabCBox[k])
            spongeLayout.addWidget(spongeLabel)

            morphotypeLayout.addLayout(spongeLayout)

        # Horizontal layout
        hLayout = QHBoxLayout()
        hLayout.addLayout(leftLayout)
        hLayout.addLayout(morphotypeLayout)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(hLayout)

        self.setLayout(mainLayout)

    def setDefaultValues(self, parameters):
        self._thresholdSBox.setValue(parameters.threshold())
        self._detectionBoxCBox.setChecked(parameters.displayProcessedImages())

    def updateParameters(self, parameters):
        parameters.setThreshold(self._thresholdSBox.value())
        parameters.setDisplayProcessedImages(self._detectionBoxCBox.isChecked())

        morphotypes = {}

        for i in range(len(self._tabCBox)):
            morphotypes[i] = self._tabCBox[i].isChecked()

        parameters.setMorphotypes(morphotypes)
