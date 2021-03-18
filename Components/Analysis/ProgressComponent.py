from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import * #(pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import * #(QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import * #(QProgressBar, QPixmap)

try:
    from PyQt5.QtWinExtras import QWinTaskbarButton
    _QT_WIN_EXTRAS_LOADED = True
except ModuleNotFoundError:
    _QT_WIN_EXTRAS_LOADED = False

class ProgressComponent(QWidget):

    def __init__(self):
        super().__init__()

        title_label = QLabel("Progression")
        title_label.setFont(QFont('Times', 15))

        self._max_value = 1
        self._taskbar_button = None

        self._current_image_label = QLabel()
        self._time_label = QLabel()
        self._next_image_label = QLabel()

        info_layout = QHBoxLayout()
        info_layout.addWidget(self._current_image_label)
        info_layout.addWidget(self._time_label)
        info_layout.addWidget(self._next_image_label)

        self._progress_bar = QProgressBar()
        self._progress_bar_animation = QPropertyAnimation(self._progress_bar, b"value")
        self._progress_bar_animation.setDuration(500)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self._progress_bar)

        self.setLayout(main_layout)
    
    def reset(self, max_value: int):
        self._max_value = max_value
        self._progress_bar.setValue(0)
        self._progress_bar.setMaximum(10*max_value)

        self._current_image_label.setText("Image : 0/%d" % max_value)
        self._time_label.setText("Temps restant : ")
        self._next_image_label.setText("Prochaine image : ")

        if _QT_WIN_EXTRAS_LOADED:
            window = self.window().windowHandle()
            if window is None:
                self._taskbar_button = None
            else:
                self._taskbar_button = QWinTaskbarButton(self)
                self._taskbar_button.setWindow(window)
                self._taskbar_button.progress().setVisible(True)
                self._taskbar_button.progress().setRange(0, self._max_value)

    def stop(self):
        if self._taskbar_button is not None:
            self._taskbar_button.progress().setVisible(False)

    def update(self, next_image: str, value: int, time_left: QTime):
        self._progress_bar_animation.stop()
        self._progress_bar_animation.setStartValue(self._progress_bar_animation.currentValue())
        self._progress_bar_animation.setEndValue(value*10)
        self._progress_bar_animation.start()

        self._current_image_label.setText("Image : " + str(value) + "/" + str(self._max_value))

        time_left_str = ""
        if time_left is None:
            time_left_str = "Estimation..."
        else:
            time_left_str = "%dh %dm %ds" % (time_left.hour(), time_left.minute(), time_left.second())

        self._time_label.setText("Temps restant : " + time_left_str)
        self._next_image_label.setText("Prochaine image : " + next_image)

        if self._taskbar_button is not None:
            self._taskbar_button.progress().setValue(value)

