from PyQt5.QtGui import QColor

class Morphotype:
    def __init__(self, name:str, color: QColor):
        self._name = name
        self._color = color
    
    def name(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def color(self) -> QColor:
        return self._color

    def setColor(self, color: QColor):
        self._color = color

    def __str__(self) -> str:
        return self._name