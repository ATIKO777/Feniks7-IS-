# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Matvey\Desktop\Feniks7\add_ekey.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(448, 236)
        Form.setMaximumSize(Form.size())
        Form.setMinimumSize(Form.size())
        self.label_holder = QtWidgets.QLabel(Form)
        self.label_holder.setGeometry(QtCore.QRect(41, 41, 75, 18))
        self.label_holder.setObjectName("label_holder")
        self.holder_text = QtWidgets.QLabel(Form)
        self.holder_text.setGeometry(QtCore.QRect(120, 41, 331, 18))
        self.holder_text.setObjectName("holder_text")
        self.label_date_reg = QtWidgets.QLabel(Form)
        self.label_date_reg.setGeometry(QtCore.QRect(41, 71, 132, 18))
        self.label_date_reg.setObjectName("label_date_reg")
        self.label_date_exp = QtWidgets.QLabel(Form)
        self.label_date_exp.setGeometry(QtCore.QRect(41, 100, 115, 18))
        self.label_date_exp.setObjectName("label_date_exp")
        self.dateEdit_date_reg = QtWidgets.QDateEdit(Form)
        self.dateEdit_date_reg.setGeometry(QtCore.QRect(180, 68, 110, 24))
        self.dateEdit_date_reg.setObjectName("dateEdit_date_reg")
        self.dateEdit_date_reg.setCalendarPopup(True)
        self.dateEdit_date_reg.setDate(QtCore.QDate.currentDate())
        self.dateEdit_date_exp = QtWidgets.QDateEdit(Form)
        self.dateEdit_date_exp.setGeometry(QtCore.QRect(180, 97, 110, 24))
        self.dateEdit_date_exp.setObjectName("dateEdit_date_exp")
        self.dateEdit_date_exp.setCalendarPopup(True)
        self.dateEdit_date_exp.setDate(QtCore.QDate.currentDate())
        self.comboBox_type = QtWidgets.QComboBox(Form)
        self.comboBox_type.setGeometry(QtCore.QRect(42, 130, 219, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setGeometry(QtCore.QRect(105, 160, 93, 28))
        self.pushButton_add.setObjectName("pushButton_add")

        # Добавить icon win
        icon_main = QtGui.QIcon()
        icon_main.addPixmap(QtGui.QPixmap("C:\\Users\\Matvey\\Desktop\\Feniks7\\icons/main_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить электронный ключ"))
        self.label_holder.setText(_translate("Form", "Владелец:"))
        self.holder_text.setText(_translate("Form", "ООО ТЕСТ"))
        self.label_date_reg.setText(_translate("Form", "Дата регистрации:"))
        self.label_date_exp.setText(_translate("Form", "Дата истечения:"))
        self.comboBox_type.setItemText(0, _translate("Form", "Регистрация"))
        self.comboBox_type.setItemText(1, _translate("Form", "Ключ клиента"))
        self.comboBox_type.setItemText(2, _translate("Form", "Доверенность"))
        self.pushButton_add.setText(_translate("Form", "Добавить"))



