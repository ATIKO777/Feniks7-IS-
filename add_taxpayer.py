from PyQt5 import QtCore, QtGui, QtWidgets
from ui_add_taxpayer import Ui_Form
from functions import add_taxpayer
import sys



def open_add_taxpayer(db, cursor, Form):
    global Form_taxpayer
    Form_taxpayer = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form_taxpayer)
    Form.close()
    del Form
    Form_taxpayer.show()

    ui.pushButton_add.clicked.connect(lambda: add_taxpayer(ui, db, cursor, Form_taxpayer))
