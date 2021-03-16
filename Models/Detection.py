from Services.Loader import Loader

class Detection:
    def __init__(self, bouding_box: list, class_id: int, confidence: float):
        self._boundingBox = bouding_box
        self._class_id = class_id
        self._confidence = confidence

    def boundingBox(self) -> list:
        return self._boundingBox

    def classId(self) -> int:
        return self._class_id

    def className(self) -> str:
        return Loader.SpongesClasses()[self._class_id]

    def confidence(self) -> float:
        return self._confidence
    
