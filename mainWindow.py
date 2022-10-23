from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
import os

basedir = os.path.dirname(__file__)


class mainWindow(QtWidgets.QMainWindow):

    switch_window = QtCore.pyqtSignal(str, str, str, int)

    def read_style_file(self):
        path_to_style = os.path.join(
            basedir, "assets", "style.qss")
        with open(path_to_style, "r+") as help_file:
            _style = help_file.read()
            self.setStyleSheet(_style)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.bot_id = None
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(
            "Developped by Hafedh Ben Slema®  v1.0")
        self.read_style_file()
        self.icon = QtGui.QIcon(os.path.join(
            basedir, "assets", "icon.ico"))
        self.setWindowIcon(self.icon)

        self.setWindowTitle('Main')
        self.setFixedSize(1400, 900)

        self.path = "Import Dataset"

        # MainLayout
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QGridLayout()
        self.centralWidget.setLayout(layout)
        layout.setRowStretch(0, 4)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 3)
        layout.setRowStretch(5, 1)

        self.head_title = QtWidgets.QLabel('Select Website BOT')
        self.head_title.setObjectName("head_title")

        # BOT Layout
        self.box_layout = QtWidgets.QHBoxLayout()
        self.box_layout.setSpacing(40)
        self.box_layout.setContentsMargins(80, 0, 80, 0)
        img_list = ["reddit.png", "indeed.png", "twitter.png",
                    "glassdoor.png", "linkedin.png", "g2.png", "capterra.png"]
        # 4 is number of Bots
        box_list = []
        for i in range(len(img_list)):
            box = QtWidgets.QPushButton("")
            if img_list[i] in ["linkedin.png", "capterra.png"]:
                box.setEnabled(False)
            box.setObjectName("box")
            box.setCheckable(True)
            icon = QIcon(os.path.join(
                basedir, "assets", img_list[i]))
            box.setIcon(icon)
            box.setIconSize(QtCore.QSize(120, 120))
            box.setCursor(QCursor(Qt.PointingHandCursor))
            box_list.append(box)
        # Render boxes
        self.bot_group = QtWidgets.QButtonGroup()
        i = 0
        for box in box_list:
            self.bot_group.addButton(box, i)
            self.box_layout.addWidget(box)
            i += 1
        self.bot_group.buttonClicked.connect(self.slot)
        # Inputs Layout
        self.input = QtWidgets.QVBoxLayout()
        self.input.setSpacing(14)
        self.input.setContentsMargins(332, 30, 332, 0)
        # Fields
        # Keyword
        self.key_bar = QtWidgets.QLineEdit()
        self.key_bar.setPlaceholderText("Select Search Keyword...")
        self.key_bar.setObjectName("key_bar")
        # Number of Records
        self.number_of_records = QtWidgets.QLineEdit()
        self.number_of_records.setPlaceholderText(
            "Select Number of Records...")
        self.number_of_records.setObjectName("key_bar")
        # Submit
        self.submit_button = QtWidgets.QPushButton('Submit')
        self.submit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.submit_button.clicked.connect(self.submit)
        # Add To inputs
        self.input.addWidget(self.key_bar)
        self.input.addWidget(self.number_of_records)
        self.input.addWidget(self.submit_button)

        self.import_data = QtWidgets.QPushButton("Import Dataset")
        self.import_data.setObjectName("import_dataset")
        self.import_data.setCursor(QCursor(Qt.PointingHandCursor))
        self.import_data.clicked.connect(self.open_workspace)
        self.import_layout = QtWidgets.QGridLayout()
        self.import_layout.addWidget(self.import_data, 0, 0)
        self.import_layout.setColumnStretch(0, 1)
        self.import_layout.setColumnStretch(1, 5)

        # Add to layout
        layout.addWidget(self.head_title, 1, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.box_layout, 2, 0)
        layout.addLayout(self.input, 3, 0)
        layout.addLayout(self.import_layout, 5, 0)

    def slot(self, object):
        self.bot_id = self.bot_group.id(object)

    def submit(self):
        if self.bot_id != None or self.path != "Import Dataset":
            self.switch_window.emit(self.key_bar.text(),
                                    self.number_of_records.text(), self.path, self.bot_id)

    def open_workspace(self):

        path = QtWidgets.QFileDialog.getOpenFileName(
            self.centralWidget,
            "Open a folder",
            basedir
        )
        if path[0]:
            trimmed_path = path[0].split("/")[-1]
            self.path = path[0]
        else:
            trimmed_path = "Import Dataset"
            self.path = trimmed_path
        self.import_data.setText(trimmed_path)
