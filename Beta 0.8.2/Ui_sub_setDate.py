# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 17:30:08 2020

本界面用于输入数据分析的日志文档起止日期，包括：
四个文本行，四个标签，四个按钮。

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QWidget, QLabel, QPushButton, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_sub_Date(object):
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("日期设置")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        # Dialog.resize(500, 400)
        Dialog.setFixedSize(500, 400)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建文本行
        self.lineEdit_year = QLineEdit(Dialog)
        self.lineEdit_month = QLineEdit(Dialog)
        self.lineEdit_day1 = QLineEdit(Dialog)
        self.lineEdit_day2 = QLineEdit(Dialog)
        # 创建按钮
        self.PbCal1 = QPushButton(u"选择日期", Dialog)
        # self.PbCal1.setObjectName("PbCal1")
        self.PbCal2 = QPushButton(u"选择日期", Dialog)
        self.PbOK = QPushButton(u"确定", Dialog)
        self.PbCancel = QPushButton(u"取消", Dialog)        
        # 添加到布局
        layout.addWidget(self.dateTapUI(Dialog))
        layout.addWidget(self.PbOK)
        layout.addWidget(self.PbCancel)  
        
    def dateTapUI(self, Dialog):
        """创建日期键入布局"""
        dateTap = QWidget(Dialog)
        layout = QHBoxLayout(Dialog)
        layout.addWidget(self.lineEdit_year)
        layout.addWidget(QLabel("年  "))
        layout.addWidget(self.lineEdit_month)
        layout.addWidget(QLabel("月  "))
        layout.addWidget(self.sub_dateTapUI(Dialog))
        dateTap.setLayout(layout)
        return dateTap
    
    def sub_dateTapUI(self, Dialog):
        sub_dateTap = QWidget(Dialog)
        layout = QGridLayout()
        layout.addWidget(self.lineEdit_day1,0,0)
        layout.addWidget(QLabel("日起  "),0,1)
        layout.addWidget(self.PbCal1,0,2)
        layout.addWidget(self.lineEdit_day2,1,0)
        layout.addWidget(QLabel("日止  "),1,1)
        layout.addWidget(self.PbCal2,1,2)        
        sub_dateTap.setLayout(layout)
        return sub_dateTap

    
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_sub_Date()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())