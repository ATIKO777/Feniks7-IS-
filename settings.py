from PyQt5 import QtCore, QtGui, QtWidgets
from ui_settings import Ui_Form
from functions import show_settings, close_settings, save_settings, connect_
import sys



def open_settings(config, app):
    global Form
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    show_settings(ui, config)

    ui.pushButton_2.clicked.connect(lambda: close_settings(Form))
    ui.pushButton.clicked.connect(lambda: save_settings(ui, Form))
    ui.pushButton_3.clicked.connect(lambda: connect_(app, ui, Form))
