import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from data_collecting import data_collecting
from mainWindow import mainWindow
from DataUI import DataUI
from processedUI import processedUI
from loadingModel import loadingModel
from notification import Notification


class Controller(QtWidgets.QMainWindow):

    def __init__(self):
        super(Controller, self).__init__()
        # Initialize All the layouts first
        self.main_window = mainWindow()
        self.window = data_collecting()
        self.model = loadingModel()
        self.model.close()
        self.window.close()
        self.dataui = DataUI()

    # Layouts Controllers
    def show_main_window(self):
        self.main_window = mainWindow()
        self.main_window.switch_window.connect(self.show_main)
        self.window.close()
        self.dataui.close()
        self.model.close()
        try:
            self.processedui.close()
        except:
            pass
        self.main_window.show()

    def show_processed(self, data, emotion_keys):
        self.processedui = processedUI(data, emotion_keys)
        self.processedui.prev_window.connect(self.show_main_window)
        self.dataui.close()
        self.main_window.close()
        self.model.close()
        self.processedui.show()

    def show_dataui(self, data, bot_name):
        self.dataui = DataUI(data, bot_name)
        self.dataui.switch_window.connect(self.show_model_loading)
        self.dataui.prev_window.connect(self.show_main_window)
        self.window.close()
        self.main_window.close()
        self.dataui.show()

    def show_notif(self):
        self.notification = Notification()
        self.notification.setNotify(
            "Error In Data Collecting...", "Please Check your internet connection or Report Bot to Maintenance \nThis message will disappear after 6s...", 6000)
        r = QtCore.QRect(self.x() + round(self.width() / 2) + 320 - round(self.notification.width() / 2) + 300,
                         self.y() + 136, self.notification.m.messageLabel.width() + 30, self.notification.m.messageLabel.height())
        self.notification.setGeometry(r)

    def show_notif_model(self):
        self.notification = Notification()
        self.notification.setNotify(
            "Error In Model Prediction...", "Please Report process details if something went wrong\nThis message will disappear after 6s...", 6000)
        r = QtCore.QRect(self.x() + round(self.width() / 2) + 320 - round(self.notification.width() / 2) + 300,
                         self.y() + 136, self.notification.m.messageLabel.width() + 30, self.notification.m.messageLabel.height())
        self.notification.setGeometry(r)

    def show_main(self, key_word, nbr, path, bot_id):
        self.window = data_collecting()
        self.window.create_thread(key_word, nbr, path, bot_id)
        self.window.switch_window.connect(self.show_dataui)
        self.window.back_to_main.connect(self.show_main_window)
        self.window.back_to_main.connect(self.show_notif)
        self.main_window.close()
        self.dataui.close()
        self.window.show()

    def show_model_loading(self, data, bot_name):
        self.model = loadingModel()
        self.model.create_thread(data, bot_name)
        self.model.switch_window.connect(self.show_processed)
        self.model.back_to_main.connect(self.show_main_window)
        self.model.back_to_main.connect(self.show_notif_model)
        self.main_window.close()
        self.dataui.close()
        self.model.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # Create the controller
    controller = Controller()
    controller.show_main_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
