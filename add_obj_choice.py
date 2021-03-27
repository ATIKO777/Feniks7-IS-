from PyQt5 import QtCore, QtGui, QtWidgets
from ui_add_obj_choice import Ui_Form
from add_taxpayer import open_add_taxpayer
from add_exebody import open_add_exebody
import sys

# Create form and init UI

def open_obj_choice(db, cursor, Qdb):
    global Form
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    ui.pushButton_taxpayer.clicked.connect(lambda: open_add_taxpayer(db, cursor, Form))
    ui.pushButton_exebody.clicked.connect(lambda: open_add_exebody(Form, Qdb, db, cursor))

