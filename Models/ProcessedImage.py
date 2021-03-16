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

    def hightlightedImage(self) -> QImage:
        img = cv2.imread(self.filePath())

        colors = [
            [76, 177, 34],
            [164, 73, 163],
            [155, 105, 0],
            [0, 0, 230],
            [0, 168, 217],
            [100, 0, 0]
        ]

        for d in self._detections:
            x, y, w, h = d.boundingBox()
            label = "%s : %.2f" % (d.className(), d.confidence())

            color = colors[d.classId()]
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 6)
            cv2.rectangle(img, (x - 3, y - labelSize[1] - 20), (x + labelSize[0], y), color, -1)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        q_img = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        return q_img