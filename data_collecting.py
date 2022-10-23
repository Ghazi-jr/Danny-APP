import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QMovie
import os
import pandas as pd
import time
from threading import *
from Bots.indeedBot import IndeedBot
from Bots.glassdoorBot import GlassdoorBot
from Bots.redditBot import RedditBot
from Bots.linkedInBot import LinkedInBot
from Bots.twitterBot import TwitterBot
from Bots.g2Bot import G2BOT
from Bots.capteraBot import CapterraBot
import numpy as np
import sys
import os

import datetime
basedir = os.path.dirname(__file__)


class data_collecting(QtWidgets.QWidget):
    # Signal to detect changement
    switch_window = QtCore.pyqtSignal(pd.DataFrame, str)
    back_to_main = QtCore.pyqtSignal()
    keyword = ""
    nbr = 100
    path = ""
    bot_id = ""

    def threading(self):

        if data_collecting.path != "Import Dataset":
            print(f"Loading data from {data_collecting.path}")
            time.sleep(1)
            self.stopAnimation()
            data = pd.read_csv(data_collecting.path)
            data = data[["comment"]]
            self.switch_window.emit(data, "Imported_data")
        else:
            print("Passed Parameters : ", data_collecting.keyword,
                  "  /  ", data_collecting.nbr, " /  ", data_collecting.bot_id)
            print("Bot Thread Created")
            print("Calling for data scraping...")

            _id = data_collecting.bot_id
            if _id == 0:
                bot = RedditBot(data_collecting.keyword,
                                int(data_collecting.nbr))
                bot_name = "Reddit_data"
            elif _id == 1:
                bot = IndeedBot(data_collecting.keyword,
                                int(data_collecting.nbr))
                bot_name = "Indeed_data"
            elif _id == 2:
                bot = TwitterBot(data_collecting.keyword,
                                 int(data_collecting.nbr))
                bot_name = "Twitter_data"
            elif _id == 3:
                bot = GlassdoorBot(
                    data_collecting.keyword, int(data_collecting.nbr))
                bot_name = "Glassdoor_data"
            elif _id == 4:
                bot = LinkedInBot(data_collecting.keyword,
                                  int(data_collecting.nbr))
                bot_name = "Linkedin_data"
            elif _id == 5:
                bot = G2BOT(data_collecting.keyword, int(data_collecting.nbr))
                bot_name = "G2_data"
            elif _id == 6:
                bot = CapterraBot(data_collecting.keyword,
                                  int(data_collecting.nbr))
                bot_name = "Capterra_data"
            data = bot.run()
            data = data[["comment"]]
            data['comment'].replace('', np.nan, inplace=True)
            data.dropna(subset=['comment'], inplace=True)
            data = data.iloc[:int(data_collecting.nbr)]
            isExist = os.path.exists(os.path.join(
                basedir, "collected_data"))
            if not isExist:
                os.makedirs(os.path.join(
                    basedir, "collected_data"))
            data.to_csv(os.path.join(
                basedir, "collected_data", bot_name+"_"+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+".csv"), index=False)
            self.stopAnimation()
            self.switch_window.emit(data, bot_name)
        # except:
        #     self.back_to_main.emit()

        return -1

    def create_thread(self, keyword, nbr, path, bot_id):
        data_collecting.keyword = keyword
        data_collecting.nbr = nbr  # Int
        data_collecting.path = path
        data_collecting.bot_id = bot_id
        self.loading_thread = Thread(target=self.threading)
        self.loading_thread.start()

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def read_style_file(self):
        path_to_style = os.path.join(
            basedir, "assets", "style.qss")
        with open(path_to_style, "r+") as help_file:
            _style = help_file.read()
            self.setStyleSheet(_style)

    def startAnimation(self):
        self.movie.start()
    # Stop Animation(According to need)

    def stopAnimation(self):
        self.movie.stop()

    def thread(self):
        t1 = Thread(target=self.stopAnimation)
        t1.start()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.read_style_file()
        self.icon = QtGui.QIcon(os.path.join(
            basedir, "assets", "icon.ico"))
        self.setWindowIcon(self.icon)
        QFontDatabase.addApplicationFont("Gilroy-ExtraBold.ttf")
        QFontDatabase.addApplicationFont("Gilroy-Light.ttf")
        QFontDatabase.addApplicationFont("Gilroy-Regular.ttf")

        self.setWindowTitle('Collecting Data...')
        self.setFixedSize(1400, 900)
        # Label Create
        self.loading = QtWidgets.QLabel()

        self.loading.setMinimumSize(QtCore.QSize(200, 200))
        self.loading.setMaximumSize(QtCore.QSize(200, 200))
        self.loading.setObjectName("loading")

        # Loading the GIF
        self.movie = QMovie(os.path.join(
            basedir, "assets", "loading.gif"))
        self.loading.setMovie(self.movie)

        self.startAnimation()

        self.message = QtWidgets.QLabel("Waiting For Data Scraping...")
        self.message.setStyleSheet(
            "color: white; font-family: Gilroy-ExtraBold; font-size : 24px;")
        self.warning = QtWidgets.QLabel("This migh take few minutes")
        self.warning.setStyleSheet(
            "color: white; font-family: Gilroy-Light; font-size : 20px;")

        # Main layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.setRowStretch(0, 10)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(3, 1)
        self.layout.setRowStretch(4, 10)
        # Add to self.layout
        self.layout.addWidget(self.loading, 1, 0,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.message, 2, 0,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.warning, 3, 0,
                              alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
