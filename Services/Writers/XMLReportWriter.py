from collections import OrderedDict
from dict2xml import dict2xml

from PySide2.QtCore import Qt

from Models.Analysis import Analysis
from Models.Detection import Detection
from Services.Writers.ReportWriter import ReportWriter

class XMLReportWriter(ReportWriter):
    def __init__(self, analysis: Analysis, indent=4, shape=Detection.DefaultDetectionShape()):
        self._indent = indent
        
        if shape in Detection.DetectionShapes():
            self._shape = shape
        else:
            self._shape = Detection.DefaultDetectionShape()
            print("[WARNING] Invalid shape %s, using default shape : %s" % (shape, self._shape))

        super().__init__(analysis)

    def _fileHeader(self) -> dict:
        informations = OrderedDict()
        
        informations["analysis_name"] = self._analysis.parameters().name()
        informations["analysed_images"] = self._analysis.imagesCount()
        informations["start_datetime"] = self._analysis.startDateTime().toString(Qt.ISODate)
        informations["end_datetime"] = self._analysis.endDateTime().toString(Qt.ISODate)

        return informations

    def _detectionParameters(self) -> dict:
        parameters = OrderedDict()
        
        parameters["src_folder"] = self._analysis.parameters().srcFolder()
        if self._analysis.parameters().saveProcessedImages():
            parameters["dest_folder"] = self._analysis.parameters().destFolder()
        parameters["confidence_threshold"] = round(self._analysis.parameters().threshold(), 1)
        parameters["selected_morphotypes"] = {"morphotype": [m.name() for m in self._analysis.parameters().selectedMorphotypes().values()]}

        return parameters

    def _detections(self) -> list:
        images = []

        id = 0
        for processed_image in self._analysis.processedImages():
            img = OrderedDict()
            img["filename"] = processed_image.fileName()

            detections = []
            for d in processed_image.detections():
                od = OrderedDict()
                od["id"] = id
                od["morphotype_id"] = d.classId()
                od["morphotype_name"] = d.className()
                od["confidence"] = "%.3f" % d.confidence()
                od["shape"] = self._shape
                od["points"] = {"point": d.toPointsList(self._shape)}
                
                detections.append(od)
                id += 1
            
            img["detections"] = {"detection": detections}
            images.append(img)

        return {"image": images}

    def text(self) -> str:
        obj = OrderedDict()
        obj["informations"] = self._fileHeader()
        obj["parameters"] = self._detectionParameters()
        obj["images"] = self._detections()

        xml_prolog = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        return xml_prolog + dict2xml(obj, wrap="analysis", indent="    ")

    def write(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self.text())

        self.writingCompleted.emit(True)

    def toHTML(self):
        text = self.text()
        escape = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "\"": "&quot;",
            "'": "&apos;"
        }
        for k,v in escape.items():
            text = text.replace(k, v)

        return super().toHTML(text)