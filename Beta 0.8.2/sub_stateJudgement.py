# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:10:53 2020

@author: Da YIN
"""

from PyQt5 import QtCore, QtWidgets
from Ui_sub_stateJudgement import Ui_sub_state
from sub_setDate import sub_setdate
from sub_setFilePath import sub_filepath
from Ui_ValueError import ui_valueError
# import pandas as pd 
from GPrintf import getDataFrame


class sub_state(QtWidgets.QWidget, Ui_sub_state):
    
    def __init__(self, parent=None):
        super(sub_state, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.pb_setFilePath.clicked.connect(self.on_pb_setFilePath_Clicked)
        self.pb_setDate.clicked.connect(self.on_pb_setDate_Clicked)
        self.pb_getCSV.clicked.connect(self.on_pb_getCSV_Clicked)
        self.pb_Cancel.clicked.connect(self.on_pb_Cancel_Clicked)
        
        self.ChildDialog1 = sub_filepath()
        self.ChildDialog1.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口        
        self.ChildDialog2 = sub_setdate()
        self.ChildDialog2.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ErrorDialog.setWindowTitle('警告')


    def on_pb_setFilePath_Clicked(self):
        self.ChildDialog1.show()

    def on_pb_setDate_Clicked(self):
        self.ChildDialog2.show()
        
    def on_pb_getCSV_Clicked(self):
        if (self.ChildDialog1.isEnabled and self.ChildDialog2.isEnabled):
            self.isEnabled = True            
            self.getMoment()

        else:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请检查文件【设置】！！")

    def on_pb_Cancel_Clicked(self):
        self.close()        

    def getMoment(self):
        dir_import = self.ChildDialog1.dir_import # 有待优化
        dir_export = self.ChildDialog1.dir_export
        year = self.ChildDialog2.year
        month = self.ChildDialog2.month
        day1 = self.ChildDialog2.day1
        day2 = self.ChildDialog2.day2
        
        for day in range(day1, 1+day2):
            df = getDataFrame(year,month,day,dir_import)
            
            str1 = "%04d_%02d_%02d_Moment"%(year,month,day)
            filename = r''+dir_export+"/"+str1+".csv"
            col_name = df.columns.tolist()
            df.to_csv(filename,encoding="utf_8_sig",index=False,
                      sep=',',columns=col_name)


class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = sub_state()
    win.show()
    sys.exit(app.exec_())