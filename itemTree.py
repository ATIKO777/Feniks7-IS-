from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont

class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False):
        super().__init__()
        
        fnt = QFont('Calibri Light', font_size)
        # fnt.setBold(set_bold)
        self.setEditable(False)
        self.setFont(fnt)
        self.setText(txt)