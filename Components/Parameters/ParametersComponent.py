from Models.Parameters import Parameters
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSpinBox, QWidget, QCheckBox, QDoubleSpinBox, QLabel, QVBoxLayout, QHBoxLayout

from Services.Loader import Loader

class ParametersComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_tabel = QLabel("Paramètres")
        title_tabel.setFont(QFont('Times', 15))

        # Threshold layout
        threshold_label = QLabel("Seuil de détection : ")
        self._threshold_sbox = QSpinBox()
        self._threshold_sbox.setRange(1, 99)
        self._threshold_sbox.setSuffix("%")

        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self._threshold_sbox)

        # Filepath layout
        # detection_box_label = QLabel("Afficher les boîtes de détection en direct : ")
        # self._detection_box_cbox = QCheckBox()

        # detection_box_layout = QHBoxLayout()
        # detection_box_layout.addWidget(detection_box_label)
        # detection_box_layout.addWidget(self._detection_box_cbox)

        # Left layout
        left_layout = QVBoxLayout()
        left_layout.addLayout(threshold_layout)
        #left_layout.addLayout(detection_box_layout)

        # Morphotypes layout
        morphotype_label = QLabel("Morphotypes à détecter : ")

        morphotype_layout = QVBoxLayout()
        morphotype_layout.addWidget(morphotype_label)

        self._tab_cbox = {}
        for k, v in Loader.SpongesClasses().items():
            self._spongeCBox = QCheckBox()
            self._tab_cbox[k] = self._spongeCBox

            sponge_label = QLabel(v)

            sponge_layout = QHBoxLayout()
            sponge_layout.addWidget(self._tab_cbox[k])
            sponge_layout.addWidget(sponge_label)

            morphotype_layout.addLayout(sponge_layout)

        # Horizontal layout
        h_layout = QHBoxLayout()
        h_layout.addLayout(left_layout)
        h_layout.addLayout(morphotype_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_tabel)
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)

    def reset(self, parameters: Parameters):
        self._threshold_sbox.setValue(parameters.threshold()*100)
        # self._detection_box_cbox.setChecked(parameters.displayProcessedImages())

        for k,v in parameters.morphotypes().items():
            self._tab_cbox[k].setChecked(v)

    def updateParameters(self, parameters: Parameters):
        parameters.setThreshold(self._threshold_sbox.value()/100)
        # parameters.setDisplayProcessedImages(self._detection_box_cbox.isChecked())

        for k in parameters.morphotypes():
            parameters.morphotypes()[k] = self._tab_cbox[k].isChecked()
