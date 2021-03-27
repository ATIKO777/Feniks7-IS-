from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5 import QtCore, QtWidgets
import mysql.connector
from animation import rise_label
from delegate_combo import *

def connectToBase(dataConnect, ui):
    try:
        db_mysql = mysql.connector.connect(
        host = dataConnect['host'],
        user = dataConnect['userName'],
        passwd = dataConnect['password'],
        database = dataConnect['dataBase']
)
    except:
        ui.label_info_2.setText("Ошибка подключения к базе данных!")
        rise_label(ui.label_info_2)
        return -1
    cursor = db_mysql.cursor()

    db = QSqlDatabase.addDatabase("QODBC")
    db.setDatabaseName("Driver={MySQL ODBC 8.0 Unicode Driver};Database=" + dataConnect['dataBase'])
    db.setPort(dataConnect['port']) 
    db.setHostName(dataConnect['host'])
    db.setUserName(dataConnect['userName'])
    db.setPassword(dataConnect['password'])
    if db.open():
        print("OK")
    else:
        print(db.lastError().text())
        with open(r"C:\Users\Matvey\Desktop\Feniks7\project\log_connect.txt", "w") as file:
            file.write(db.lastError().text())
    return [db, db_mysql, cursor]

# def showCalls(db, ui): 
#     model = QSqlTableModel(db = db)
#     model.setTable("calls")
#     model.setHeaderData(1, QtCore.Qt.Horizontal, "Имя")
#     model.setHeaderData(2, QtCore.Qt.Horizontal, "Номер телефона")
#     model.setHeaderData(3, QtCore.Qt.Horizontal, "Вопрос")
#     model.setHeaderData(4, QtCore.Qt.Horizontal, "Источник")
#     model.setHeaderData(5, QtCore.Qt.Horizontal, "Дата")
#     model.select()
#     ui.table_calls.setModel(model)
#     ui.table_calls.setColumnHidden(model.fieldIndex("ID"), True)

#     header = ui.table_calls.horizontalHeader()       
#     header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

#     delegate = ComboDelegate()
#     ui.table_calls.setItemDelegateForColumn (3, delegate)
#     return model

# def modelService_init (db, ui):
#     model = QSqlTableModel(db = db)
#     model.setTable("service")
#     model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование")
#     model.setHeaderData(3, QtCore.Qt.Horizontal, "Оплачено")
#     model.setHeaderData(4, QtCore.Qt.Horizontal, "Дата оплаты")
#     model.setHeaderData(5, QtCore.Qt.Horizontal, "Дата заявки")
#     model.select()
#     ui.table_service.setModel(model)
#     ui.table_service.setColumnHidden(model.fieldIndex("ID"), True)
#     ui.table_service.setColumnHidden(model.fieldIndex("client"), True)

#     header = ui.table_service.horizontalHeader()       
#     header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
#     header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

#     delegate = ComboDelegateForService()
#     ui.table_service.setItemDelegateForColumn (1, delegate)

#     return model

def modelService_init (db, ui):
    model = QSqlRelationalTableModel(db = db)
    model.setTable("service")
    model.setRelation(1, QSqlRelation("amenities", "ID", "T"))
    model.setRelation(5, QSqlRelation("yes_no", "ID", "choice"))
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Дата заявки")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "Дата оплаты")
    model.setHeaderData(5, QtCore.Qt.Horizontal, "Оплачено")
    model.select()
    ui.table_service.setModel(model)
    ui.table_service.setColumnHidden(model.fieldIndex("ID"), True)
    ui.table_service.setColumnHidden(model.fieldIndex("client"), True)

    header = ui.table_service.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

    ui.table_service.setItemDelegate(QSqlRelationalDelegate(ui.table_service))

    return model

def init_comboBox_taxpayers_for_exebodyEdit(ui, db, comboBox):
    model = QSqlTableModel(db = db)
    model.setTable("taxpayer")
    model.select()

    comboBox.setModel(model)
    comboBox.setModelColumn(1)

    return model

def init_query_for_table_exeBodyEdit (ui, db, id_exebody):
    model = QSqlQueryModel()
    model.setQuery('SELECT taxpayer.ID, taxpayer.title FROM taxpayer, link_payer_exebody, executive_body WHERE link_payer_exebody.taxpayer=taxpayer.ID AND link_payer_exebody.executive_body=executive_body.ID AND executive_body.ID=' + str(id_exebody))

    ui.tableView_taxpayer.setModel(model)
    ui.tableView_taxpayer.setColumnHidden(0, True)

    header = ui.tableView_taxpayer.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Предприятие")

    return model

def init_query_for_graph (ui, db):
    model = QSqlRelationalTableModel(db = db)
    model.setTable("graphique_taxpayer")
    model.setRelation(1, QSqlRelation("taxpayer", "ID", "title"))

    model.select()

    ui.tableView.setModel(model)
    ui.tableView.setColumnHidden(0, True)
    ui.tableView.setColumnHidden(2, True)
    ui.tableView.setColumnHidden(3, True)
    ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    header = ui.tableView.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Предприятие")

    return model

def init_model_for_searchAdv_exebody(ui, db):
    model = QSqlQueryModel()
    model.setQuery('SELECT * FROM executive_body')
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Имя")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Фамилия")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Отчество")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "Дата рождения")
    model.setHeaderData(5, QtCore.Qt.Horizontal, "Номер телефона")
    model.setHeaderData(6, QtCore.Qt.Horizontal, "E-mail")
    model.setHeaderData(7, QtCore.Qt.Horizontal, "Домашний адрес")


    ui.table_advSearch_exebody.setModel(model)
    ui.table_advSearch_exebody.setColumnHidden(0, True)

    header = ui.table_advSearch_exebody.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)

    return model

def init_model_for_searchAdv_ekeys(ui, db):
    model = QSqlQueryModel()
    model.setQuery('SELECT taxpayer.title, ekey.* FROM ekey, taxpayer WHERE ekey.holder=taxpayer.ID')
    model.setHeaderData(0, QtCore.Qt.Horizontal, "Предприятие")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Дата регистрации")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Дата истечения")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "Тип")
    model.setHeaderData(6, QtCore.Qt.Horizontal, "Статус активности")

    ui.table_advSearch_ekeys.setModel(model)
    ui.table_advSearch_ekeys.setColumnHidden(1, True)
    ui.table_advSearch_ekeys.setColumnHidden(5, True)

    header = ui.table_advSearch_ekeys.horizontalHeader()       
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

    return model


def showCalls(db, ui): 
    model = QSqlRelationalTableModel(db = db)
    model.setTable("calls")
    model.setRelation(7, QSqlRelation("call_status", "ID", "choice"))
    model.setRelation(3, QSqlRelation("amenities", "ID", "T"))
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Имя")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Номер телефона")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Вопрос")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "Источник")
    model.setHeaderData(5, QtCore.Qt.Horizontal, "Дата звонка")
    model.setHeaderData(7, QtCore.Qt.Horizontal, "Статус звонка")
    model.setHeaderData(6, QtCore.Qt.Horizontal, "Дозвониться")
    model.select()
    ui.table_calls.setModel(model)
    ui.table_calls.setItemDelegate(QSqlRelationalDelegate(ui.table_calls))
    ui.table_calls.setColumnHidden(model.fieldIndex("ID"), True)

    header = ui.table_calls.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)

    return model
    

def read_config():
    config = {'dataBase' : '', 'host' : '', 'port' : 0, 'userName' : '', 'password' : '', 'remind_birthday' : 0, 'remind_ekey' : 0, 'objects_size_editable' : '0'}
    word = ''
    flag = False
    flag_read = False
    temp = ''
    with open(r"C:\Users\Matvey\Desktop\Feniks7\project\config.txt", "r") as f:
        for line in f.readlines():
            for symb in line:
                if flag_read == True:
                    if symb != "'" and word != 'port' and word != 'remind_birthday' and word != 'remind_ekey':
                        config[word] = config[word] + symb
                    elif symb != "'" and (word == 'port' or word == 'remind_birthday' or word == 'remind_ekey'):
                        temp = temp + symb
                    else:
                        flag_read = False
                        if word == 'port' or word == 'remind_birthday' or word == 'remind_ekey':
                            try:
                                config[word] = int(temp)
                            except:
                                pass
                        break
                if symb == ':':
                    if word in config:
                        flag = True
                    else:
                        break
                if symb == "'" and flag == True:
                    flag_read = True
                if flag == False:
                    word = word + symb
            flag = False
            flag_read = False
            word = ''
            temp = ''
        return config

def write_config(dict):
    with open(r"C:\Users\Matvey\Desktop\Feniks7\project\config.txt", "w") as file:
        for key in dict.keys():
            try:
                file.write(key + ': ' + "'" + dict[key] + "'" + "\n")
            except:
                file.write(key + ': ' + "'" + str(dict[key]) + "'" + "\n")


def init_model_tablePlans (ui, db):
    model = QSqlRelationalTableModel(db = db)
    model.setTable("plans")
    model.setRelation(3, QSqlRelation("status_plan", "ID", "status"))
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Событие")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Срок")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Выполнение")
    model.select()
    ui.table_plans.setModel(model)
    ui.table_plans.setColumnHidden(model.fieldIndex("ID"), True)

    header = ui.table_plans.horizontalHeader()       
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    ui.table_plans.setItemDelegate(QSqlRelationalDelegate(ui.table_plans))

    return model
                
def init_comboBox_ekeysModel(ui, db, comboBox):
    model = QSqlTableModel(db = db)
    model.setTable("ekey")

    # model.setFilter('holder=' + str(8) + ' AND statusActive=1')
    # model.select()
    comboBox.setModel(model)
    comboBox.setModelColumn(3)

    return model