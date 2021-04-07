from Models.Analysis import Analysis
from Services.Writers.ReportWriter import ReportWriter

class HTMLReportWriter(ReportWriter):
    def __init__(self, analysis: Analysis):
        super().__init__(analysis)

    def text(self) -> str:
        content = open("Resources/documents/report_template.html", encoding="utf-8").read()

        # Summary
        content = content.replace("{{TITLE}}", self._analysis._parameters.name())
        content = content.replace("{{ANALYSED_IMAGES}}", str(self._analysis.imagesCount()))
        content = content.replace("{{START_DATE}}", self._analysis.startDateTime().toString("dd/MM/yyyy 'à' hh:mm"))
        content = content.replace("{{END_DATE}}", self._analysis.endDateTime().toString("dd/MM/yyyy 'à' hh:mm"))
        
        # Parameters
        selected_morphotypes_names = [m.name() for m in self._analysis.parameters().selectedMorphotypes().values()]

        content = content.replace("{{ANALYSED_FOLDER}}", self._analysis.parameters().srcFolder())
        content = content.replace("{{CONFIDENCE_THRESHOLD}}", "%.1f%%" % (self._analysis.parameters().threshold()*100))
        content = content.replace("{{SELECTED_MORPHOTYPES}}", ", ".join(selected_morphotypes_names))
        content = content.replace("{{OPT_SAVE_PROCESSED_IMAGES}}", str(self._analysis.parameters().saveProcessedImages()))
        if self._analysis.parameters().saveProcessedImages():
            content = content.replace("{{PROCESSED_IMAGES_FOLDER}}", self._analysis.parameters().destFolder())
        
        # Detections
        morphotypes_stats = ""
        total_progress = ""

        total = self._analysis.totalDetections()
        for morphotype_id, morphotype in self._analysis.parameters().selectedMorphotypes().items():
            detections = self._analysis.cumulativeDetectionsFor(morphotype_id)

            morphotypes_stats += """
                <div class="stat-item">
                    <div class="stat-item-header">
                        <span class="name">%s</span>
                        <span class="count">%s (%.1f%%)</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress" style="width: %.1f%%; background-color: %s"></div>
                    </div>
                </div>
            """ % (morphotype.name(), detections, detections*100/total, detections*100/total, morphotype.color().name())

            total_progress += """
                <div class="progress" style="width: %.1f%%; background-color: %s"></div>
            """ % (detections*100/total, morphotype.color().name())

        content = content.replace("{{MORPHOTYPES_STATS}}", morphotypes_stats)
        content = content.replace("{{TOTAL_PROGRESS}}", total_progress)
        content = content.replace("{{TOTAL_DETECTIONS}}", str(total))


        # Chart
        content = content.replace("{{CHART_IMAGE}}", self._analysis.base64ChartImage())

        legend_items = ""
        for morphotype_id, morphotype in self._analysis.parameters().selectedMorphotypes().items():
            legend_items += """
                <div class="legend-item">
                    <div class="legend-item-color-container">
                        <div class="legend-item-color" style="background-color: %s"></div>
                    </div>
                    <div class="legend-item-name">%s</div>
                </div>
            """ % (morphotype.color().name(), morphotype.name())

        content = content.replace("{{LEGEND_ITEMS}}", legend_items)

        # Interest
        image_items = ""
        for processed_image_filename, base64_img in self._analysis.mostInterestingBase64Images().items():
            image_items += """
                <div class="images-item">
                    <div class="images-item-container">
                        <img src="%s">
                        <span>%s</span>
                    </div>
                </div>
            """ % (base64_img, processed_image_filename)

        content = content.replace("{{IMAGE_ITEMS}}", image_items)

        return content

    def write(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(self.text())

    def toHTML(self):
        return self.text()
