from PyQt5 import QtCore, QtGui, QtWidgets
from ui_add_key import Ui_Form
from functions import add_key_func, show_holder_for_key
import sys


def open_add_key(ui_main, db, cursor):
    global Form
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()


    show_holder_for_key(ui, ui_main, db, cursor)
    ui.pushButton_add.clicked.connect(lambda: add_key_func(ui, ui_main, db, cursor, Form))
