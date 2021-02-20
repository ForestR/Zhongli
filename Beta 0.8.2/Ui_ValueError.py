# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 17:08:28 2020

@author: Da YIN
"""

from PyQt5 import QtWidgets, QtGui, QtCore

class ui_valueError(object):
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("ValueError")
        Dialog.setWindowIcon(QtGui.QIcon("ship.svg"))
        # Dialog.resize(200,100)
        Dialog.setFixedSize(200,100)
        Dialog.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QtWidgets.QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建标签
        self.label_Tips = QtWidgets.QLabel("请输入正确数据！！")
        self.label_Tips.setAlignment(QtCore.Qt.AlignCenter)  # 居中
        # 创建按钮
        self.PbOK = QtWidgets.QPushButton("确定", Dialog)
        # 添加到布局
        layout.addWidget(self.label_Tips)
        layout.addWidget(self.PbOK)
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    UI = ui_valueError()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
