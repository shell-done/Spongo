from PySide2.QtCore import QStandardPaths, Qt, Signal, Slot
from PySide2.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QMessageBox, QSizePolicy, QComboBox, QLabel, QHBoxLayout, QSpinBox, QVBoxLayout, QWidget

from Models.Analysis import Analysis
from Services.Writers.ReportWriter import ReportWriter
from Services.Writers.PDFReportWriter import PDFReportWriter
from Services.Writers.TextReportWriter import TextReportWriter
from Services.Writers.CSVReportWriter import CSVReportWriter
from Services.Writers.JSONReportWriter import JSONReportWriter
from Services.Writers.XMLReportWriter import XMLReportWriter
from Services.Writers.Yolov4AnnotationsWriter import Yolov4AnnotationsWriter
from Services.Threads.ReportWriterThread import ReportWriterThread
from Components.Widgets.StylizedButton import StylizedButton
from Controllers.MessageBox.ProgressMessageBox import ProgressMessageBox

class DownloadComponent(QGroupBox):
    reportFormatChanged = Signal(ReportWriter)
    saveCompleted = Signal(bool)

    def __init__(self):
        super().__init__()

        self._report_writer = None
        self._report_writer_thread = ReportWriterThread()
        self._report_writer_thread.completed.connect(self._saveCompleted)
        
        self._progress_message = ProgressMessageBox(self.parentWidget(), "Export des données en cours...", "Export des données en cours...", 0, 0)

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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self._form_layout = QFormLayout()
        self._form_layout.setHorizontalSpacing(20)
        self._form_layout.setVerticalSpacing(14)

        self._report_type_cbox = QComboBox()
        for report_type, v in self._report_types.items():
            self._report_type_cbox.addItem(v["name"], report_type)

        self._form_layout.addRow("Type de rapport :", self._report_type_cbox)

        self._info_text = QLabel(self._report_types[self._default_report_type]["description"])
        self._info_text.setObjectName("info")
        self._form_layout.addRow(self._info_text)

        self._report_format_cbox = QComboBox()
        for format, data in self._report_formats[self._default_report_type].items():
            self._report_format_cbox.addItem(format, data)

        self._form_layout.addRow("Format du rapport :", self._report_format_cbox)

        self._detection_shape_cbox = QComboBox()
        self._detection_shape_cbox.addItem("Rectangle", "rectangle")
        self._detection_shape_cbox.addItem("Cercle", "circle")
        self._detection_shape_cbox.hide()

        self._separator_cbox = QComboBox()
        self._separator_cbox.addItem("Point virgule", ";")
        self._separator_cbox.addItem("Virgule", ",")
        self._separator_cbox.hide()

        self._nb_keeped_spinbox = QSpinBox(self)
        self._nb_keeped_spinbox.setRange(1, 1)
        self._nb_keeped_spinbox.hide()

        download_button = StylizedButton("Télécharger", "blue")
        download_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.addWidget(download_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self._form_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

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
        report_type = self._report_type_cbox.currentData()
        self._info_text.setText(self._report_types[report_type]["description"])

        self._report_format_cbox.clear()
        for format, data in self._report_formats[report_type].items():
            self._report_format_cbox.addItem(format, data)

        if report_type == "summary":
            self._showDetectionShape(False)
            self._showSeparator(False)
            self._showKeepedNumber(False)
        elif report_type == "full":
            self._showDetectionShape(True)
            self._showKeepedNumber(False)
        elif report_type == "annotations":
            self._showDetectionShape(False)
            self._showSeparator(False)
            self._showKeepedNumber(True)
    
    @Slot(str)
    def _reportFormatChanged(self, format: str):
        if format == "CSV":
            self._showSeparator(True)
        else: # JSON & XSML
            self._showSeparator(False)

        self._loadWriter()

    def _showDetectionShape(self, show: bool):
        self._showRow("Séparateur :", self._detection_shape_cbox, show)

    def _showSeparator(self, show: bool):
        self._showRow("Détection :", self._separator_cbox, show)

    def _showKeepedNumber(self, show: bool):
        self._showRow("Images à exporter :", self._nb_keeped_spinbox, show)

    def _showRow(self, label: str, widget: QWidget, show: bool):
        if show and not widget.isVisible():
            widget.show()
            self._form_layout.addRow(label, widget)
        elif not show and widget.isVisible():
            label = self._form_layout.labelForField(widget)
            widget.hide()
            label.hide()
            self._form_layout.removeWidget(widget)
            self._form_layout.removeWidget(label)
            del label

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

        self._report_writer_thread.start(self._report_writer, filepath)
        self._progress_message.exec_()

    @Slot()
    def _saveCompleted(self, success: bool):
        if self._progress_message:
            self._progress_message.close()
        
        self.saveCompleted.emit(success)
