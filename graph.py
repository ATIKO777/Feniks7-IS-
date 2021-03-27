# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore
from dataBase import init_comboBox_taxpayers_for_exebodyEdit, init_query_for_graph
from functions import add_taxpayer_for_graph
from PyQt5.QtGui import QCursor

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):
    cell_selected = None
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi(r"C:\Users\Matvey\Desktop\Feniks7\TEST\graph\qt_designer.ui",self)

        self.setWindowTitle("Feniks-7 || Построение графиков")
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.delete_item = QAction('Удалить')
        self.delete_all = QAction('Удалить всё')
        self.tableView.customContextMenuRequested.connect(self.show_contextMenu)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        icon_main = QtGui.QIcon()
        icon_main.addPixmap(QtGui.QPixmap("C:\\Users\\Matvey\\Desktop\\Feniks7\\icons/main_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon_main)
    

    def show_contextMenu(self, pos):
        menu = QMenu(self.tableView)
        deleteAction = menu.addAction(self.delete_item)
        deleteAllAction = menu.addAction(self.delete_all)
        menu.exec_(QCursor().pos())

    def delete_item_graph (self, model, cell):
        # print(cell.row())
        model.removeRow(cell.row())
        model.select()

    def delete_all_items (self, model):
        for i in range(model.rowCount()):
            model.removeRow(i)
        model.select()

    def get_cell (self, cell):
       self.cell_selected = cell


    def update_graph(self, db, cursor):

        # fs = 500
        # f = random.randint(1, 100)
        # ts = 1/fs
        # length_of_signal = 100
        # t = np.linspace(0,1,length_of_signal)
        
        # cosinus_signal = np.cos(2*np.pi*f*t)
        # sinus_signal = np.sin(2*np.pi*f*t)

        # self.MplWidget.canvas.axes.clear()
        # self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget.canvas.draw()

        x_labels = []
        y = []
        z = []
        sql_request = 'SELECT graphique_taxpayer.*, taxpayer.title FROM graphique_taxpayer, taxpayer WHERE graphique_taxpayer.taxpayer=taxpayer.ID'
        cursor.execute(sql_request)
        result = cursor.fetchall()

        for element in result:
            x_labels.append(element[4])
            y.append(element[2])
            z.append(element[3])

        # x_labels = ['Первый', 'Второй', 'Третий', 'Четвертый', 'Пятый', 'Шестой', 'Седьмой', 'Восьмой', 'Девятый', 'Десятый']
        x = np.arange(len(x_labels))
        # y = [32, 24, 54, 54, 12, 43, 76, 89, 1, 11]
        # z = [11, 13, 22, 15, 32, 12, 11, 23, 21, 24]

        l = []
        for i in range(len(y)):
            l.append(y[i] + z[i])


        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.bar(x, l, label='Кол-во неоплаченных услуг', color='firebrick')
        self.MplWidget.canvas.axes.bar(x, y, label='Кол-во оплаченных услуг', color='steelblue')
        self.MplWidget.canvas.axes.legend()

        self.MplWidget.canvas.axes.set_xticks(x)
        self.MplWidget.canvas.axes.set_xticklabels(x_labels)

        self.MplWidget.fig.autofmt_xdate(rotation=45)

        # for i, a in enumerate(y):
        #     self.MplWidget.canvas.axes.text(i - 0.14, a, str(a), color='black')

        # for i, a in enumerate(z):
        #     self.MplWidget.canvas.axes.text(i - 0.14, l[i], str(a), color='black')

        self.MplWidget.canvas.draw()


def open_plot_graph(Qdb, db, cursor):
    global window
    # app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    # app.exec_()

    comboBoxModel = init_comboBox_taxpayers_for_exebodyEdit(window, Qdb, window.comboBox)
    tableViewModel = init_query_for_graph(window, Qdb)
    window.button_add.clicked.connect(lambda: add_taxpayer_for_graph(window, db, cursor, tableViewModel))
    window.tableView.pressed.connect(window.get_cell)
    window.delete_item.triggered.connect(lambda: window.delete_item_graph(tableViewModel, window.cell_selected))
    window.delete_all.triggered.connect(lambda: window.delete_all_items(tableViewModel))

    window.button_plot.clicked.connect(lambda: window.update_graph(db, cursor))