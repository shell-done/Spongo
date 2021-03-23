from PyQt5.QtWidgets import QFormLayout, QGridLayout, QGroupBox, QSizePolicy, QSpinBox, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout

from Services.Loader import Loader
from Models.Parameters import Parameters

class ParametersComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Paramètres")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        left_layout = QFormLayout()
        left_layout.setHorizontalSpacing(20)
        left_layout.setVerticalSpacing(14)

        self._threshold_sbox = QSpinBox()
        self._threshold_sbox.setRange(1, 99)
        self._threshold_sbox.setSuffix(" %")
        self._threshold_sbox.setMaximumWidth(150)
        left_layout.addRow("Seuil de détection :", self._threshold_sbox)


        morphotype_layout = QGridLayout()
        morphotype_layout.addWidget(QLabel("Morphotypes à détecter :"), 0, 0, 1, 6)

        self._tab_cbox = {}
        for k, v in Loader.SpongesClasses().items():
            sponge_cbox = QCheckBox()
            self._tab_cbox[k] = sponge_cbox

            x = k%2 + 1
            y = k//2 * 2 + 1
            morphotype_layout.addWidget(sponge_cbox, x, y)
            morphotype_layout.addWidget(QLabel(v), x, y + 1)

        for i in range(0, 7):
            if i == 0:
                morphotype_layout.setColumnMinimumWidth(i, 15)
                morphotype_layout.setColumnStretch(i, 0)
            if i%2 == 1:
                morphotype_layout.setColumnMinimumWidth(i, 20)
                morphotype_layout.setColumnStretch(i, 0)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(morphotype_layout)

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
