from zipfile import ZipFile

from PySide2.QtCore import QFile

from Services.Writers.ReportWriter import ReportWriter


class Yolov4AnnotationsWriter(ReportWriter):
    def text(self) -> str:
        return ""

    def checkErrors(self) -> str:
        for img in self._analysis.processedImages():
            if not QFile(img.filePath()).exists():
                return "Fichier introuvable : %s. Assurez-vous que les images soient toujours dans le dossier analysé (%s)" % (img.fileName(), img.folderPath())

        return None

    def write(self, filepath: str):
        with ZipFile(filepath, "w") as zip:
            for img in self._analysis.processedImages():
                w,h = img.size()

                lines = []
                for d in img.detections():
                    box = d.boundingBox()
                    lines.append("%d %.6f %.6f %.6f %.6f" % (d.classId(), (box[0]+box[2]/2)/w, (box[1]+box[3]/2)/h, box[2]/w, box[3]/h))

                filename = ".".join(img.fileName().split(".")[:-1]) + ".txt"
                text = "\n".join(lines)

                zip.writestr(filename, text)
                zip.write(img.filePath(), img.fileName())

    def toHTML(self):
        return super().toHTML("Aucun aperçu disponible")