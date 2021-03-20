from Services.ReportWriter import ReportWriter
from Services.Loader import Loader

class TextReportWriter(ReportWriter):
    def _fileHeader(self) -> str:
        lines = []

        lines.append("+%s+" % ("-"*58))
        lines.append("|%s|" % (" "*58))
        lines.append("|%s|" % self._analysis.parameters().name().upper().center(58))
        lines.append("|%s|" % (" "*58))
        lines.append("+%s+" % ("-"*58))
        lines.append("")

        lines.append("Informations :")
        lines.append("-"*25)
        lines.append("\tNom de l'analyse : %s" % self._analysis.parameters().name())
        lines.append("\tImages analysées : %d" % self._analysis.imagesCount())
        lines.append("\tCommencé le : %s" % self._analysis.startDateTime().toString("dd/MM/yyyy 'à' hh:mm"))
        lines.append("\tTerminé le : %s" % self._analysis.endDateTime().toString("dd/MM/yyyy 'à' hh:mm"))
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    def _detectionParameters(self) -> str:
        lines = []

        lines.append("Paramètres :")
        lines.append("-"*25)
        lines.append("\tDossier analysé : %s" % self._analysis.parameters().srcFolder())
        if self._analysis.parameters().saveProcessedImages():
            lines.append("\tDossier des images analysées : %s" % self._analysis.parameters().destFolder())
        lines.append("\tSeuil de confiance : %.1f%%" % (self._analysis.parameters().threshold()*100))
        
        lines.append("\tMorphotypes recherchés : %s " % ", ".join(self._analysis.parameters().morphotypesNames().values()))
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    def _detectionSummary(self) -> str:
        lines = []

        lines.append("Détections :")
        lines.append("-"*25)

        total = self._analysis.totalDetections()
        for class_id, class_name in self._analysis.parameters().morphotypesNames().items():
            detections = self._analysis.cumulativeDetections()[class_id]
            lines.append("\t%s : %d (%.1f%%)" % (class_name, detections, detections*100/total))

        lines.append("")
        lines.append("\tTotal : %d" % total)
        lines.append("")

        return "\n".join(lines) 

    def writeSummary(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self._fileHeader())
            file.write(self._detectionParameters())
            file.write(self._detectionSummary())

        print("Report downloaded")