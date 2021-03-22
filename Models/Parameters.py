from Services.Loader import Loader

class Parameters:
    def __init__(self):
        self._name = "Analyse de la plongée"
        self._srcFolder = ""
        self._threshold = 0.5
        self._displayProcessedImages = True

        self._morphotypes = {}
        for i in range(len(Loader.SpongesClasses())):
            self._morphotypes[i] = True

        self._saveProcessedImages = True
        self._destFolder = ""

    def name(self):
        return self._name

    def setName(self, name: str):
        self._name = name

    def srcFolder(self):
        return self._srcFolder

    def setSrcFolder(self, srcFolder: str):
        self._srcFolder = srcFolder

    def threshold(self):
        return self._threshold

    def setThreshold(self, threshold: float):
        self._threshold = threshold

    def displayProcessedImages(self):
        return self._displayProcessedImages

    def setDisplayProcessedImages(self, displayProcessedImages: bool):
        self._displayProcessedImages = displayProcessedImages

    def morphotypes(self):
        return self._morphotypes

    def setMorphotypes(self, morphotypes: dict[int, bool]):
        self._morphotypes = morphotypes

    def saveProcessedImages(self):
        return self._saveProcessedImages

    def setSaveProcessedImages(self, saveProcessedImages: bool):
        self._saveProcessedImages = saveProcessedImages

    def destFolder(self):
        return self._destFolder

    def setDestFolder(self, destFolder: str):
        self._destFolder = destFolder
    
