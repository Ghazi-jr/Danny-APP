from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from table_model import TableModel
import pandas as pd
import sys
import os

basedir = os.path.dirname(__file__)


class DataUI(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(pd.DataFrame, str)
    prev_window = QtCore.pyqtSignal()

    def read_style_file(self):
        path_to_style = os.path.join(
            basedir, "assets", "style.qss")

        with open(path_to_style, "r+") as help_file:
            _style = help_file.read()
            self.setStyleSheet(_style)

    def delete(self):
        if self.dataTable.selectionModel().hasSelection():
            indexes = [QtCore.QPersistentModelIndex(
                index) for index in self.dataTable.selectionModel().selectedRows()]
            maxrow = max(indexes, key=lambda x: x.row()).row()
            next_ix = QtCore.QPersistentModelIndex(
                self.model.index(maxrow+1, 0))
            for index in indexes:
                print('Deleting row %d...' % index.row())
                self.model.removeRow(index.row())
                self.model.dataChanged(index)
            self.dataTable.setCurrentIndex(QtCore.QModelIndex(next_ix))

        else:
            print('No row selected!')

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            self.delete()

    def __init__(self, data=pd.DataFrame(), bot_name=""):
        self.data = data
        self.bot_name = bot_name
        QtWidgets.QWidget.__init__(self)
        self.read_style_file()
        self.icon = QtGui.QIcon(os.path.join(
            basedir, "assets", "icon.ico"))
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Data Observer')
        self.setFixedSize(1400, 900)
        # MainLayout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        # Render data Table
        if not(self.data.empty):
            self.dataTable = QtWidgets.QTableView()
            self.model = TableModel(data.values)
            self.data_proxy = QtCore.QSortFilterProxyModel()
            self.data_proxy.setFilterKeyColumn(-1)  # Search all columns.
            self.data_proxy.setSourceModel(self.model)
            self.data_proxy.sort(0, Qt.AscendingOrder)
            self.dataTable.setModel(self.data_proxy)
            self.dataTable.setObjectName("dataTable")
            table_header = self.dataTable.horizontalHeader()
            table_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.dataTable.setVerticalScrollMode(
                QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

            table_numbers = self.dataTable.verticalHeader()
            table_numbers.setVisible(False)
            self.layout.addWidget(self.dataTable, 1, 0)

        self.process = QtWidgets.QPushButton("Get Model Results")
        self.process.setCursor(QCursor(Qt.PointingHandCursor))
        self.process.clicked.connect(self.submit)

        self.prev_page = QtWidgets.QPushButton("Back to Main Window")
        self.prev_page.setCursor(QCursor(Qt.PointingHandCursor))
        self.prev_page.clicked.connect(self.prev)

        self.config_layout = QtWidgets.QHBoxLayout()
        self.config_layout.setSpacing(600)
        self.config_layout.setContentsMargins(81, 20, 81, 0)
        self.config_layout.addWidget(self.prev_page)
        self.config_layout.addWidget(self.process)

        self.layout.addLayout(self.config_layout, 0, 0)

    def submit(self):
        self.switch_window.emit(self.data, self.bot_name)

    def prev(self):
        self.prev_window.emit()
