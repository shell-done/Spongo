from Models.Analysis import Analysis

class ReportWriter():
    def __init__(self, analysis: Analysis):
        self._analysis = analysis

    def text(self) -> str:
        return None

    def write(self, filepath: str):
        return None

    def toHTML(self, text):
        return """
        <html>
            <head>
                <meta charset='utf-8'>
            </head>
            <body>
                <pre>%s</pre>
            </body>
        </html>
        """ % text
    