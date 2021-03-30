from Models.Detection import Detection
import json

class ProcessedImage:
    @staticmethod
    def fromJSON(obj):
        detections = []
        for d in obj["_detections"]:
            detections.append(Detection.fromJSON(d))

        return ProcessedImage(obj["_folder_path"], obj["_file_name"], detections)

    def __init__(self, folder_path: str, file_name: str, detections: list):
        self._folder_path = folder_path
        self._file_name = file_name
        self._detections = detections

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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)