# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pickCalendar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sub_calendar(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("选择日期")
        Dialog.setWindowIcon(QtGui.QIcon("ship.svg"))
        # Dialog.resize(500, 400)
        Dialog.setFixedSize(500, 400)
        Dialog.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QtWidgets.QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建日历控件
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setGridVisible(True)
        # self.calendarWidget.clicked[QtCore.QDate].connect(self.showDate)
        # 创建标签控件
        self.label = QtWidgets.QLabel(Dialog)
        date = self.calendarWidget.selectedDate()
        self.label.setText("选取日期：" + date.toString())
        # 创建按钮
        self.PbOK = QtWidgets.QPushButton("确定", Dialog)
        self.PbCancel = QtWidgets.QPushButton("取消", Dialog)
        # 添加到布局
        layout.addWidget(self.calendarWidget)
        layout.addWidget(self.label)
        layout.addWidget(self.PbOK)
        layout.addWidget(self.PbCancel)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_sub_calendar()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
