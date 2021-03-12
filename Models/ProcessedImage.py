from cv2 import cv2
from PyQt5.QtGui import QImage

from Models.Detection import Detection

class ProcessedImage:
    def __init__(self, filepath: str, detections: list[Detection]):
        self.__filepath = filepath
        self.__detections = detections

    def filepath(self) -> str:
        return self.__filepath

    def detections(self) -> list[Detection]:
        return self.__detections

    def hasDetections(self) -> bool:
        return len(self.__detections) > 0

    def detectionsCount(self) -> dict[int, int]:
        detections_count = {}
        for d in self.__detections:
            detections_count[d.classId()] = detections_count.get(d.classId(), 0) + 1

        return detections_count

    def hightlightedImage(self) -> QImage:
        img = cv2.imread(self.__filepath)

        colors = [
            [76, 177, 34],
            [164, 73, 163],
            [155, 105, 0],
            [0, 0, 230],
            [0, 168, 217],
            [100, 0, 0]
        ]

        for d in self.__detections:
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