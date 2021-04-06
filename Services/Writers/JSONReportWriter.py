import json

from PySide2.QtCore import Qt

from Models.Analysis import Analysis
from Models.ProcessedImage import ProcessedImage
from Models.Detection import Detection
from Services.Writers.ReportWriter import ReportWriter

class JSONReportWriter(ReportWriter):
    def __init__(self, analysis: Analysis, shape=Detection.DefaultDetectionShape()):
        if shape in Detection.DetectionShapes():
            self._shape = shape
        else:
            self._shape = Detection.DefaultDetectionShape()
            print("[WARNING] Invalid shape %s, using default shape : %s" % (shape, self._shape))

        super().__init__(analysis)

    def _fileHeader(self) -> dict:
        informations = {}
        
        informations["analysis_name"] = self._analysis.parameters().name()
        informations["analysed_images"] = self._analysis.imagesCount()
        informations["start_datetime"] = self._analysis.startDateTime().toString(Qt.ISODate)
        informations["end_datetime"] = self._analysis.endDateTime().toString(Qt.ISODate)

        return informations

    def _detectionParameters(self) -> dict:
        parameters = {}
        
        parameters["src_folder"] = self._analysis.parameters().srcFolder()
        if self._analysis.parameters().saveProcessedImages():
            parameters["dest_folder"] = self._analysis.parameters().destFolder()
        parameters["confidence_threshold"] = round(self._analysis.parameters().threshold(), 1)
        parameters["selected_morphotypes"] = [m.name() for m in self._analysis.parameters().selectedMorphotypes().values()]

        return parameters

    def _detections(self) -> list:
        images = []

        id = 0
        for processed_image in self._analysis.processedImages():
            img = {}
            img["filename"] = processed_image.fileName()

            detections = []
            for d in processed_image.detections():
                detections.append({
                    "id": id,
                    "morphotype_id": d.classId(),
                    "morphotype_name": d.className(),
                    "shape": self._shape,
                    "points": d.toPointsList(self._shape)
                })

                id += 1
            
            img["detections"] = detections
            images.append(img)

        return images

    def text(self) -> str:
        obj = {
            "informations": self._fileHeader(),
            "parameters": self._detectionParameters(),
            "images": self._detections()
        }

        return json.dumps(obj, indent=4, ensure_ascii=False)

    def write(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self.text())

    def toHTML(self):
        return super().toHTML(self.text())