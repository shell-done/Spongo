from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from Models.ProcessedImage import ProcessedImage
from Models.Parameters import Parameters
from Services.Threads.HighlightDetectionsThread import HighlightDetectionsThread

class ImageComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_label = QLabel("Dernière détection")
        title_label.setFont(QFont('Times', 15))

        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignCenter)
        self._highlight_detections_thread = HighlightDetectionsThread()
        self._highlight_detections_thread.imageLoadedSignal.connect(self._highlightedImageReceived)

        self._filename_label = QLabel("Aucune image")
        self._filename_label.setAlignment(Qt.AlignCenter)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self._image_label)
        v_layout.addWidget(self._filename_label)

        self._stat_label = QLabel()
        self._stat_label.setAlignment(Qt.AlignCenter)

        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self._stat_label)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        main_layout.addLayout(h_layout)
        main_layout.addWidget(self._image_label)

        self.setLayout(main_layout)

    def reset(self, parameters: Parameters):
        self._parameters = parameters

        self._image_label.setText("Image loading...")
        self._filename_label.setText("Aucune image")
        self._stat_label.setText("Stats loading...")

    def update(self, processed_image: ProcessedImage):
        self._highlight_detections_thread.start(processed_image)
        
        detections_count = processed_image.detectionsCount()
        text = ""
        
        for class_id, class_name in self._parameters.morphotypesNames().items():
            text += "%s : %d\n" % (class_name, detections_count.get(class_id, 0))

        self._filename_label.setText(processed_image.fileName())
        self._stat_label.setText(text)

    @pyqtSlot(QImage)
    def _highlightedImageReceived(self, image: QImage):
        pixmap = QPixmap(image)

        scaled = pixmap.scaled(self._image_label.size(), Qt.KeepAspectRatio)
        self._image_label.setPixmap(scaled)