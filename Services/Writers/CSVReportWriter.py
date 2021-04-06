from Models.Analysis import Analysis
from Models.ProcessedImage import ProcessedImage
from Models.Detection import Detection
from Services.Writers.ReportWriter import ReportWriter

class CSVReportWriter(ReportWriter):
    def __init__(self, analysis: Analysis, separator=";", shape=Detection.DefaultDetectionShape()):
        self._separator = separator

        if shape in Detection.DetectionShapes():
            self._shape = shape
        else:
            self._shape = Detection.DefaultDetectionShape()
            print("[WARNING] Invalid shape %s, using default shape : %s" % (shape, self._shape))

        super().__init__(analysis)

    def _fileHeader(self) -> str:
        labels = ["id", "morphotype_id", "morphotype_name", "filename", "shape", "points", "confidence"]
        return self._separator.join(labels) + "\n"

    def _detections(self) -> str:
        lines = []

        id = 0
        for img in self._analysis.processedImages():
            for d in img.detections():
                points = "\"[%s]\"" % ",".join([str(p) for p in d.toPointsList(self._shape)])
                line = [str(id), str(d.classId()), d.className(), img.fileName(), self._shape, points, "%.3f" % d.confidence()]
                lines.append(self._separator.join(line))
                id += 1

        return "\n".join(lines)

    def text(self) -> str:
        return self._fileHeader() + self._detections()

    def write(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self.text())

    def toHTML(self):
        return super().toHTML(self.text())