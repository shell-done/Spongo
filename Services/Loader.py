from Models.Morphotype import Morphotype
import json

from PyQt5.QtGui import QColor
import Resources.Resources
from PyQt5.QtCore import QFile
from PyQt5 import QtCore

class Loader:
    CLASSES_FILE_PATH = "data/parameters/classes.names"
    MORPHOTYPES_FILE_PATH = "Resources/config/morphotypes.json"
    STYLE_FILE_PATH = "Resources/style/style.qss"

    _sponges_morphotypes = {}
    _qss_variables = {}

    @staticmethod
    def SpongesMorphotypes() -> dict:
        if len(Loader._sponges_morphotypes) == 0:
            with open(Loader.MORPHOTYPES_FILE_PATH, 'rt') as f:
                obj = json.loads(f.read())

            for i,m in enumerate(obj):
                Loader._sponges_morphotypes[i] = Morphotype(m["name"], QColor(m["color"]))

        return Loader._sponges_morphotypes

    @staticmethod
    def PreprocessedQSS() -> str:
        lines = []
        qss_file = QFile(Loader.STYLE_FILE_PATH)
        if qss_file.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text):
            text = QtCore.QTextStream(qss_file)

        while not text.atEnd():
            lines.append(text.readLine().rstrip("\n"))

        qss_file.close()

        qss_vars = {}
        qss_body = ""

        for i, l in enumerate(lines):
            l = l.strip()
            if len(l) == 0:
                continue

            if l.startswith("//"):
                continue

            if l[0] == "@":
                if not l.endswith(";"):
                    print("[WARNING] QSSPreprocessor : Parsing error at line %d for '%s' (missing semicolon)" % (i, l))

                l = l.rstrip(";")
                s = l.split(":")
                if len(s) < 2:
                    print("[WARNING] QSSPreprocessor : Parsing error at line %d for '%s' (missing colon)" % (i, l))
                    continue

                qss_vars[s[0].strip()] = s[1].strip()
            else:
                qss_body += l

        qss_vars_names = list(qss_vars.keys())
        qss_vars_names.sort()
        qss_vars_names.reverse()
        for k in qss_vars_names:
            qss_body = qss_body.replace(k, qss_vars[k])
            Loader._qss_variables[k] = qss_vars[k]
        
        return qss_body

    @staticmethod
    def QSSVariable(name: str) -> str:
        return Loader._qss_variables.get(name, None)

    @staticmethod
    def QSSColor(name: str) -> str:
        return QColor(Loader._qss_variables.get(name, None))