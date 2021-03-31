import json

from Services.Loader import Loader

class Detection:
    @staticmethod
    def DetectionShapes() -> list:
        return ["circle", "rectangle"]

    @staticmethod
    def DefaultDetectionShape() -> str:
        return Detection.DetectionShapes()[0]

    @staticmethod
    def fromJSON(obj):
        return Detection(obj["_boundingBox"], obj["_class_id"], obj["_confidence"])

    def __init__(self, bouding_box: list, class_id: int, confidence: float):
        self._boundingBox = bouding_box
        self._class_id = class_id
        self._confidence = confidence

    def boundingBox(self) -> list:
        return self._boundingBox

    def classId(self) -> int:
        return self._class_id

    def className(self) -> str:
        return Loader.SpongesMorphotypes()[self._class_id].name()

    def confidence(self) -> float:
        return self._confidence
    
    def toPointsList(self, shape) -> list:
        if shape == "circle":
            x,y = (self._boundingBox[0] + self._boundingBox[2]//2, self._boundingBox[1] + self._boundingBox[3]//2)
            r = max(self._boundingBox[2], self._boundingBox[3])
            return [x, y, r]

        elif shape == "rectangle":
            return self._boundingBox

        else:
            return None

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)