from PyQt5 import QtCore, QtGui, QtWidgets
from ui_taxpayer_edit import Ui_Form
from functions import show_data_for_taxpayer_edit, change_data_taxpayer
import sys


def open_taxpayer_edit(ui_main, db, cursor):
    global Form
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    show_data_for_taxpayer_edit(ui, ui_main, db, cursor)
    ui.pushButton_save.clicked.connect(lambda: change_data_taxpayer(ui, ui_main, db, cursor, Form))
