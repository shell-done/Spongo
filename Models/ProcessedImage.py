from cv2 import cv2
from PyQt5.QtGui import QImage

from Models.Detection import Detection

class ProcessedImage:
    def __init__(self, folder_path: str, file_name: str, detections: list[Detection]):
        self._file_name = file_name
        self._folder_path = folder_path
        self._detections = detections

    def folderPath(self) -> str:
        return self._folder_path

    def fileName(self) -> str:
        return self._file_name

    def filePath(self) -> str:
        return self._folder_path + "/" + self._file_name

    def detections(self) -> list[Detection]:
        return self._detections

    def hasDetections(self) -> bool:
        return len(self._detections) > 0

    def detectionsCount(self) -> dict[int, int]:
        detections_count = {}
        for d in self._detections:
            detections_count[d.classId()] = detections_count.get(d.classId(), 0) + 1

        return detections_count
