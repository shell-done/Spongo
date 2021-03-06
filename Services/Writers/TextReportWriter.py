from Services.Writers.ReportWriter import ReportWriter

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
        
        selected_morphotypes_names = [m.name() for m in self._analysis.parameters().selectedMorphotypes().values()]
        lines.append("\tMorphotypes recherchés : %s " % ", ".join(selected_morphotypes_names))
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    def _detectionSummary(self) -> str:
        lines = []

        lines.append("Détections :")
        lines.append("-"*25)

        total = self._analysis.totalDetections()
        div_by = total
        if div_by == 0:
            div_by = 1

        for morphotype_id, morphotype in self._analysis.parameters().selectedMorphotypes().items():
            detections = self._analysis.cumulativeDetections()[morphotype_id]
            lines.append("\t%s : %d (%.1f%%)" % (morphotype.name(), detections, detections*100/div_by))

        lines.append("")
        lines.append("\tTotal : %d" % total)
        lines.append("")

        return "\n".join(lines) 

    def text(self) -> str:
        return self._fileHeader() + self._detectionParameters() + self._detectionSummary()

    def write(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self.text())

        print("aaah")
        self.writingCompleted.emit(True)

    def toHTML(self):
        return super().toHTML(self.text())