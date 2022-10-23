from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from wordcloud import WordCloud
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from processed_table_model import ProcessedTableModel
from searched_table_model import searched_table_model
import pandas as pd
import numpy as np
import matplotlib
import os

basedir = os.path.dirname(__file__)
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_alpha(0)
        self.axes = fig.add_subplot(111)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        super(MplCanvas, self).__init__(fig)


class processedUI(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    prev_window = QtCore.pyqtSignal()

    def read_style_file(self):
        path_to_style = os.path.join(
            basedir, "assets", "style.qss")
        with open(path_to_style, "r+") as help_file:
            _style = help_file.read()
            self.setStyleSheet(_style)

    def grey_color_func(self, word, font_size, position, orientation, random_state=None,
                        **kwargs):
        return "hsl(0, 0%%, %d%%)" % np.random.randint(60, 100)

    def buttonClick(self):
        print(self.sender().text())

    def showComments(self):
        try:
            word = self.sender().currentItem().text()
            dlg = QtWidgets.QDialog(self)
            searched = self.data[self.data["comment"].str.contains(
                word.strip())]

            searched = searched[["comment", "Label"]]
            searched_table = QtWidgets.QTableView()
            searched_model = searched_table_model(searched.values)
            searched_proxy = QtCore.QSortFilterProxyModel()
            searched_proxy.setFilterKeyColumn(-1)  # Search all columns.
            searched_proxy.setSourceModel(searched_model)
            searched_proxy.sort(0, Qt.AscendingOrder)
            searched_table.setModel(searched_proxy)
            searched_table.setObjectName("searchedTable")

            searched_table.verticalHeader().setDefaultSectionSize(70)
            searched_table.horizontalHeader().setDefaultSectionSize(130)
            searched_table.horizontalHeader().resizeSection(0, 620)
            searched_table.setVerticalScrollMode(
                QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
            searched_table.setHorizontalScrollMode(
                QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

            table_numbers = searched_table.verticalHeader()
            table_numbers.setVisible(False)

            dlg.setGeometry(380, 250, 840, 480)
            dlg.setWindowTitle(word)
            lay = QtWidgets.QHBoxLayout()
            lay.addWidget(searched_table)
            dlg.setLayout(lay)
            dlg.exec()
        except:
            pass

    def __init__(self, data=pd.DataFrame(), emotion_keys=pd.Series()):
        QtWidgets.QWidget.__init__(self)
        self.data = data
        self.emotion_keys = emotion_keys
        self.emo_raw = emotion_keys
        self.data.fillna("")

        self.read_style_file()
        self.icon = QtGui.QIcon(os.path.join(
            basedir, "assets", "icon.ico"))
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Model Results')
        self.setFixedSize(1400, 900)
        # MainLayout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setRowStretch(0, 3)
        self.layout.setRowStretch(1, 4)

        # Render data Table
        if not(self.data.empty):
            self.dataTable = QtWidgets.QTableView()
            self.model = ProcessedTableModel(data.values)
            self.data_proxy = QtCore.QSortFilterProxyModel()
            self.data_proxy.setFilterKeyColumn(-1)  # Search all columns.
            self.data_proxy.setSourceModel(self.model)
            self.data_proxy.sort(0, Qt.AscendingOrder)
            self.dataTable.setModel(self.data_proxy)
            self.dataTable.setObjectName("dataTable")

            self.dataTable.verticalHeader().setDefaultSectionSize(70)
            self.dataTable.horizontalHeader().setDefaultSectionSize(130)
            self.dataTable.horizontalHeader().resizeSection(0, 620)
            self.dataTable.setVerticalScrollMode(
                QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
            self.dataTable.setHorizontalScrollMode(
                QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

            table_numbers = self.dataTable.verticalHeader()
            table_numbers.setVisible(False)
            self.layout.addWidget(self.dataTable, 1, 0)

        self.render_wc(self.emotion_keys, "admiration")
        combo = QtWidgets.QComboBox(self)
        predicted = list(set(self.data["Label"].values))
        for emo in predicted:
            combo.addItem(emo)

        combo.activated[str].connect(self.onChange)
        combo.setStyleSheet(
            "padding : 20px; color : white; border : 2px solid white; border-radius : 5px; font-size : 18px; font-weight : bold;")

        self.word_select_layout = QtWidgets.QGridLayout()
        self.word_select_layout.addWidget(combo, 0, 0)
        self.word_select_layout.addWidget(self.sc, 1, 0)
        self.word_select_layout.setContentsMargins(10, 0, 0, 0)

        list_widget = QtWidgets.QListWidget(self)
        list_widget.setStyleSheet(
            "border: transparent; color : white; font-size : 18px; font-weight : bold; padding : 10px;")

        # list widget items
        it = [
            num for sublist in self.emotion_keys for num in sublist.split(",")]
        for w in list(set(it)):
            if w != "" and self.data["comment"].str.contains(w.strip()).any() == True:
                item = QtWidgets.QListWidgetItem(w.strip())
                list_widget.addItem(item)

        self.prev_page = QtWidgets.QPushButton("Back to Main Window")
        self.prev_page.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.prev_page.clicked.connect(self.prev)

        list_widget.itemDoubleClicked.connect(self.showComments)
        word_layout = QtWidgets.QGridLayout()
        word_layout.addWidget(list_widget, 0, 0)
        word_layout.addLayout(self.word_select_layout, 0, 1)
        word_layout.addWidget(self.prev_page)
        word_layout.setColumnStretch(0, 3)
        word_layout.setColumnStretch(0, 4)
        word_layout.setContentsMargins(81, 10, 81, 10)
        self.layout.addLayout(word_layout, 0, 0)

    def render_wc(self, emotion_keys, emotion=None):
        self.sc = MplCanvas(self, width=8, height=400, dpi=100)
        dt = self.data.copy()
        dt["Em"] = emotion_keys
        if emotion != None:
            dt = dt[dt["Label"] == emotion]
            dt.fillna("")
            d = [
                num for sublist in dt["Em"].values for num in sublist.split(",")]
            corpus = ",".join(d)
        else:
            corpus = ','.join(self.emotion_keys)
        if (len(corpus) > 10):
            wordcloud = WordCloud(background_color="#27323D",
                                  contour_color='#27323D').generate(corpus)
            self.sc.axes.imshow(wordcloud.recolor(color_func=self.grey_color_func, random_state=3),
                                interpolation="bilinear")

    def re_render_wc(self, emotion_keys, emotion=None):
        self.word_select_layout.removeWidget(self.sc)
        self.sc = MplCanvas(self, width=8, height=400, dpi=100)
        dt = self.data.copy()
        dt["Em"] = emotion_keys
        if emotion != None:
            dt = dt[dt["Label"] == emotion]
            corpus = ",".join(dt["Em"].values)
        else:
            corpus = ','.join(self.emotion_keys)

        if (len(corpus) > 10):
            wordcloud = WordCloud(background_color="#27323D",
                                  contour_color='#27323D').generate(corpus)
            self.sc.axes.imshow(wordcloud.recolor(color_func=self.grey_color_func, random_state=3),
                                interpolation="bilinear")

        self.word_select_layout.addWidget(self.sc, 1, 0)

    def onChange(self):
        emo = self.sender().currentText()
        self.re_render_wc(self.emo_raw, emo)

    def prev(self):
        self.prev_window.emit()
