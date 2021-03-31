from Models.Analysis import Analysis

class ReportWriter():
    def __init__(self, analysis: Analysis):
        self._analysis = analysis

    def text(self) -> str:
        return None

    def write(self, filepath: str):
        return None
    