from Services.Loader import Loader

class Detection:
    def __init__(self, bouding_box: list, class_id: int, confidence: float):
        self.__boundingBox = bouding_box
        self.__class_id = class_id
        self.__confidence = confidence

    def boundingBox(self) -> list:
        return self.__boundingBox

    def classId(self) -> int:
        return self.__class_id

    def className(self) -> str:
        return Loader.SpongesClasses()[self.__class_id]

    def confidence(self) -> float:
        return self.__confidence
    
