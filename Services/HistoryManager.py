from Services.AppInfo import AppInfo
from Services.Loader import Loader
import json

from PyQt5.QtCore import QDateTime, QDir, QFile, Qt, QStandardPaths

from Models.Analysis import Analysis

class HistoryManager:
    DATE_FORMAT = "yyyyMMdd-hhmmss"

    @staticmethod
    def appDirectory():
        directory = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        
        if AppInfo.isDevMode():
            directory = directory.replace("python", "Spongo")

        if not QDir().exists(directory):
            QDir().mkdir(directory)

        return directory

    @staticmethod
    def saveAnalysis(analysis: Analysis):
        filename = "%s@%s.json" % (analysis.parameters().name(), analysis.startDateTime().toString(HistoryManager.DATE_FORMAT))
        
        filepath = "%s/%s" % (HistoryManager.appDirectory(), filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json_str = analysis.toJSON()
            f.write(json_str)

    @staticmethod
    def deleteAnalysis(filename: str):
        filepath = "%s/%s.json" % (HistoryManager.appDirectory(), filename)
        QFile.remove(filepath)

    @staticmethod
    def renameAnalysis(current_filename: str, analysis: Analysis):
        HistoryManager.deleteAnalysis(current_filename)
        HistoryManager.saveAnalysis(analysis)

    @staticmethod
    def hasAnalysis() -> bool:
        files = QDir(HistoryManager.appDirectory()).entryList(["*.json"], QDir.Files | QDir.Readable)

        return len(files) > 0

    @staticmethod
    def analysisList() -> list:
        files = QDir(HistoryManager.appDirectory()).entryList(["*.json"], QDir.Files | QDir.Readable)

        analysis = {}
        for f in files:
            f = f.rstrip(".json")
            name, date_str = "@".join(f.split("@")[:-1]), f.split("@")[-1]

            date = QDateTime.fromString(date_str, HistoryManager.DATE_FORMAT)
            analysis[date] = {"name": name, "file": f, "date": date.toString("dd/MM/yyyy")}

        names = []
        for k in sorted(analysis.keys(), reverse=True):
            names.append(analysis[k])

        return names

    @staticmethod
    def loadAnalysis(filename: str) -> Analysis:
        if not filename.endswith(".json"):
            filename += ".json"

        filepath = "%s/%s" % (HistoryManager.appDirectory(), filename)

        with open(filepath, "r", encoding="utf-8") as f:
            json_str = f.read()

        json_obj = json.loads(json_str)
        return Analysis.fromJSON(json_obj)

    @staticmethod
    def loadLastAnalysis() -> Analysis:
        filename = HistoryManager.analysisList()[0]["file"]
        
        return HistoryManager.loadAnalysis(filename)
        