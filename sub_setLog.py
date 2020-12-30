# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:03:00 2020

@author: Da YIN
"""

from PyQt5 import QtWidgets, QtCore
from Ui_sub_setLog import Ui_subWin_setLog
from sub_customOutput import sub_custom
from Ui_ValueError import ui_valueError


class sub_setlog(QtWidgets.QWidget, Ui_subWin_setLog):  
    def __init__(self, parent=None):
        super(sub_setlog, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.pb_custom.clicked.connect(self.on_pb_custom_Clicked)
        self.pb_OK.clicked.connect(self.on_pb_OK_Clicked)
        self.pb_Cancel.clicked.connect(self.close)

        self.ChildDialog = sub_custom()
        self.ChildDialog.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        

    def on_pb_custom_Clicked(self):
        self.ChildDialog.show()
        # self.close()
  
    def on_pb_OK_Clicked(self):
        self.i = self.pageCombo.currentIndex()
        self.list_j = [] 
        for j in range(len(self.checkBox[self.i])):
            if self.checkBox[self.i][j].isChecked():
                # print(self.i,j,self.dict_cat[self.i][j][2])
                self.list_j.append(j)
        if self.list_j != []:
            self.isEnabled = True
            self.close()
        else:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请选择当前日志中的参数！！")
  
    
class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        # super(valueError, self).__init__()
        # Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx
        super().__init__() 
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)
        

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    win = sub_setlog()
    win.show()
    sys.exit(app.exec_())