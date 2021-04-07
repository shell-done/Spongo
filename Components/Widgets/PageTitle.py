from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from Components.Widgets.StylizableWidget import StylizableWidget

class PageTitle(StylizableWidget):
    backArrowClicked = Signal()

    def __init__(self, text: str, show_back_arrow: bool = True, parent: QWidget = None):
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(12)

        self._back_arrow_visible = False
        self._back_arrow = None
        self.showBackArrow(show_back_arrow)

        self._title = QLabel(text, self)
        self._layout.addWidget(self._title)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.setLayout(self._layout)

    def text(self) -> str:
        return self._title().text()

    def setText(self, text: str):
        self._title.setText(text)

    def isBackArrowVisible(self) -> bool:
        return self._back_arrow_visible

    def showBackArrow(self, show: bool):
        if show == self._back_arrow_visible:
            return

        if show:
            self._back_arrow = QLabel(self)
            self._back_arrow.setPixmap(QPixmap(":/img/back_arrow.png"))
            self._back_arrow.mousePressEvent = self._backArrowClicked
            self._back_arrow.setCursor(Qt.PointingHandCursor)

            self._layout.insertWidget(0, self._back_arrow)
        else:
            self._layout.removeWidget()
            self._back_arrow = None

        self._back_arrow_visible = show

    def _backArrowClicked(self, event):
        self.backArrowClicked.emit()