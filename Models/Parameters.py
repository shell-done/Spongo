class Parameters:
    def __init__(self, name: str, srcFolder: str, threshold: int, displayProcessedImages: bool, morphotypes: list, saveProcessedImages: bool, destFolder: str):
        self.__name = name
        self.__srcFolder = srcFolder
        self.__threshold = threshold
        self.__displayProcessedImages = displayProcessedImages
        self.__morphotypes = morphotypes
        self.__saveProcessedImages = saveProcessedImages
        self.__destFolder = destFolder

    def name(self):
        return self.__nameAnalysis

    def srcFolder(self):
        return self.__srcFolder

    def threshold(self):
        return self.__threshold
    
    def displayProcessedImages(self):
        return self.__displayProcessedImages

    def morphotypes(self):
        return self.__morphotypes

    def saveProcessedImages(self):
        return self.__saveProcessedImages
    
    def destFolder(self):
        return self.__destFolder
