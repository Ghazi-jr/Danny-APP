import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd

COLORS = ['#d1e5f0', "#92c5de", '#fddbc7', '#d6604d']


class ProcessedTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter

        elif role == Qt.BackgroundRole:
            value = self._data[index.row()][index.column()]
            value = value.strip("%").strip()
            try:
                value = float(value)
            except:
                pass
            if (isinstance(value, int) or isinstance(value, float)):
                value = int(value)  # Convert to integer for indexing.
                if value >= 0 and value <= 25:
                    value = 0
                elif value > 25 and value <= 50:
                    value = 1
                elif value > 50 and value <= 75:
                    value = 2
                elif value > 75 and value <= 100:
                    value = 3
                return QtGui.QColor(COLORS[value])

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            colNames = ['Comment', 'Label', "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", 'curiosity', "desire", "disappointment", "disapproval", "disgust",
                        "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"]

            return colNames[section]
        else:
            return f"{section}"

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            ch = (value)

            self._data[row][column] = ch
            self.dataChanged.emit(index, index)
            return True
