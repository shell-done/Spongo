from PyQt5.QtCore import QDateTime, QTime

from Models.Parameters import Parameters
from Models.ProcessedImage import ProcessedImage

class Analysis:
    def __init__(self, parameters: Parameters, images_filenames: list):
        self._parameters = parameters

        self._images_filenames = images_filenames
        self._detected_sponges = {key:0 for key in parameters.selectedMorphotypes()}

        self._current_img_index = 0
        self._start_datetime = QDateTime.currentDateTime()
        self._end_datetime = None
        self._processed_images = []
        self._most_interesting_base64_images = []

    def parameters(self) -> Parameters:
        return self._parameters

    def addProcessedImage(self, processed_image: ProcessedImage):
        self._processed_images.append(processed_image)
        
        for k in self._detected_sponges:
            self._detected_sponges[k] += processed_image.detectionsCount().get(k, 0)

        self._current_img_index += 1

    def processedImages(self) -> list:
        return self._processed_images

    def cumulativeDetections(self) -> dict:
        return self._detected_sponges

    def cumulativeDetectionsFor(self, class_id) -> int:
        return self._detected_sponges.get(class_id, 0)

    def totalDetections(self) -> int:
        return sum(self._detected_sponges.values())

    def imagesCount(self) -> int:
        return len(self._images_filenames)

    def currentImageIndex(self) -> int:
        return self._current_img_index

    def currentImageName(self) -> str:
        return self._images_filenames[self._current_img_index]

    def nextImageName(self) -> str:
        if self._current_img_index + 1 < len(self._images_filenames):
            return self._images_filenames[self._current_img_index + 1]

        return None

    def mostInterestingImages(self, count: int) -> list:
        sorted_by_interest = sorted(self._processed_images, key=ProcessedImage.interestScore)
        best_images = sorted_by_interest[-count:] if len(sorted_by_interest) > count else sorted_by_interest

        return best_images

    def mostInterestingBase64Images(self) -> dict:
        return self._most_interesting_base64_images

    def setMostInterestingBase64Images(self, base64_images: dict):
        self._most_interesting_base64_images = base64_images

    def startDateTime(self) -> QDateTime:
        return self._start_datetime

    def endDateTime(self) -> QDateTime:
        return self._end_datetime

    def finish(self):
        self._end_datetime = QDateTime.currentDateTime()

    def isFinished(self):
        return False if self._end_datetime is None else True

    def estimateTimeLeft(self) -> QTime():
        if len(self._processed_images) < 3:
            return None

        if self.isFinished():
            return QTime(0, 0)

        seconds_elapsed = self._start_datetime.secsTo(QDateTime.currentDateTime())
        nb_of_images = len(self._images_filenames)
        nb_of_processed_images = len(self._processed_images)
        seconds_left = seconds_elapsed*(nb_of_images - nb_of_processed_images)//nb_of_processed_images

        time = QTime(0, 0).addSecs(seconds_left)

        return time

    def duration(self):
        seconds_elapsed = self._start_datetime.secsTo(self._end_datetime)
        time = QTime(0, 0).addSecs(seconds_elapsed)

        return time
