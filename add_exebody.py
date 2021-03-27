from PyQt5 import QtCore, QtGui, QtWidgets
from ui_add_exebody import Ui_Form
from dataBase import init_comboBox_taxpayers_for_exebodyEdit, init_query_for_table_exeBodyEdit
from functions import add_exebody, add_exebody_cancel, change_data_exebody, newLink_exebody_taxpayer
from del_window import open_del_window
import sys


def open_add_exebody(Form, Qdb, db, cursor):
    global Form_exebody
    Form_exebody = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form_exebody)
    Form_exebody.show()

    Form.close()
    del Form
    id_exebody = add_exebody(db, cursor)

    comboBoxModel = init_comboBox_taxpayers_for_exebodyEdit(ui, Qdb, ui.comboBox_taxpayer)
    tableViewTaxpayerModel = init_query_for_table_exeBodyEdit(ui, Qdb, id_exebody)

    ui.pushButton_cancel.clicked.connect(lambda: add_exebody_cancel(db, cursor, id_exebody, Form_exebody))
    ui.pushButton_add.clicked.connect(lambda: change_data_exebody(ui, id_exebody, Form_exebody, db, cursor))
    ui.pushButton_add_taxpayer.clicked.connect(lambda: newLink_exebody_taxpayer(ui, id_exebody, db, cursor, tableViewTaxpayerModel))

    ui.tableView_taxpayer.customContextMenuRequested.connect(ui.call_contextMenu)

    ui.tableView_taxpayer.pressed.connect(ui.get_cell_selected)

    ui.delete_link_action.triggered.connect(lambda: open_del_window('exeBody_edit_or_add', ui, db, cursor, None, tableViewTaxpayerModel, id_exebody))



