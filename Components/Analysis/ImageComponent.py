from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

from Services.Loader import Loader
from Services.HighlightDetectionsThread import HighlightDetectionsThread
from Models.ProcessedImage import ProcessedImage

class ImageComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_label = QLabel("Dernière détection")
        title_label.setFont(QFont('Times', 15))

        self._image_label = QLabel()
        self._image_label.setAlignment(QtCore.Qt.AlignCenter)
        self._highlight_detections_thread = HighlightDetectionsThread()
        self._highlight_detections_thread.imageLoadedSignal.connect(self._highlightedImageReceived)

        self._filename_label = QLabel("Aucune image")
        self._filename_label.setAlignment(QtCore.Qt.AlignCenter)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self._image_label)
        v_layout.addWidget(self._filename_label)

        self._stat_label = QLabel()
        self._stat_label.setAlignment(QtCore.Qt.AlignCenter)

        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self._stat_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        main_layout.addLayout(h_layout)
        main_layout.addWidget(self._image_label)

        self.setLayout(main_layout)

    def reset(self):
        self._image_label.setText("Image loading...")
        self._filename_label.setText("Aucune image")
        self._stat_label.setText("Stats loading...")

    def update(self, processed_image: ProcessedImage):
        self._highlight_detections_thread.start(processed_image)
        
        detections_count = processed_image.detectionsCount()
        text = ""
        
        for class_id, class_name in Loader.SpongesClasses().items():
            text += "%s : %d\n" % (class_name, detections_count.get(class_id, 0))

        self._filename_label.setText(processed_image.fileName())
        self._stat_label.setText(text)

    @pyqtSlot(QImage)
    def _highlightedImageReceived(self, image: QImage):
        pixmap = QPixmap(image)

        scaled = pixmap.scaled(self._image_label.size(), Qt.KeepAspectRatio)
        self._image_label.setPixmap(scaled)