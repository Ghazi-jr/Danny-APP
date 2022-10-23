import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QMovie
import os
import pandas as pd
from threading import *
from transformers import pipeline
import numpy as np
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from spacy_download import load_spacy
import re
import os
import datetime
basedir = os.path.dirname(__file__)

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class loadingModel(QtWidgets.QWidget):
    # Signal to detect changement
    switch_window = QtCore.pyqtSignal(pd.DataFrame, pd.Series)
    back_to_main = QtCore.pyqtSignal()
    nlp = load_spacy("en_core_web_sm")

    def load_model(self):
        self.emotion = pipeline("sentiment-analysis",
                                model='arpanghoshal/EmoRoBERTa', return_all_scores=True, framework='tf')

    def get_predictions(self, data):
        preds = []
        labels = []
        for text in data['comment']:  # Change to Text Column
            try:
                pred = self.emotion(text.strip())
                labels.append(max(pred[0], key=lambda x: x['score'])['label'])
                pred_sc = [str(np.round(x["score"] * 100, 3)) +
                           " %" for x in pred[0]]

                preds.append(pred_sc)
            except:
                preds.append(None)
                labels.append(None)
                print('Tokens number is too hight')

        return preds, labels

    def text_cleaning(self, text, stop_words=stopwords.words('english'), allow_postags=set(['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN'])):

        text = re.sub("[^A-Za-z" "]+", " ", text).lower()
        text = re.sub("[0-9" "]+", " ", text)
        words = []
        for token in loadingModel.nlp(text):
            if token.text not in stop_words and token.pos_ in allow_postags:
                words.append(token.lemma_)
        return' '.join(words)

    def get_adjectives(self, text):
        blob = TextBlob(text)
        return [word for (word, tag) in blob.tags if (tag.startswith("JJ") or tag.startswith("VB"))]

    def isNaN(self, string):
        return string != string

    def threading(self):
        try:
            self.load_model()
            # self.data["comment"] = self.data['comment'].apply(
            #     lambda x: self.text_cleaning(x))
            preds, labels = self.get_predictions(self.data)
            text = self.data['comment'].apply(
                lambda x: self.text_cleaning(x))
            adj = text.apply(self.get_adjectives)
            trimmed = []
            for ad in adj:
                aa = ', '.join(list(set(ad)))
                trimmed.append(aa)
            self.emotion_keywords = trimmed

            self.stopAnimation()

            self.data['Label'] = labels
            df = pd.DataFrame(
                preds, columns=["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", 'curiosity', "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"])
            result = pd.concat([self.data, df], axis=1)
            isExist = os.path.exists(os.path.join(
                basedir, "predicted_data"))
            if not isExist:
                os.makedirs(os.path.join(
                    basedir, "predicted_data"))
            result.to_csv(os.path.join(
                basedir, "predicted_data", self.bot_name+"_"+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+".csv"), index=False)

            self.emotion_keywords = pd.Series(self.emotion_keywords)
            if len(self.emotion_keywords) == len(self.data):
                self.switch_window.emit(result, self.emotion_keywords)
            else:
                self.back_to_main.emit()
        except:
            self.back_to_main.emit()
        return -1

    def create_thread(self, data, bot_name):
        self.bot_name = bot_name
        self.loading_thread = Thread(target=self.threading)
        self.data = data
        self.data.dropna(inplace=True)
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

        self.setWindowTitle('Model processing...')
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

        self.message = QtWidgets.QLabel("Waiting For Model prediction...")
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
