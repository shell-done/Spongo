from Models.Analysis import Analysis
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStandardPaths, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFormLayout, QGroupBox, QMessageBox, QSizePolicy, QPushButton, QComboBox, QLabel, QHBoxLayout, QLineEdit

from Services.Writers.CSVReportWriter import CSVReportWriter
from Services.Writers.JSONReportWriter import JSONReportWriter
from Services.Writers.XMLReportWriter import XMLReportWriter
from Services.Writers.TextReportWriter import TextReportWriter

from Components.Widgets.StylizedButton import StylizedButton

class DownloadComponent(QGroupBox):
    changeFormat = pyqtSignal([str])

    def __init__(self):
        super().__init__()

        self._info_texts = ["Le résumé inclu les statistiques générales sur les images analysées",
                            "Le rapport complet inclu les statistiques détaillées sur les images analysées"]
        self._report_types = ["Résumé", "Complet"]
        self._resume_report_formats = ["PDF", "Texte"]
        self._resume_report_formats_extensions = ["*.pdf", "*.txt"]
        self._complete_report_formats = ["CSV", "JSON", "XML"]
        self._complete_report_formats_extensions = ["*.csv", "*.json", "*.xml"]

        self.setTitle("Paramètres")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout = QFormLayout(self)
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(14)

        self._report_type_cbox = QComboBox()
        self._report_type_cbox.addItems(self._report_types)
        main_layout.addRow("Type de rapport :", self._report_type_cbox)

        self._info_text = QLabel(self._info_texts[0])
        self._info_text.setObjectName("info")
        main_layout.addRow(self._info_text)

        self._report_format_cbox = QComboBox()
        for i in range(len(self._resume_report_formats)):
            self._report_format_cbox.addItem(self._resume_report_formats[i], self._resume_report_formats_extensions[i])
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

        spacer_label = QLabel("Spacer")
        spacer_label.hide()
        main_layout.addRow(spacer_label)

        for widget in (self._detection_shape_label, self._detection_shape_cbox, self._separator_label, self._separator_cbox, spacer_label):
            retain = widget.sizePolicy()
            retain.setRetainSizeWhenHidden(True)
            widget.setSizePolicy(retain)
            
        filepath_label = QLabel("Destination :")
        self._filepath_text = QLineEdit()
        filepath_button = QPushButton(" Parcourir... ")
        
        filepath_layout = QHBoxLayout()
        filepath_layout.setSpacing(8)
        filepath_layout.addWidget(filepath_label)
        filepath_layout.addWidget(self._filepath_text)
        filepath_layout.addWidget(filepath_button)
        main_layout.addRow(filepath_layout)

        download_button = StylizedButton("Télécharger", "blue")
        download_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.addWidget(download_button)
        main_layout.addRow(button_layout)

        self.setLayout(main_layout)

        # Signals
        filepath_button.clicked.connect(self.filepathBrowse)
        download_button.clicked.connect(self._exportReport)
        self._report_type_cbox.currentIndexChanged.connect(self._reportTypeChanged)
        self._report_format_cbox.currentTextChanged.connect(self._reportFormatChanged)

    def reset(self, analysis: Analysis):
        self._analysis = analysis

        self._report_type_cbox.setCurrentIndex(0)
        self._report_format_cbox.setCurrentIndex(0)

    pyqtSlot()
    def _reportTypeChanged(self, index: int):
        self._info_text.setText(self._info_texts[index])

        self._report_format_cbox.clear()
        if index == 0: # Résumé
            for i in range(len(self._resume_report_formats)):
                self._report_format_cbox.addItem(self._resume_report_formats[i], self._resume_report_formats_extensions[i])
            self._detection_shape_label.hide()
            self._detection_shape_cbox.hide()
        else: # Complet
            for i in range(len(self._complete_report_formats)):
                self._report_format_cbox.addItem(self._complete_report_formats[i], self._complete_report_formats_extensions[i])
            self._detection_shape_label.show()
            self._detection_shape_cbox.show()
    
    pyqtSlot()
    def _reportFormatChanged(self, format: int):
        self.changeFormat[str].emit(format)

        self._filepath_text.setText("")

        if format == "CSV":
            self._separator_label.show()
            self._separator_cbox.show()
        else: # JSON & XSML
            self._separator_label.hide()
            self._separator_cbox.hide()

    @pyqtSlot()
    def filepathBrowse(self):
        dialog = QFileDialog()
       
        filename = self._analysis.parameters().name().replace(" ", "_")
        directory = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        path = dialog.getSaveFileName(self, "Sélectionner un fichier", directory + "/" + filename, self._report_format_cbox.currentData())

        self._filepath_text.setText(path[0])

    @pyqtSlot()
    def _exportReport(self):
        format_text = self._report_format_cbox.currentText()

        if self._filepath_text.text() != "":
            if format_text == "CSV":
                writer = CSVReportWriter(self._analysis, self._separator_cbox.currentData(), self._detection_shape_cbox.currentData())

            elif format_text == "JSON":
                writer = JSONReportWriter(self._analysis, shape=self._detection_shape_cbox.currentData())
            
            elif format_text == "XML":
                writer = XMLReportWriter(self._analysis, shape=self._detection_shape_cbox.currentData())

            elif format_text == "PDF":
                pass
            
            elif format_text == "Texte":
                writer = TextReportWriter(self._analysis)
            
            writer.write(self._filepath_text.text())
            
        else:
            QMessageBox.warning(self, "Erreur", "Vous n'avez pas sélectionné de dossier destination pour le rapport")
