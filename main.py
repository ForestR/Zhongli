# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 16:33:13 2020

@author: Da YINs
"""

from PyQt5 import QtCore, QtWidgets
from Ui_mainWin import Ui_main
from sub_visiualization import sub_visiual
from sub_stateJudgement import sub_state
from Ui_ValueError import ui_valueError

class mainWin(QtWidgets.QMainWindow, Ui_main):
    
    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.action_helpDoc.triggered.connect(self.on_action_helpDoc_triggered)
        self.action_author.triggered.connect(self.on_action_author_triggered)
        self.pb_sub_visiual.clicked.connect(self.on_pb_sub_visiual_Clicked)
        self.pb_sub_state.clicked.connect(self.on_pb_sub_state_Clicked)
        self.pb_Cancel.clicked.connect(self.on_pb_Cancel_Clicked)
        
        
        self.ChildDialog1 = sub_visiual()
        self.ChildDialog1.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口        
        self.ChildDialog2 = sub_state()
        self.ChildDialog2.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        

    def on_action_helpDoc_triggered(self):
        self.ErrorDialog.show()
        self.ErrorDialog.setWindowTitle('帮助文档')
        self.ErrorDialog.setFixedSize(350,100)
        self.ErrorDialog.label_Tips.setText('敬请期待！')
        
    def on_action_author_triggered(self):
        self.ErrorDialog.show()
        self.ErrorDialog.setWindowTitle('关于作者')
        self.ErrorDialog.setFixedSize(350,200)
        self.ErrorDialog.label_Tips.setText('Zhongli 0.8.1\n\n作者：殷达，汪望明\n\n单位：中交广航局 技术中心\n\n邮箱：1220645510@qq.com')
        
    def on_pb_sub_visiual_Clicked(self):
        self.ChildDialog1.show()

    def on_pb_sub_state_Clicked(self):
        self.ChildDialog2.show()
        
    def on_pb_Cancel_Clicked(self):
        self.close()

class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = mainWin()
    win.show()
    sys.exit(app.exec_())