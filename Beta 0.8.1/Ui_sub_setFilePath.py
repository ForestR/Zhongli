# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:21:35 2020

本界面用于设置导入导出地址，包括：
两个标签，两个文本行和四个按钮。

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Ui_subWin_filepath(object):
        
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("目录设置")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        Dialog.setFixedSize(500, 400)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建标签
        self.label_import = QLabel("导入")
        self.label_export = QLabel("导出")
        # 创建文本行
        self.lineEdit_import = QLineEdit(Dialog)
        self.lineEdit_export = QLineEdit(Dialog)
        # 创建按钮
        self.pb_import = QPushButton("选择目录", Dialog)
        self.pb_export = QPushButton("选择目录", Dialog)
        self.pb_OK = QPushButton(u"确定", Dialog)
        self.pb_Cancel = QPushButton(u"取消", Dialog)
        # 添加到布局
        layout.addLayout(self.fileTapUI(Dialog))
        layout.addLayout(self.fileTapUI_2(Dialog))
        layout.addWidget(self.pb_OK)
        layout.addWidget(self.pb_Cancel)   
        
    def fileTapUI(self, Dialog):
        layout = QHBoxLayout(Dialog)
        # layout.addWidget(self.sub_fileTapUI())
        layout.addWidget(self.label_import)
        layout.addWidget(self.lineEdit_import)
        layout.addWidget(self.pb_import)
        return layout

    def fileTapUI_2(self, Dialog):
        layout = QHBoxLayout(Dialog)
        layout.addWidget(self.label_export)
        layout.addWidget(self.lineEdit_export)
        layout.addWidget(self.pb_export)
        return layout

    # def sub_fileTapUI(self):
    #     sub_fileTap = QWidget()
    #     layout = QFormLayout()
    #     layout.addRow(self.label_import, self.lineEdit_import)
    #     sub_fileTap.setLayout(layout)
    #     return sub_fileTap
    
        
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_subWin_filepath()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
