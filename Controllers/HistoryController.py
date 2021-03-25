from PyQt5.QtCore import QDir, QFile, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout
import html
from shutil import copyfile

from Models.Parameters import Parameters
from Controllers.BaseController import BaseController
from Components.History.ResumeComponent import ResumeComponent

class HistoryController(BaseController):

    def __init__(self):
        super().__init__()

        title = QLabel("Historique de l'analyse")
        title.setFont(QFont("Arial", 20))

        self._resume_component = ResumeComponent()

        self._return_button = QPushButton("Retour")
        self._quit_button = QPushButton("Quitter")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self._return_button)
        button_layout.addWidget(self._quit_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self._resume_component)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button slots
        self._return_button.clicked.connect(self._returnClick)
        self._quit_button.clicked.connect(self._quitClick)

    def start(self, analysis):
        self._resume_component.reset(analysis)

        src = "D:/Utilisateurs/Margaux/Documents/Workspace/Projets_M1/Spongo_IHM/data/pdf/default.html"
        dst = "D:/Utilisateurs/Margaux/Documents/Workspace/Projets_M1/Spongo_IHM/data/pdf/current.html"

        with open(src, "r") as f:
            self._data = f.read()

        self.replaceString(analysis)
            
        with open(dst, "w") as f:
            f.write(self._data)

    @pyqtSlot()
    def _returnClick(self):
        pass

    @pyqtSlot()
    def _quitClick(self):
        self.changeWidget.emit("/menu")

    def replaceString(self, analysis):
        self._data = self._data.replace("{{TITLE}}", analysis._parameters.name())
        self._data = self._data.replace("{{DATE}}", analysis.startDateTime().toString("dd-MM-yyyy hh:mm"))

        self._data = self._data.replace("{{ANALYSED_IMAGES}}", str(len(analysis.processedImages())))

        hours = analysis.duration().hour()
        minutes = analysis.duration().minute()
        seconds = analysis.duration().second()
        self._data = self._data.replace("{{TOTAL_TIME}}", "%dh %dm %ds" % (hours, minutes, seconds))

        self._data = self._data.replace("{{DETECTED_SPONGES}}", str(analysis.totalDetections()))

        self._data = self._data.replace("{{SPONGES_PER_IMAGE}}", str(float(analysis.totalDetections() / len(analysis.processedImages()))))

        sponge_element, legend_element = "", ""
        for k, v in analysis._parameters.morphotypes().items():
            if v:
                sponge_element += """<div class="sponge_element">
                        <div class="info_line">
                            <h3>{{SPONGE_NAME}} : </h3>
                            <h3 class="percent">{{NUMBER_SPONGE}} ({{PERCENT}}%)</h3>
                        </div>
                        <div class="progress_element">
                            <div class="progress_bar"></div>
                        </div>
                    </div>"""

                sponge_element = sponge_element.replace("{{SPONGE_NAME}}", str(analysis._parameters.morphotypesNames()[k]))
                sponge_element = sponge_element.replace("{{NUMBER_SPONGE}}", str(analysis.cumulativeDetectionsFor(k)))

                percent = analysis.cumulativeDetectionsFor(k) * 100 / analysis.totalDetections()
                sponge_element = sponge_element.replace("{{PERCENT}}", "{:.1f}".format(percent))

                legend_element += """<div class="legend_element">
                        <div class="color"></div>
                        <h3>{{SPONGE_NAME}}</h3>
                    </div>"""

                legend_element = legend_element.replace("{{SPONGE_NAME}}", str(analysis._parameters.morphotypesNames()[k]))

        self._data = self._data.replace("{{SPONGE_ELEMENT}}", sponge_element)
        self._data = self._data.replace("{{LEGEND_ELEMENT}}", legend_element)
        

