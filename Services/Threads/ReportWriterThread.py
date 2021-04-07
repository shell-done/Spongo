from PySide2.QtCore import QThread, Signal, Slot

from Services.Writers.ReportWriter import ReportWriter

class ReportWriterThread(QThread):
    completed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._abort = False
        self._report_writer = None
        self._filepath = None

    def start(self, report_writer: ReportWriter, filepath: str):
        self._abort = True

        if self.isRunning:
            self.wait()

        self._report_writer = report_writer
        self._filepath = filepath
        self._abort = False

        self._report_writer.writingCompleted.connect(self._completed)

        if self._report_writer.isAsync():
            self._report_writer.write(self._filepath)
        else:
            super().start()

    def run(self):
        self._report_writer.write(self._filepath)

    @Slot(bool)
    def _completed(self, success: bool):
        self.completed.emit(success)
