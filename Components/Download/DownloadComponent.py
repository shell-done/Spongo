from PySide2.QtCore import QStandardPaths, Qt, Signal, Slot
from PySide2.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QMessageBox, QSizePolicy, QComboBox, QLabel, QHBoxLayout, QSpinBox

from Models.Analysis import Analysis
from Services.Writers.ReportWriter import ReportWriter
from Services.Writers.PDFReportWriter import PDFReportWriter
from Services.Writers.TextReportWriter import TextReportWriter
from Services.Writers.CSVReportWriter import CSVReportWriter
from Services.Writers.JSONReportWriter import JSONReportWriter
from Services.Writers.XMLReportWriter import XMLReportWriter
from Services.Writers.Yolov4AnnotationsWriter import Yolov4AnnotationsWriter
from Components.Widgets.StylizedButton import StylizedButton

class DownloadComponent(QGroupBox):
    reportFormatChanged = Signal(ReportWriter)
    saveCompleted = Signal(bool)

    def __init__(self):
        super().__init__()

        self._report_writer = None

        self._report_types = {
            "summary": {"name": "Résumé", "description": "Le résumé inclu les statistiques générales sur les images analysées"},
            "full": {"name": "Complet", "description": "Le rapport complet inclu les statistiques détaillées sur les images analysées"},
            "annotations": {"name": "Annotations", "description": "Converti les résultats de l'analyse en annotation utilisable pour l'entrainement"}
        }
        self._report_formats = {
            "summary": {
                "PDF": {"type": "Document PDF", "extension": "*.pdf"},
                "Texte": {"type": "Fichier texte", "extension": "*.txt"}
            },
            "full": {
                "CSV": {"type": "Fichier CSV", "extension": "*.csv"},
                "JSON": {"type": "Fichier JSON", "extension": "*.json"},
                "XML": {"type": "Fichier XML", "extension": "*.xml"},
            },
            "annotations": {
                "Annotations YOLOv4": {"type": "Fichier zip", "extension": "*.zip"}
            }
        }
        self._default_report_type = "summary"

        self.setTitle("Paramètres")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout = QFormLayout(self)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(14)

        self._report_type_cbox = QComboBox()
        for report_type, v in self._report_types.items():
            self._report_type_cbox.addItem(v["name"], report_type)

        main_layout.addRow("Type de rapport :", self._report_type_cbox)

        self._info_text = QLabel(self._report_types[self._default_report_type]["description"])
        self._info_text.setObjectName("info")
        main_layout.addRow(self._info_text)

        self._report_format_cbox = QComboBox()
        for format, data in self._report_formats[self._default_report_type].items():
            self._report_format_cbox.addItem(format, data)

        main_layout.addRow("Format du rapport :", self._report_format_cbox)

        self._detection_shape_label = QLabel("Détection :")
        self._detection_shape_cbox = QComboBox()
        self._detection_shape_cbox.addItem("Rectangle", "rectangle")
        self._detection_shape_cbox.addItem("Cercle", "circle")
        self._detection_shape_label.hide()
        self._detection_shape_cbox.hide()
        main_layout.addRow(self._detection_shape_label, self._detection_shape_cbox)

        self._separator_label = QLabel("Séparateur :")
        self._separator_cbox = QComboBox()
        self._separator_cbox.addItem("Point virgule", ";")
        self._separator_cbox.addItem("Virgule", ",")
        self._separator_label.hide()
        self._separator_cbox.hide()
        main_layout.addRow(self._separator_label, self._separator_cbox)

        self._nb_keeped_label = QLabel("Images à exporter :")
        self._nb_keeped_spinbox = QSpinBox(self)
        self._nb_keeped_spinbox.setRange(1, 1)
        self._nb_keeped_label.hide()
        self._nb_keeped_spinbox.hide()
        main_layout.addRow(self._nb_keeped_label, self._nb_keeped_spinbox)

        spacer_label = QLabel("Spacer")
        spacer_label.hide()
        main_layout.addRow(spacer_label)

        for widget in (self._detection_shape_label, self._detection_shape_cbox, self._separator_label, self._separator_cbox, self._nb_keeped_label, self._nb_keeped_spinbox, spacer_label):
            retain = widget.sizePolicy()
            retain.setRetainSizeWhenHidden(True)
            widget.setSizePolicy(retain)

        download_button = StylizedButton("Télécharger", "blue")
        download_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.addWidget(download_button)
        main_layout.addRow(button_layout)

        self.setLayout(main_layout)

        # Signals
        download_button.clicked.connect(self._exportReport)
        self._report_type_cbox.currentIndexChanged.connect(self._reportTypeChanged)
        self._report_format_cbox.currentTextChanged.connect(self._reportFormatChanged)
        self._detection_shape_cbox.currentIndexChanged.connect(self._reportParamsChanged)
        self._separator_cbox.currentIndexChanged.connect(self._reportParamsChanged)

    def reset(self, analysis: Analysis):
        self._analysis = analysis

        self._report_type_cbox.setCurrentIndex(0)
        self._report_format_cbox.setCurrentIndex(0)
        self._nb_keeped_spinbox.setMaximum(analysis.imagesWithDetections())
        self._nb_keeped_spinbox.setValue(min(100, analysis.imagesWithDetections()))
        self._loadWriter()

    def _loadWriter(self):
        format_text = self._report_format_cbox.currentText()
        if format_text == "PDF":
            self._report_writer = PDFReportWriter(self._analysis)
        
        elif format_text == "Texte":
            self._report_writer = TextReportWriter(self._analysis)

        elif format_text == "CSV":
            self._report_writer = CSVReportWriter(self._analysis, self._separator_cbox.currentData(), self._detection_shape_cbox.currentData())

        elif format_text == "JSON":
            self._report_writer = JSONReportWriter(self._analysis, shape=self._detection_shape_cbox.currentData())
        
        elif format_text == "XML":
            self._report_writer = XMLReportWriter(self._analysis, shape=self._detection_shape_cbox.currentData())

        elif format_text == "Annotations YOLOv4":
            self._report_writer = Yolov4AnnotationsWriter(self._analysis)

        self.reportFormatChanged.emit(self._report_writer)

    @Slot(int)
    def _reportTypeChanged(self, index: int):
        report_type = self.sender().currentData()
        self._info_text.setText(self._report_types[report_type]["description"])

        self._report_format_cbox.clear()
        for format, data in self._report_formats[report_type].items():
            self._report_format_cbox.addItem(format, data)

        if report_type == "full":
            self._detection_shape_label.show()
            self._detection_shape_cbox.show()
        else:
            self._detection_shape_label.hide()
            self._detection_shape_cbox.hide()

        if report_type == "annotations":
            self._nb_keeped_label.show()
            self._nb_keeped_spinbox.show()
        else:
            self._nb_keeped_label.hide()
            self._nb_keeped_spinbox.hide()
    
    @Slot(str)
    def _reportFormatChanged(self, format: str):
        if format == "CSV":
            self._separator_label.show()
            self._separator_cbox.show()
        else: # JSON & XSML
            self._separator_label.hide()
            self._separator_cbox.hide()

        self._loadWriter()

    @Slot(int)
    def _reportParamsChanged(self, index: int):
        self._loadWriter()

    @Slot()
    def _exportReport(self):
        report_type = self._report_type_cbox.currentData()
        if report_type == "annotations":
            self._report_writer.setKeep(self._nb_keeped_spinbox.value())

        error = self._report_writer.checkErrors()
        if error:
            QMessageBox.warning(self.parentWidget(), "Impossible de générer le rapport", error)
            return

        filename = self._analysis.parameters().name()
        report_format = self._report_format_cbox.currentData()

        path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) + "/" + filename
        filter = "Fichier %s (%s)" % (report_format["type"], report_format["extension"])

        result = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", path, filter)
        
        filepath = result[0]
        if filepath == '':
            return

        self._report_writer.write(filepath)
        self.saveCompleted.emit(True)
