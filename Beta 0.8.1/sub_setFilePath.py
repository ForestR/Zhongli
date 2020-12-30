# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:59:11 2020

@author: Da YIN
"""

from PyQt5 import QtWidgets, QtCore
from Ui_sub_setFilePath import Ui_subWin_filepath
from Ui_ValueError import ui_valueError


class sub_filepath(QtWidgets.QWidget, Ui_subWin_filepath):  
    def __init__(self, parent=None):
        super(sub_filepath, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.lineEdit_import.setText("C:/")
        self.lineEdit_export.setText("C:/")
        self.fileDialog = QtWidgets.QFileDialog()
        self.pb_import.clicked.connect(self.on_pb_import_Clicked)
        self.pb_export.clicked.connect(self.on_pb_export_Clicked)
        self.pb_OK.clicked.connect(self.on_pb_OK_Clicked)
        self.pb_Cancel.clicked.connect(self.close)
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        
        
    def on_pb_import_Clicked(self):
        # url = self.fileDialog.getOpenFileUrls()      # 返回选中的多个文件路径
        Dir = self.fileDialog.getExistingDirectory()   # 返回选中的文件夹路径
        self.lineEdit_import.setText(Dir)
        
    def on_pb_export_Clicked(self):
        Dir = self.fileDialog.getExistingDirectory()
        self.lineEdit_export.setText(Dir) 
  
    def on_pb_OK_Clicked(self):

        try:
            self.dir_import = self.lineEdit_import.text()
            self.dir_export = self.lineEdit_export.text()

            if self.dir_import != "" and self.dir_export != "":
                self.isEnabled = True
                self.close()
            else:
                self.isEnabled = False
                self.ErrorDialog.show() # 可以传递文本到标签
                self.ErrorDialog.label_Tips.setText("请检查文件路径！！")
        except ValueError:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请检查文件路径！！")


class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)
        

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    win = sub_filepath()
    win.show()
    sys.exit(app.exec_())
