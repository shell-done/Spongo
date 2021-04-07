from Models.Detection import Detection
import json
from numpy import ndarray

class ProcessedImage:
    @staticmethod
    def fromJSON(obj):
        detections = []
        for d in obj["_detections"]:
            detections.append(Detection.fromJSON(d))

        return ProcessedImage(obj["_folder_path"], obj["_file_name"], obj["_size"], detections)

    def __init__(self, folder_path: str, file_name: str, size: tuple, detections: list):
        self._folder_path = folder_path
        self._file_name = file_name
        self._detections = detections
        self._loaded_image = None
        self._size = size

    def folderPath(self) -> str:
        return self._folder_path

    def fileName(self) -> str:
        return self._file_name

    def filePath(self) -> str:
        return self._folder_path + "/" + self._file_name

    def detections(self) -> list:
        return self._detections

    def hasDetections(self) -> bool:
        return len(self._detections) > 0

    def detectionsCount(self) -> dict:
        detections_count = {}
        for d in self._detections:
            detections_count[d.classId()] = detections_count.get(d.classId(), 0) + 1

        return detections_count

    def interestScore(self) -> float:
        s = 0
        for v in self.detectionsCount().values():
            s += v**0.5

        return s

    def size(self) -> tuple:
        return self._size

    def setLoadedImage(self, image: ndarray):
        self._loaded_image = image

    def loadedImage(self) -> ndarray:
        return self._loaded_image

    def resetLoadedImage(self):
        self._loaded_image = None

    def toJSON(self):
        del self._loaded_image
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)