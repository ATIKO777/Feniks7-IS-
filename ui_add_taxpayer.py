# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Matvey\Desktop\Feniks7\add_taxpayer.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(489, 231)
        Form.setMaximumSize(Form.size())
        Form.setMinimumSize(Form.size())
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setGeometry(QtCore.QRect(260, 178, 93, 28))
        self.pushButton_add.setMaximumSize(QtCore.QSize(220, 16777215))
        self.pushButton_add.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_add.setObjectName("pushButton_add")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(21, 21, 441, 150))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.comboBox_legal_form = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_legal_form.setObjectName("comboBox_legal_form")
        self.comboBox_legal_form.addItem("")
        self.comboBox_legal_form.addItem("")
        self.comboBox_legal_form.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.comboBox_legal_form)
        self.lineEdit_title = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_title)
        self.label_inn = QtWidgets.QLabel(self.layoutWidget)
        self.label_inn.setObjectName("label_inn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_inn)
        self.lineEdit_inn = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_inn.setObjectName("lineEdit_inn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_inn)
        self.label_address = QtWidgets.QLabel(self.layoutWidget)
        self.label_address.setObjectName("label_address")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_address)
        self.lineEdit_address = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_address)
        self.label_email = QtWidgets.QLabel(self.layoutWidget)
        self.label_email.setObjectName("label_email")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_email)
        self.lineEdit_email = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_email)
        self.label_phone = QtWidgets.QLabel(self.layoutWidget)
        self.label_phone.setObjectName("label_phone")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_phone)
        self.lineEdit_phone = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_phone)

        # Добавить icon win
        icon_main = QtGui.QIcon()
        icon_main.addPixmap(QtGui.QPixmap("C:\\Users\\Matvey\\Desktop\\Feniks7\\icons/main_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить налогоплательщика"))
        self.pushButton_add.setText(_translate("Form", "Добавить"))
        self.comboBox_legal_form.setItemText(0, _translate("Form", "АО"))
        self.comboBox_legal_form.setItemText(1, _translate("Form", "ООО"))
        self.comboBox_legal_form.setItemText(2, _translate("Form", "ИП"))
        self.label_inn.setText(_translate("Form", "ИНН:"))
        self.label_address.setText(_translate("Form", "Юридический адрес:"))
        self.label_email.setText(_translate("Form", "E-mail:"))
        self.label_phone.setText(_translate("Form", "Номер телефона:"))


