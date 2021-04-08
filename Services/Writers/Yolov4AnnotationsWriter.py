from Models.ProcessedImage import ProcessedImage
from zipfile import ZipFile

from PySide2.QtCore import QFile

from Models.Analysis import Analysis
from Services.Loader import Loader
from Services.Writers.ReportWriter import ReportWriter

class Yolov4AnnotationsWriter(ReportWriter):
    def __init__(self, analysis: Analysis):
        self._keep = 100
        super().__init__(analysis)

    def setKeep(self, val: int):
        self._keep = val

    def text(self) -> str:
        return ""

    def checkErrors(self) -> str:
        for img in self._analysis.processedImages():
            if not QFile(img.filePath()).exists():
                text = "Fichier introuvable : %s. Assurez-vous que les images soient toujours dans le dossier analysé (%s). " % (img.fileName(), img.folderPath())
                text += "Si les images étaient sur un support externe (clé USB, disque dur, ...), assurez-vous que celui-ci soit connecté."

                return text

        return None

    def write(self, filepath: str):
        with ZipFile(filepath, "w") as zip:
            classes = ["%d_%s" % (id, morphotype.name()) for id, morphotype in Loader.SpongesMorphotypes().items()]
            zip.writestr("data/classes.txt", "\n".join(classes))

            for img in sorted(self._analysis.processedImages(), key=ProcessedImage.interestScore)[-self._keep:]:
                if not img.hasDetections():
                    continue

                img_w,img_h = img.size()

                lines = []
                for d in img.detections():
                    box = d.boundingBox()

                    nl = (box[0])/img_w
                    nr = (box[0] + box[2])/img_w
                    nt = (box[1])/img_h
                    nb = (box[1] + box[3])/img_h

                    if nl <= 0: nl = 0.00001
                    if nr >= 1: nr = 0.99999
                    if nt <= 0: nt = 0.00001
                    if nb >= 1: nb = 0.99999

                    nx = (nl + nr)/2
                    nw = nr - nl

                    ny = (nt + nb)/2
                    nh = nb - nt

                    lines.append("%d %.6f %.6f %.6f %.6f" % (d.classId(), nx, ny, nw, nh))

                filename = ".".join(img.fileName().split(".")[:-1]) + ".txt"
                text = "\n".join(lines)

                zip.writestr("data/%s" % filename, text)
                zip.write(img.filePath(), "data/%s" % img.fileName())

        self.writingCompleted.emit(True)

    def toHTML(self):
        return super().toHTML("Aucun aperçu disponible")