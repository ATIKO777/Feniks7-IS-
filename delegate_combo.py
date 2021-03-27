from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor

class ComboDelegate(QItemDelegate):
    editorItems=['Бухгалтерия', 'Печать','Ликвидация', 'Регистрация', 'Изменение юр. адреса', 'Смена директора', 'Смена учредителя', 'Смена ОКВЭД']
    height = 25
    width = 249
    def createEditor(self, parent, option, index):
        editor = QListWidget(parent)
        # editor.addItems(self.editorItems)
        # editor.setEditable(True)
        editor.currentItemChanged.connect(self.currentItemChanged)
        return editor

    def setEditorData(self,editor,index):
        z = 0
        for item in self.editorItems:
            ai = QListWidgetItem(item)
            editor.addItem(ai)
            if item == index.data():
                editor.setCurrentItem(editor.item(z))
            z += 1
        x = QCursor().pos().x()
        y = QCursor().pos().y()
        if y >= 813:
            editor.setGeometry(497, y - 450, self.width, 20*len(self.editorItems))
        else:
            editor.setGeometry(497, y - 275, self.width, 20*len(self.editorItems))

    def setModelData(self, editor, model, index):
        editorIndex=editor.currentIndex()
        text=editor.currentItem().text() 
        model.setData(index, text)
        # print '\t\t\t ...setModelData() 1', text

    @pyqtSlot()
    def currentItemChanged(self): 
        self.commitData.emit(self.sender())

class ComboDelegateForService(QItemDelegate):
    editorItems=['Бухгалтерия', 'Печать','Ликвидация', 'Регистрация', 'Изменение юр. адреса', 'Смена директора', 'Смена учредителя', 'Смена ОКВЭД']
    height = 25
    width = 255
    def createEditor(self, parent, option, index):
        editor = QListWidget(parent)
        # editor.addItems(self.editorItems)
        # editor.setEditable(True)
        editor.currentItemChanged.connect(self.currentItemChanged)
        return editor

    def setEditorData(self,editor,index):
        z = 0
        for item in self.editorItems:
            ai = QListWidgetItem(item)
            editor.addItem(ai)
            if item == index.data():
                editor.setCurrentItem(editor.item(z))
            z += 1
        x = QCursor().pos().x()
        y = QCursor().pos().y()
        if y >= 810:
            editor.setGeometry(0, y - 780, self.width, 20*len(self.editorItems))
        else:
            editor.setGeometry(0, y - 625, self.width, 20*len(self.editorItems))

    def setModelData(self, editor, model, index):
        editorIndex=editor.currentIndex()
        text=editor.currentItem().text() 
        model.setData(index, text)
        # print '\t\t\t ...setModelData() 1', text

    @pyqtSlot()
    def currentItemChanged(self): 
        self.commitData.emit(self.sender())