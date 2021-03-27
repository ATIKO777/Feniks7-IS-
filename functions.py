import datetime
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from itemTree import *
from dataBase import read_config, write_config
import sys
import os



def remind_birthday (ui, db, cursor, period):
    # Upcoming birthdays
    # sql_request = 'SELECT * FROM  executive_body WHERE  DATE_ADD(birthday, INTERVAL YEAR(CURDATE())-YEAR(birthday) + IF(DAYOFYEAR(CURDATE()) - 1 > DAYOFYEAR(birthday),1,0) YEAR)  BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)'
    sql_request = 'SELECT * FROM  executive_body WHERE  DATE_ADD(birthday, INTERVAL YEAR(CURDATE())-YEAR(birthday) + IF(DAYOFYEAR(CURDATE()) - 1 > DAYOFYEAR(birthday),1,0) YEAR)  BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL ' + str(period) + ' DAY)'

    cursor.execute(sql_request)
    result = cursor.fetchall()
    for exeBody in result:
        text = exeBody[2] + ' ' + exeBody[1][0] + '.' + exeBody[3][0] + '.' + '  ' + exeBody[4].strftime('%d/%m/%Y')
        ui.add_element_list(text, 'gift')

def remind_expEKey (ui, db, cursor, period):
    # sql_request = 'SELECT taxpayer.*, ekey.dateEnd FROM ekey, taxpayer WHERE  (ekey.dateEnd  BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)) AND ekey.holder=taxpayer.ID AND ekey.statusActive=1'
    sql_request = 'SELECT taxpayer.*, ekey.dateEnd FROM ekey, taxpayer WHERE  (ekey.dateEnd  BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL ' + str(period) + ' DAY)) AND ekey.holder=taxpayer.ID AND ekey.statusActive=1'

    cursor.execute(sql_request)
    result = cursor.fetchall()
    for taxpayer in result:
        text = taxpayer[2] + ' ' + taxpayer[1] + '  ' + taxpayer[7].strftime('%d/%m/%Y')
        ui.add_element_list(text, 'ekey')

# def search_calls (ui, model):
#     if ui.checkBox_dateCall.checkState() == 0:
#         if ui.box_question.currentText() == 'Любой':
#             model.setFilter('')
#             model.select()
#         else:
#             model.setFilter("question=" + "'" + ui.box_question.currentText() + "'")
#             model.select()
#     else:
#         Date1_str = ui.dateEdit_requset_call.date()
#         Date1_str = Date1_str.toString(Qt.ISODate)
#         Date2_str = ui.dateEdit_requset_call2.date()
#         Date2_str = Date2_str.toString(Qt.ISODate)
#         where = 'date_call>=' + "'" + Date1_str + "'" + ' AND ' + 'date_call<=' + "'" + Date2_str + "'"
#         if ui.box_question.currentText() == 'Любой':
#             model.setFilter(where)
#             model.select()
#         else:
#             where = where + ' AND question=' + "'" + ui.box_question.currentText() + "'"
#             model.setFilter(where)
#             model.select()

def search_calls (ui, model):
    if ui.checkBox_dateCall.checkState() == 0:
        if ui.box_question.currentText() == 'Любой':
            model.setFilter('')
            model.select()
        else:
            model.setFilter("T=" + "'" + ui.box_question.currentText() + "'")
            model.select()
    else:
        Date1_str = ui.dateEdit_requset_call.date()
        Date1_str = Date1_str.toString(Qt.ISODate)
        Date2_str = ui.dateEdit_requset_call2.date()
        Date2_str = Date2_str.toString(Qt.ISODate)
        where = 'date_call>=' + "'" + Date1_str + "'" + ' AND ' + 'date_call<=' + "'" + Date2_str + "'"
        if ui.box_question.currentText() == 'Любой':
            model.setFilter(where)
            model.select()
        else:
            where = where + ' AND T=' + "'" + ui.box_question.currentText() + "'"
            model.setFilter(where)
            model.select()

def add_call (ui, model):
    rec = model.record()
    rec.setValue(5, QtCore.QDateTime.currentDateTime())
    rec.setValue(6, QtCore.QDate.currentDate())
    rec.setValue(3, 9)
    rec.setValue(7, 100)
    model.insertRecord(-1 , rec) # -1
    search_calls(ui, model)
    ui.table_calls.scrollToBottom()

def Tree_init (ui):
    ui.tree_search.setHeaderHidden(True)
    treeModel = QStandardItemModel()
    rootNode = treeModel.invisibleRootItem()
    return {'model' : treeModel, 'root' : rootNode}

def search (ui, db, tree, cursor, sql_request = None, collapse = True):
    if sql_request == None:
        sql_request = 'SELECT taxpayer.ID, executive_body.ID, taxpayer.title, executive_body.first_name, executive_body.last_name, executive_body.middle_name FROM taxpayer, executive_body, link_payer_exebody WHERE link_payer_exebody.executive_body=executive_body.ID AND link_payer_exebody.taxpayer=taxpayer.ID ORDER BY taxpayer.ID'
    cursor.execute(sql_request)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    temp = -2
    flag = False
    for element in result:
        if temp != element[0]:
            if flag == True:
                tree['root'].appendRow(item)
            item = StandardItem(element[2], 12)
            flag = True


            ui.ids.append([])
            ui.ids[-1].append(element[0])
            ui.ids[-1].append([])
        item_body = StandardItem(element[3] + ' ' + element[4] + ' ' + element[5], 10)
        item.appendRow(item_body)
        ui.ids[-1][-1].append(element[1])
        temp = element[0]
    tree['root'].appendRow(item)

    ui.tree_search.setModel(tree['model'])
    ui.tree_search.expandAll()
    if collapse == True:
        ui.tree_search.collapseAll()

def select (ui, db, cursor, model, modelEkeys):
    ui.current_id = ui.current_Item['id']
    if ui.current_Item['type'] == 'exebody':
        sql_request = 'SELECT * FROM executive_body WHERE ID=' + str(ui.current_Item['id'])
        cursor.execute(sql_request)
        result = cursor.fetchall()

        ui.tabWidget_2.setCurrentIndex(2)
        ui.label_FIO_exe_val.setText(result[0][2] + ' ' + result[0][1] + ' ' + result[0][3])
        try:
            ui.label_birthday_exeBody.setText(result[0][4].strftime('%d/%m/%Y'))
        except:
            ui.label_birthday_exeBody.setText('Нет данных')
        ui.label_address_exe_val.setText(result[0][7])
        ui.label_email_exe_val.setText(result[0][6]) 
        ui.label_phone_exeBody.setText(result[0][5])
    elif ui.current_Item['type'] == 'taxpayer':
        #ui.current_id = ui.current_Item['id']
        sql_request = 'SELECT * FROM taxpayer, ekey WHERE taxpayer.ID=' + str(ui.current_Item['id']) + ' AND ekey.holder=taxpayer.ID AND ekey.statusActive=1'
        cursor.execute(sql_request)
        result = cursor.fetchall()
        modelEkeys.setFilter('holder=' + str(ui.current_id) + ' AND statusActive=1')
        modelEkeys.select()
        # ui.box_ekeys.setModelColumn(3)
        if len(result) != 0:
            ui.tabWidget_2.setCurrentIndex(0)
            ui.label_legalForm.setText(result[0][2])
            ui.label_legalForm_val.setText(result[0][1])
            ui.label_inn_val.setText(str(result[0][3]))
            ui.label_lAddress_val.setText(result[0][4])
            ui.label_email_val.setText(result[0][5])
            ui.label_phone_val.setText(result[0][6])
            ui.label_dateReg_val.setText(result[0][8].strftime('%d/%m/%Y'))
            ui.label_expDate_val.setText(result[0][9].strftime('%d/%m/%Y'))
            ui.label_type_ekey.setText(result[0][10])
            ui.label_dateReg.setText('Дата регистрации:')
            ui.label_expDate.setText('Дата истечения:')
        else:
            sql_request = 'SELECT * FROM taxpayer WHERE taxpayer.ID=' + str(ui.current_Item['id'])
            cursor.execute(sql_request)
            result = cursor.fetchall()
            ui.tabWidget_2.setCurrentIndex(0)
            ui.label_legalForm.setText(result[0][2])
            ui.label_legalForm_val.setText(result[0][1])
            ui.label_inn_val.setText(str(result[0][3]))
            ui.label_lAddress_val.setText(result[0][4])
            ui.label_email_val.setText(result[0][5])
            ui.label_phone_val.setText(result[0][6])
            ui.label_dateReg.setText('Отсутствует')
            ui.label_dateReg_val.setText('')
            ui.label_expDate_val.setText('')
            ui.label_type_ekey.setText('')
            ui.label_expDate.setText('')
        search_service(ui, model, ui.current_id, type_sign = 'open')

# def search_service (ui, model, id, type_sign = 'button'):
#     where = 'client=' + str(id)
#     if type_sign == 'open':
#         model.setFilter(where)
#         model.select()
#         return 0
#     else:
#         if ui.box_title_service.currentText() != 'Любое':
#             where = where + ' AND '
#             where = where + 'title=' + "'" + ui.box_title_service.currentText() + "'"
#         if ui.box_status_pay.currentText() != 'Любой':
#             where = where + ' AND '
#             where = where + 'pay_status='
#             if ui.box_status_pay.currentText() == 'Оплачено':
#                 where = where + '1'
#             elif ui.box_status_pay.currentText() == 'Не оплачено':
#                 where = where + '0'
#         if ui.checkBox_dRequest.checkState() != 0:
#             Date1_str = ui.dateEdit_request.date()
#             Date1_str = Date1_str.toString(Qt.ISODate)
#             Date2_str = ui.dateEdit_request2.date()
#             Date2_str = Date2_str.toString(Qt.ISODate)
#             where = where + ' AND '
#             where = where + 'date_request>=' + "'" + Date1_str + "'" + ' AND ' + 'date_request<=' + "'" + Date2_str + "'"
#         if ui.checkBox_dPay.checkState() != 0:
#             Date1_str = ui.dateEdit_pay.date()
#             Date1_str = Date1_str.toString(Qt.ISODate)
#             Date2_str = ui.dateEdit_pay2.date()
#             Date2_str = Date2_str.toString(Qt.ISODate)
#             where = where + ' AND '
#             where = where + 'date_pay>=' + "'" + Date1_str + "'" + ' AND ' + 'date_pay<=' + "'" + Date2_str + "'"

#         model.setFilter(where) 
#         model.select()

def search_service (ui, model, id, type_sign = 'button'):
    where = 'client=' + str(id)
    if type_sign == 'open':
        model.setFilter(where)
        model.select()
        return 0
    else:
        if ui.box_title_service.currentText() != 'Любое':
            where = where + ' AND '
            where = where + 'T=' + "'" + ui.box_title_service.currentText() + "'"
        if ui.box_status_pay.currentText() != 'Любой':
            where = where + ' AND '
            where = where + 'pay_status='
            if ui.box_status_pay.currentText() == 'Оплачено':
                where = where + '1'
            elif ui.box_status_pay.currentText() == 'Не оплачено':
                where = where + '2'
        if ui.checkBox_dRequest.checkState() != 0:
            Date1_str = ui.dateEdit_request.date()
            Date1_str = Date1_str.toString(Qt.ISODate)
            Date2_str = ui.dateEdit_request2.date()
            Date2_str = Date2_str.toString(Qt.ISODate)
            where = where + ' AND '
            where = where + 'date_request>=' + "'" + Date1_str + "'" + ' AND ' + 'date_request<=' + "'" + Date2_str + "'"
        if ui.checkBox_dPay.checkState() != 0:
            Date1_str = ui.dateEdit_pay.date()
            Date1_str = Date1_str.toString(Qt.ISODate)
            Date2_str = ui.dateEdit_pay2.date()
            Date2_str = Date2_str.toString(Qt.ISODate)
            where = where + ' AND '
            where = where + 'date_pay>=' + "'" + Date1_str + "'" + ' AND ' + 'date_pay<=' + "'" + Date2_str + "'"

        model.setFilter(where) 
        model.select()



def add_service (ui, model):
    rec = model.record()
    rec.setValue(4, QtCore.QDate.currentDate())
    rec.setValue(3, QtCore.QDate.currentDate())
    rec.setValue(2, ui.current_id)
    rec.setValue(1, 9)
    rec.setValue(5, 2)
    model.insertRecord(-1 , rec)
    search_service(ui, model, ui.current_id)
    ui.table_service.scrollToBottom()

def pre_search (ui, db, tree, cursor):
    clear_tree(ui, tree['model'])
    text_search = ui.line_search.text()
    if text_search == '':
        search (ui, db, tree, cursor)
        return 0
    last_name = ''
    first_name = ''
    f = False
    num = True
    for symb in text_search:
        if symb == ' ':
            f = True
        if f == False:
            last_name = last_name + symb
        elif f == True and symb != ' ':
            first_name = first_name + symb
    sql_request_lfn = 'SELECT taxpayer.ID, executive_body.ID, taxpayer.title, executive_body.first_name, executive_body.last_name, executive_body.middle_name FROM taxpayer, executive_body, link_payer_exebody WHERE link_payer_exebody.executive_body=executive_body.ID AND link_payer_exebody.taxpayer=taxpayer.ID AND executive_body.last_name LIKE ' + "'" + last_name + "%'" + ' AND executive_body.first_name LIKE ' + "'" + first_name + "%'"
    sql_request_title = 'SELECT taxpayer.ID, executive_body.ID, taxpayer.title, executive_body.first_name, executive_body.last_name, executive_body.middle_name FROM taxpayer, executive_body, link_payer_exebody WHERE link_payer_exebody.executive_body=executive_body.ID AND link_payer_exebody.taxpayer=taxpayer.ID AND taxpayer.title LIKE ' + "'" + text_search + "%'"
    try:
        int(text_search)
    except :
        num = False
    if num == True:    
        sql_request_inn = 'SELECT taxpayer.ID, executive_body.ID, taxpayer.title, executive_body.first_name, executive_body.last_name, executive_body.middle_name FROM taxpayer, executive_body, link_payer_exebody WHERE link_payer_exebody.executive_body=executive_body.ID AND link_payer_exebody.taxpayer=taxpayer.ID AND taxpayer.inn=' + text_search
        search (ui, db, tree, cursor, sql_request = sql_request_inn)
    
    search (ui, db, tree, cursor, sql_request = sql_request_lfn, collapse = False)
    search (ui, db, tree, cursor, sql_request = sql_request_title)

def clear_tree (ui, model):
    model.removeRows(0, model.rowCount())
    ui.ids = []
    ui.current_Item = {'type' : '', 'id' : 0}
    # ui.current_id = None

def show_holder_for_key (ui, ui_main, db, cursor):
    sql_request = 'SELECT title FROM taxpayer WHERE ID=' + str(ui_main.current_id)
    cursor.execute(sql_request)
    result = cursor.fetchall()
    ui.holder_text.setText(result[0][0])


def add_key_func (ui, ui_main, db, cursor, Form):
    date_reg = ui.dateEdit_date_reg.date()
    date_reg_show = date_reg.toPyDate().strftime('%d/%m/%Y')
    date_reg = date_reg.toString(Qt.ISODate)
    date_exp = ui.dateEdit_date_exp.date()
    date_exp_show = date_exp.toPyDate().strftime('%d/%m/%Y')
    date_exp = date_exp.toString(Qt.ISODate)
    t = ui.comboBox_type.currentText()

    sql_request = 'UPDATE ekey SET statusActive=0 WHERE holder=' + str(ui_main.current_id) + ' AND statusActive=1' + ' AND type=' + "'" + t + "'"
    cursor.execute(sql_request)
    db.commit()

    sql_request = "INSERT INTO ekey (dateReg, dateEnd, type, holder, statusActive) VALUES (%s, %s, %s, %s, %s)"
    val = (date_reg, date_exp, t, ui_main.current_id, 1)
    cursor.execute(sql_request, val)
    db.commit()

    Form.close()
    del Form


    ui_main.label_dateReg_val.setText(date_reg_show)
    ui_main.label_expDate_val.setText(date_exp_show)
    ui_main.label_type_ekey.setText(t)
    ui_main.label_dateReg.setText('Дата регистрации:')
    ui_main.label_expDate.setText('Дата истечения:')

def show_data_for_taxpayer_edit (ui, ui_main, db, cursor):
    sql_request = 'SELECT * FROM taxpayer WHERE ID=' + str(ui_main.current_id)
    cursor.execute(sql_request)
    result = cursor.fetchall()
    
    ui.comboBox_legal_form.setCurrentText(result[0][2])
    ui.lineEdit_title.setText(result[0][1])
    ui.lineEdit_inn.setText(str(result[0][3]))
    ui.lineEdit_address.setText(result[0][4])
    ui.lineEdit_email.setText(result[0][5])
    ui.lineEdit_phone.setText(result[0][6])

def change_data_taxpayer (ui, ui_main, db, cursor, Form):
    legal_form = ui.comboBox_legal_form.currentText()
    title = ui.lineEdit_title.text()
    inn = ui.lineEdit_inn.text()
    try:
        inn = int(inn)
    except:
        ui.lineEdit_inn.setText('')
        ui.lineEdit_inn.setPlaceholderText("Неверный тип данных!")
        return -1
    address = ui.lineEdit_address.text()
    email = ui.lineEdit_email.text()
    phone = ui.lineEdit_phone.text()

    sql_request = 'UPDATE taxpayer SET legal_form=' + "'" + legal_form  + "'" + ', title=' + "'" + title + "'" + ', inn=' + str(inn) + ', legal_address=' + "'" + address + "'" + ', email=' + "'" + email + "'" + ', phoneNum=' + "'" + phone + "'" + ' WHERE ID=' + str(ui_main.current_id)
    cursor.execute(sql_request)
    db.commit()

    Form.close()
    del Form

    ui_main.label_legalForm.setText(legal_form)
    ui_main.label_legalForm_val.setText(title)
    ui_main.label_inn_val.setText(str(inn))
    ui_main.label_lAddress_val.setText(address)
    ui_main.label_email_val.setText(email)
    ui_main.label_phone_val.setText(phone)

def add_taxpayer(ui, db, cursor, Form):
    legal_form = ui.comboBox_legal_form.currentText()
    title = ui.lineEdit_title.text()
    inn = ui.lineEdit_inn.text()
    address = ui.lineEdit_address.text()
    email = ui.lineEdit_email.text()
    phone = ui.lineEdit_phone.text()

    try:
        int(inn)
    except:
        ui.lineEdit_inn.setText('')
        ui.lineEdit_inn.setPlaceholderText('Неверный тип данных!')
        return -1

    sql_request = "INSERT INTO taxpayer (title, legal_form, inn, legal_address, email, phoneNum) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (title, legal_form, inn, address, email, phone)
    cursor.execute(sql_request, val)
    db.commit()

    if legal_form == 'ИП':
        add_exebody_IP(db, cursor, title, address, email, phone, cursor.lastrowid)

    Form.close()
    del Form

def show_data_for_exebody_edit (ui, ui_main, db, cursor):
    sql_request = 'SELECT * FROM executive_body WHERE ID=' + str(ui_main.current_id)
    cursor.execute(sql_request)
    result = cursor.fetchall()

    ui.lineEdit.setText(result[0][2])
    ui.lineEdit_2.setText(result[0][1])
    ui.lineEdit_3.setText(result[0][3])
    try:
        ui.dateEdit.setDate(result[0][4])
    except:
        ui.dateEdit.setDate(QtCore.QDate.currentDate())
    ui.lineEdit_4.setText(result[0][7])
    ui.lineEdit_5.setText(result[0][6])
    ui.lineEdit_6.setText(result[0][5])

def change_data_exebody(ui, id_exebody, Form, db, cursor):
    last_name = ui.lineEdit.text()
    first_name = ui.lineEdit_2.text()
    middle_name = ui.lineEdit_3.text()
    birthday = ui.dateEdit.date()
    birthday = birthday.toString(Qt.ISODate)
    address = ui.lineEdit_4.text()
    email = ui.lineEdit_5.text()
    phone = ui.lineEdit_6.text()

    sql_request = 'UPDATE executive_body SET first_name=' + "'" + first_name  + "'" + ', last_name=' + "'" + last_name + "'" + ', middle_name=' + "'" + middle_name + "'" + ', birthday=' + "'" + birthday + "'" + ', phoneNum=' + "'" + phone + "'" + ', email=' + "'" + email + "'" + ', home_address=' + "'" + address + "'" + ' WHERE ID=' + str(id_exebody)
    cursor.execute(sql_request)
    db.commit()

    Form.close()
    del Form



def getValueComboBoxTaxpayer (comboBox):
    comboBox.setModelColumn(0)
    id_taxpayer = int(comboBox.currentText())
    comboBox.setModelColumn(1)

    return id_taxpayer

def newLink_exebody_taxpayer(ui, id_exebody, db, cursor, model):
    id_taxpayer = getValueComboBoxTaxpayer(ui.comboBox_taxpayer)

    sql_request = "INSERT INTO link_payer_exebody (executive_body, taxpayer) VALUES (%s, %s)"
    val = (id_exebody, id_taxpayer)
    cursor.execute(sql_request, val)
    db.commit()

    model.setQuery(model.query().lastQuery())

def add_exebody(db, cursor):
    sql_request = "INSERT INTO executive_body (last_name) VALUES (%s)"
    val = ('',)
    cursor.execute(sql_request, val)
    db.commit()

    id_exebody = cursor.lastrowid
    return id_exebody

def add_exebody_cancel(db, cursor, id_exebody, Form):
    sql_request = 'DELETE FROM link_payer_exebody WHERE executive_body=' + str(id_exebody)
    cursor.execute(sql_request)
    db.commit()

    sql_request = 'DELETE FROM executive_body WHERE ID=' + str(id_exebody)
    cursor.execute(sql_request)
    db.commit()

    Form.close()
    del Form

def add_exebody_IP (db, cursor, title, address, email, phone, id_taxpayer):
    name = ['', '', '']
    j = 0
    for i in range(len(title)):
        if title[i] == ' ':
            j = j + 1
            i = i + 1
        else:
            name[j] = name[j] + title[i]
    
    sql_request = "INSERT INTO executive_body (last_name, first_name, middle_name, phoneNum, email, home_address) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name[0], name[1], name[2], phone, email, address)
    cursor.execute(sql_request, val)
    db.commit()

    id_exebody = cursor.lastrowid

    sql_request = "INSERT INTO link_payer_exebody (executive_body, taxpayer) VALUES (%s, %s)"
    val = (id_exebody, id_taxpayer)
    cursor.execute(sql_request, val)
    db.commit()

def open_adv_search(ui):
    ui.tabWidget_2.setCurrentIndex(1)

def search_ekey (ui, model):
    sql_request = 'SELECT taxpayer.title, ekey.* FROM ekey, taxpayer WHERE ekey.holder=taxpayer.ID'
    if ui.checkBox_ekey_reg_searchAdv.checkState() == 2:
        Date1_str = ui.dateEdit_ekey_reg.date()
        Date1_str = Date1_str.toString(Qt.ISODate)
        Date2_str = ui.dateEdit_ekey_reg2.date()
        Date2_str = Date2_str.toString(Qt.ISODate)

        sql_request = sql_request + ' AND ekey.dateReg>=' + "'" + Date1_str + "'" + ' AND ekey.dateReg<=' + "'" + Date2_str + "'"
    if ui.checkBox_ekey_exp_searchAdv.checkState() == 2:
        Date1_str = ui.dateEdit_ekey_exp.date()
        Date1_str = Date1_str.toString(Qt.ISODate)
        Date2_str = ui.dateEdit_ekey_exp2.date()
        Date2_str = Date2_str.toString(Qt.ISODate)

        sql_request = sql_request + ' AND ekey.dateEnd>=' + "'" + Date1_str + "'" + ' AND ekey.dateEnd<=' + "'" + Date2_str + "'"
    if ui.box_statusActive.currentText() != 'Любой':
        if ui.box_statusActive.currentText() == 'Действующий':
            sql_request = sql_request + ' AND ekey.statusActive=1'
        elif ui.box_statusActive.currentText() == 'Недействующий':
            sql_request = sql_request + ' AND ekey.statusActive=0'
    if ui.box_typeEkey.currentText() != 'Тип (Любой)':
        sql_request = sql_request + ' AND ekey.type=' + "'" + ui.box_typeEkey.currentText() + "'"
    
    model.setQuery(sql_request)

def search_exebody_advSearch (ui, model):
    if ui.checkBox_exebody_searchAdv.checkState() == 2:
        Date1_str = ui.dateEdit_birthday.date()
        Date1_str = Date1_str.toString(Qt.ISODate)
        Date2_str = ui.dateEdit_birthday2.date()
        Date2_str = Date2_str.toString(Qt.ISODate)

        sql_request = 'SELECT * FROM executive_body WHERE  DATE_ADD(birthday, INTERVAL YEAR(' + "'" + Date1_str + "'" +  ')-YEAR(birthday) + IF(DAYOFYEAR(' + "'" + Date1_str + "'" + ') - 1 > DAYOFYEAR(birthday),1,0) YEAR)  BETWEEN ' + "'" + Date1_str + "'" + ' AND ' + "'" + Date2_str + "'"
        model.setQuery(sql_request)
    else:
        model.setQuery('SELECT * FROM executive_body')

def show_settings(ui, config):
    ui.lineEdit_db.setText(config['dataBase'])
    ui.lineEdit_host.setText(config['host'])
    ui.lineEdit_port.setText(str(config['port']))
    ui.lineEdit_userName.setText(config['userName'])
    ui.lineEdit_password.setText(config['password'])

    ui.lineEdit_birthday.setText(str(config['remind_birthday']))
    ui.lineEdit_ekey.setText(str(config['remind_ekey']))

def close_settings(Form):
    Form.close()
    del Form

def save_settings(ui, Form):
    config = {'dataBase' : '', 'host' : '', 'port' : 0, 'userName' : '', 'password' : '', 'remind_birthday' : 0, 'remind_ekey' : 0}

    config['dataBase'] = ui.lineEdit_db.text()
    config['host'] = ui.lineEdit_host.text()
    try:
        config['port'] = int(ui.lineEdit_port.text())
    except:
        ui.lineEdit_port.setText('')
        ui.lineEdit_port.setPlaceholderText("Неверный тип данных!")
        return -1

    config['userName'] = ui.lineEdit_userName.text()
    config['password'] = ui.lineEdit_password.text()

    try:
        config['remind_birthday'] = int(ui.lineEdit_birthday.text())
    except:
        ui.lineEdit_birthday.setText('')
        ui.lineEdit_birthday.setPlaceholderText("Неверный тип данных!")
        return -1

    try:
        config['remind_ekey'] = int(ui.lineEdit_ekey.text())
    except:
        ui.lineEdit_ekey.setText('')
        ui.lineEdit_ekey.setPlaceholderText("Неверный тип данных!")
        return -1

    write_config(config)
    close_settings(Form)

def add_taxpayer_for_graph(ui, db, cursor, model):
    id_taxpayer = getValueComboBoxTaxpayer(ui.comboBox)

    sql_request = 'SELECT COUNT(*) as count FROM taxpayer, service WHERE service.client=taxpayer.ID AND service.pay_status=2 AND taxpayer.ID=' + str(id_taxpayer)
    cursor.execute(sql_request)
    result = cursor.fetchall()
    count_nopay = result[0][0]

    sql_request = 'SELECT COUNT(*) as count FROM taxpayer, service WHERE service.client=taxpayer.ID AND service.pay_status=1 AND taxpayer.ID=' + str(id_taxpayer)
    cursor.execute(sql_request)
    result = cursor.fetchall()
    count_pay = result[0][0]

    sql_request = "INSERT INTO graphique_taxpayer (taxpayer, count_pay, count_nopay) VALUES (%s, %s, %s)"
    val = (id_taxpayer, count_pay, count_nopay)
    cursor.execute(sql_request, val)
    db.commit()

    model.select()



def delete_empty_str(db, cursor):
    sql_request = 'SELECT executive_body.ID FROM executive_body LEFT JOIN link_payer_exebody ON executive_body.ID=link_payer_exebody.executive_body WHERE link_payer_exebody.executive_body IS NULL'
    cursor.execute(sql_request)
    result = cursor.fetchall()

    if len(result) != 0:
        sql_request = 'DELETE FROM executive_body WHERE ID IN ('
        for element in result:
            if element[0] == result[-1][0]:
                sql_request = sql_request + str(element[0]) + ')'
            else: 
                sql_request = sql_request + str(element[0]) + ','

        cursor.execute(sql_request)
        db.commit()

def connect_(app, ui, Form):
    save_settings(ui, Form)
    app.closeAllWindows()
    os.system(r'C:\Users\Matvey\Desktop\Feniks7\TEST\graph\toExe\dist\main\main.exe')

def delete_all_str_grapgh(db, cursor):
    sql_request = 'DELETE FROM graphique_taxpayer'
    cursor.execute(sql_request)
    db.commit()


def search_plan (ui, model):
    if ui.checkBox_datePlan.checkState() == 0:
        if ui.box_status_plan.currentText() == 'Любой':
            model.setFilter('')
            model.select()
        else:
            model.setFilter("status=" + "'" + ui.box_status_plan.currentText() + "'")
            model.select()
    else:
        Date1_str = ui.dateEdit_deadline.date()
        Date1_str = Date1_str.toString(Qt.ISODate)
        Date2_str = ui.dateEdit_deadline2.date()
        Date2_str = Date2_str.toString(Qt.ISODate)
        where = 'deadline>=' + "'" + Date1_str + "'" + ' AND ' + 'deadline<=' + "'" + Date2_str + "'"
        if ui.box_status_plan.currentText() == 'Любой':
            model.setFilter(where)
            model.select()
        else:
            where = where + ' AND status=' + "'" + ui.box_status_plan.currentText() + "'"
            model.setFilter(where)
            model.select()

def add_plan (ui, model):
    rec = model.record()
    rec.setValue(2, QtCore.QDate.currentDate())
    rec.setValue(3, 2)
    model.insertRecord(-1 , rec) # -1
    search_plan(ui, model)
    ui.table_plans.scrollToBottom()

def change_show_ekey(ui, db, cursor):
    type_key = ui.box_ekeys.currentText()

    sql_request = 'SELECT * FROM ekey WHERE holder=' + str(ui.current_id) + ' AND ' + 'statusActive=1' + ' AND ' + 'type=' + "'" + type_key + "'"
    cursor.execute(sql_request)
    result = cursor.fetchall()

    ui.label_dateReg_val.setText(result[0][1].strftime('%d/%m/%Y'))
    ui.label_expDate_val.setText(result[0][2].strftime('%d/%m/%Y'))
    ui.label_type_ekey.setText(result[0][3])
    ui.label_dateReg.setText('Дата регистрации:')
    ui.label_expDate.setText('Дата истечения:')
