from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QSizePolicy, QWidget, QLabel, QVBoxLayout, QHBoxLayout

from Models.ProcessedImage import ProcessedImage
from Models.Parameters import Parameters
from Services.Threads.HighlightDetectionsThread import HighlightDetectionsThread

class ImageComponent(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("Dernière détection")

        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignCenter)
        self._image_label.setObjectName("image")

        self._filename_label = QLabel()
        self._filename_label.setAlignment(Qt.AlignCenter)

        main_layout = QGridLayout(self)
        main_layout.addWidget(self._image_label, 0, 0)
        main_layout.addWidget(self._filename_label, 1, 0)

        main_layout.setRowStretch(0, 1)
        main_layout.setVerticalSpacing(10)

        self.setLayout(main_layout)

        self._highlight_detections_thread = HighlightDetectionsThread()
        self._highlight_detections_thread.imageLoadedSignal.connect(self._highlightedImageReceived)

    def reset(self, parameters: Parameters):
        self._parameters = parameters

        self._image_label.setText("Chargement...")
        self._filename_label.setText("")

    def update(self, processed_image: ProcessedImage):
        dest_folder = self._parameters.destFolder() if self._parameters.saveProcessedImages() else None

        self._highlight_detections_thread.start(processed_image, dest_folder)
        self._filename_label.setText(processed_image.fileName())

    @pyqtSlot(QImage)
    def _highlightedImageReceived(self, image: QImage):
        pixmap = QPixmap(image)

        scaled = pixmap.scaled(self._image_label.size(), Qt.KeepAspectRatio)
        self._image_label.setFixedSize(scaled.size())
        self._image_label.setPixmap(scaled)
