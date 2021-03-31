import json

from PyQt5.QtCore import QFileInfo
from Services.Loader import Loader

class Parameters:
    @staticmethod
    def fromJSON(obj):
        parameters = Parameters()
        for k,v in obj.items():
            if k == "_morphotypes":
                parameters.__dict__[k] = {int(i):m for i,m in v.items()}
            else:
                parameters.__dict__[k] = v

        return parameters

    def __init__(self):
        self._name = "Analyse de la plongée"
        self._src_folder = ""
        self._threshold = 0.5
        self._device_id = ""
        self._display_processed_images = True

        self._morphotypes = {}
        for i in Loader.SpongesMorphotypes():
            self._morphotypes[i] = True

        self._save_processed_images = False
        self._dest_folder = ""

    def name(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name.strip()

    def srcFolder(self) -> str:
        return self._src_folder

    def setSrcFolder(self, srcFolder: str):
        self._src_folder = srcFolder.strip()

    def threshold(self) -> float:
        return self._threshold

    def setThreshold(self, threshold: float):
        self._threshold = threshold

    def deviceId(self) -> str:
        return self._device_id

    def setDeviceId(self, device_id: str):
        self._device_id = device_id

    def displayProcessedImages(self) -> bool:
        return self._display_processed_images

    def setDisplayProcessedImages(self, display_processed_images: bool):
        self._display_processed_images = display_processed_images

    def morphotypes(self) -> dict:
        return self._morphotypes

    def setMorphotypes(self, morphotypes: dict):
        self._morphotypes = morphotypes

    def selectedMorphotypes(self) -> dict:
        ret = {}
        for k,v in self._morphotypes.items():
            if v:
                ret[k] = Loader.SpongesMorphotypes()[k]

        return ret

    def saveProcessedImages(self) -> bool:
        return self._save_processed_images

    def setSaveProcessedImages(self, saveProcessedImages: bool):
        self._save_processed_images = saveProcessedImages

    def destFolder(self) -> str:
        return self._dest_folder

    def setDestFolder(self, destFolder: str):
        self._dest_folder = destFolder.strip()

    def checkValidity(self) -> str:
        if len(self._name) < 2:
            return "Le nom de l'analyse doit faire au moins 2 caractères"

        if not QFileInfo(self._src_folder).isDir():
            return "Le dossier source sélectionné est invalide"

        if self._threshold < 0.01 or self._threshold > 0.99:
            return "Le seuil de détection doit être compris entre 1%% et 99%%"

        if not any(self._morphotypes.values()):
            return "Aucun morphotype n'a été sélectionné"

        if self._save_processed_images:
            dest_folder = QFileInfo(self._dest_folder)

            if not dest_folder.isDir():
                return "Le dossier de destination sélectionné est invalide"

            if not dest_folder.isWritable():
                return "Le dossier de destination est protégé en écriture, veuillez sélectionner un autre dossier"

        return None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)