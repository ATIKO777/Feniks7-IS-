from PyQt5 import QtCore, QtGui, QtWidgets
from ui_del_window import Ui_Form
import sys



def open_del_window(type_del, ui_main, db, cursor, tree, model, id_exebody=None):
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    ui.pushButton_2.clicked.connect(lambda: close_del_window(Form))
    if type_del == 'treeItem':
        ui.pushButton.clicked.connect(lambda: ui_main.delete_treeItem(db, cursor, tree, Form))
    elif type_del == 'service_or_call':
        ui.pushButton.clicked.connect(lambda: ui_main.delete_service_and_call(model, ui_main.cell_selected, Form))
    elif type_del == 'exeBody_edit_or_add':
        ui.pushButton.clicked.connect(lambda: ui_main.delete_link(model, id_exebody, db, cursor, Form))


def close_del_window(Form):
    Form.close()
    del Form
