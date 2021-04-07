from PySide2.QtWidgets import QComboBox, QFormLayout, QGridLayout, QGroupBox, QSizePolicy, QSpinBox, QCheckBox, QLabel, QHBoxLayout

from Models.Parameters import Parameters
from Services.Loader import Loader
from Services.NeuralNetwork.NeuralNetwork import NeuralNetwork

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
        self._threshold_sbox.setMaximumWidth(250)
        left_layout.addRow("Seuil de détection :", self._threshold_sbox)

        self._devices_list = QComboBox()
        self._devices_list.setMaximumWidth(250)
        self._setDevicesList()

        left_layout.addRow("Processeur à utiliser :", self._devices_list)

        morphotype_layout = QGridLayout()
        morphotype_layout.setSpacing(5)

        morphotype_layout.addWidget(QLabel("Morphotypes à détecter :"), 0, 0, 1, 4)

        self._tab_cbox = {}
        for k,m in Loader.SpongesMorphotypes().items():
            sponge_cbox = QCheckBox(m.name())
            self._tab_cbox[k] = sponge_cbox

            x = k%2 + 1
            y = k//2 + 1
            morphotype_layout.addWidget(sponge_cbox, x, y)

        morphotype_layout.setColumnMinimumWidth(0, 15)
        morphotype_layout.setColumnStretch(0, 0)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(morphotype_layout)

        self.setLayout(main_layout)

    def _setDevicesList(self):
        self._devices_list.clear()
        available_devices = NeuralNetwork.getAvailableCalculationDevices()

        for device_id, device_name in available_devices.items():
            self._devices_list.addItem(device_name, device_id)

        if len(available_devices) == 1:
            self._devices_list.addItem("GPU (Indisponible)", None)
            self._devices_list.model().item(1).setEnabled(False)
        else:
            self._devices_list.setCurrentIndex(1)

    def reset(self, parameters: Parameters):
        self._threshold_sbox.setValue(parameters.threshold()*100)

        for k,v in parameters.morphotypes().items():
            self._tab_cbox[k].setChecked(v)

    def updateParameters(self, parameters: Parameters):
        parameters.setThreshold(self._threshold_sbox.value()/100)
        parameters.setDeviceId(self._devices_list.currentData())

        for k in parameters.morphotypes():
            parameters.morphotypes()[k] = self._tab_cbox[k].isChecked()
