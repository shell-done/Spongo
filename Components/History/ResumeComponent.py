from Models.Analysis import Analysis
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ResumeComponent(QWidget):

    def __init__(self):
        super().__init__()

        self._title_label = QLabel()
        self._title_label.setFont(QFont('Times', 15))

        # Résumé layout
        resume_title_label = QLabel("Résumé")

        self._date_label = QLabel("Date :")
        self._analysed_images_label = QLabel("Images analysées :")
        self._time_label = QLabel("Temps total :")

        resume_first_line_layout = QHBoxLayout()
        resume_first_line_layout.addWidget(self._date_label)
        resume_first_line_layout.addWidget(self._analysed_images_label)
        resume_first_line_layout.addWidget(self._time_label)

        self._detected_sponges_label = QLabel("Eponges détectées :")
        self._sponge_per_image_label = QLabel("Eponges par image :")

        resume_second_line_layout = QHBoxLayout()
        resume_second_line_layout.addWidget(self._detected_sponges_label)
        resume_second_line_layout.addWidget(self._sponge_per_image_label)

        resume_layout = QVBoxLayout()
        resume_layout.addWidget(resume_title_label)
        resume_layout.addLayout(resume_first_line_layout)
        resume_layout.addLayout(resume_second_line_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._title_label)
        main_layout.addLayout(resume_layout)
        self.setLayout(main_layout)

    def reset(self, analysis):
        self._title_label.setText("Statistiques : %s" % analysis._parameters.name())