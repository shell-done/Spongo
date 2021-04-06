from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QColor, QPaintEvent, QPainter, QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QStyle, QStyleOption, QWidget

from Components.Widgets.StylizableWidget import StylizableWidget

class ChartLegendItem(StylizableWidget):
    toggled = Signal(bool)

    def __init__(self, label: str, color: QColor, parent: QWidget = None):
        super().__init__(parent)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        self._is_checked = False
        self._color = color

        self._box = QLabel(self)
        self._box.setCursor(Qt.PointingHandCursor)
        self._box.setFixedSize(18, 18)
        self._box.mousePressEvent = self._boxClicked
        self._box.setObjectName("item-icon")
        self._boxClicked(None)

        self._sponge_label = QLabel(label + " :")
        self._count = QLabel("0")
        self._count.setObjectName("value")

        main_layout.addWidget(self._box)
        main_layout.addWidget(self._sponge_label, 1)
        main_layout.addWidget(self._count)

    def _boxClicked(self, event):
        self._is_checked = not self._is_checked
        color = self._color if self._is_checked else QColor("white")
        pixmap = QPixmap(18, 18)
        pixmap.fill(color)

        self._box.setPixmap(pixmap)
        self.toggled.emit(self._is_checked)

    def isChecked(self) -> bool:
        return self._is_checked

    def setValue(self, value: str):
        self._count.setText(value)
