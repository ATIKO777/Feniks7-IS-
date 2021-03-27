from PyQt5 import QtCore, QtGui, QtWidgets
from ui_exebody_edit import Ui_Form
from functions import show_data_for_exebody_edit, change_data_exebody, newLink_exebody_taxpayer
from dataBase import init_comboBox_taxpayers_for_exebodyEdit, init_query_for_table_exeBodyEdit
from del_window import open_del_window
import sys

def open_exebody_edit(ui_main, db, cursor, Qdb):
    global Form
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    id_exebody = ui_main.current_id


    show_data_for_exebody_edit(ui, ui_main, db, cursor)
    comboBoxModel = init_comboBox_taxpayers_for_exebodyEdit(ui, Qdb, ui.comboBox_taxpayer)
    tableViewTaxpayerModel = init_query_for_table_exeBodyEdit(ui, Qdb, id_exebody)

    ui.pushButton_2.clicked.connect(lambda: change_data_exebody(ui, id_exebody, Form, db, cursor))
    ui.pushButton_add_taxpayer.clicked.connect(lambda: newLink_exebody_taxpayer(ui, id_exebody, db, cursor, tableViewTaxpayerModel))

    ui.tableView_taxpayer.customContextMenuRequested.connect(ui.call_contextMenu)

    ui.tableView_taxpayer.pressed.connect(ui.get_cell_selected)

    ui.delete_link_action.triggered.connect(lambda: open_del_window('exeBody_edit_or_add', ui, db, cursor, None, tableViewTaxpayerModel, id_exebody))
