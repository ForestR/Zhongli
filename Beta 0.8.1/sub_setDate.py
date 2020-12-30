# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 08:41:37 2020

@author: Da YIN
"""

from PyQt5 import QtCore, QtWidgets
from Ui_sub_setDate import Ui_sub_Date
from Ui_sub_pickCalendar import Ui_sub_calendar
from Ui_ValueError import ui_valueError


class sub_setdate(QtWidgets.QWidget, Ui_sub_Date):  
    def __init__(self, parent=None):
        super(sub_setdate, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.PbCal1.clicked.connect(self.onPbCal1Clicked)
        self.PbCal2.clicked.connect(self.onPbCal2Clicked)
        self.PbOK.clicked.connect(self.onPbOKClicked)
        self.PbCancel.clicked.connect(self.close)
        self.ChildDialog = sub_calendar() # 一定要在主窗口类的初始化函数中对子窗口进行实例化
        self.ChildDialog.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    
    def onPbCal1Clicked(self):
        self.ChildDialog.show()
        self.ChildDialog._signal.connect(self.getData1) # 连接信号
        try:
            self.ChildDialog._signal.disconnect(self.getData2) # 阻断信号
        except TypeError:
            pass
        
    def onPbCal2Clicked(self):
        self.ChildDialog.show()
        self.ChildDialog._signal.connect(self.getData2)
        try:
            self.ChildDialog._signal.disconnect(self.getData1)
        except TypeError:
            pass
        
    def getData1(self, parameter):
        self.lineEdit_year.setText(str(parameter.year()))
        self.lineEdit_month.setText(str(parameter.month()))
        self.lineEdit_day1.setText(str(parameter.day()))

    def getData2(self, parameter):
        self.lineEdit_year.setText(str(parameter.year()))
        self.lineEdit_month.setText(str(parameter.month()))
        self.lineEdit_day2.setText(str(parameter.day()))
        
    def onPbOKClicked(self):
        try:
            self.year = int(self.lineEdit_year.text())
            self.month = int(self.lineEdit_month.text())
            self.day1 = int(self.lineEdit_day1.text())
            self.day2 = int(self.lineEdit_day2.text())
            if (self.day1 <= self.day2 and self.year > 2000 and 
                self.month > 0 and self.month <= 12):
                self.isEnabled = True
                self.close()
            else:
                self.isEnabled = False
                self.ErrorDialog.show() # 可以传递文本到标签
                self.ErrorDialog.label_Tips.setText("请检查日期输入！！")
        except ValueError:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请检查日期输入！！")


class sub_calendar(QtWidgets.QWidget, Ui_sub_calendar):
    def __init__(self):
        super(sub_calendar, self).__init__()
        self.setupUi(self)
        self.calendarWidget.clicked[QtCore.QDate].connect(self.showDate)
        self.PbOK.clicked.connect(self.slot_cal)
        self.PbOK.clicked.connect(self.close)
        self.PbCancel.clicked.connect(self.close)
        
    def showDate(self):
        date = self.calendarWidget.selectedDate()
        self.label.setText("选取日期：" + date.toString())

    # 定义信号
    _signal = QtCore.pyqtSignal(QtCore.QDate)
    # 定义槽函数        
    def slot_cal(self):
        date = self.calendarWidget.selectedDate()
        # 发送信号
        self._signal.emit(date)


class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)
        

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    win = sub_setdate()
    win.show()
    sys.exit(app.exec_())
