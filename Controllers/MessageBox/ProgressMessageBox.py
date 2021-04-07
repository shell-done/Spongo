from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout

class ProgressMessageBox(QDialog):
    def __init__(self, parent, title: str, text: str, min: int, max: int):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.setWindowTitle(title)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        self._label = QLabel(text, self)
        self._label.setAlignment(Qt.AlignCenter)

        self._progress = QProgressBar(self)
        self._progress.setRange(min, max)

        if min == 0 and max == 0:
            self._progress.setTextVisible(False)

        main_layout.addWidget(self._label)
        main_layout.addWidget(self._progress)

    def setText(self, text: str):
        self._label.setText(text)

    def setRange(self, min: int, max: int):
        self._progress.setRange(min, max)

        if min == 0 and max == 0:
            self._progress.setTextVisible(False)
        else:
            self._progress.setTextVisible(True)

    def setValue(self, val: int):
        self._progress.setValue(val)