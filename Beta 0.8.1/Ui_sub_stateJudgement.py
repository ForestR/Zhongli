# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:04:36 2020

二级界面——船舶状态判定。

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Ui_sub_state(object):
    
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("船舶工作状态辅助判定")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        # Dialog.resize(500, 400)
        Dialog.setFixedSize(500, 400)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建按钮
        self.pb_setFilePath = QPushButton("目录设置",Dialog)
        self.pb_setDate = QPushButton("日期设置",Dialog)
        self.pb_getCSV = QPushButton("生成数表",Dialog)
        self.pb_Cancel = QPushButton(u"返回主菜单",Dialog)
        # 创建单选框
        self.rb_section = QRadioButton("区间工作状态",Dialog)
        self.rb_moment = QRadioButton("瞬时工作状态",Dialog)
        self.rb_section.setChecked(True)
        # 添加到布局
        layout.addWidget(self.pb_setFilePath)
        layout.addWidget(self.pb_setDate)
        layout.addLayout(self.rbAreaUI(Dialog))
        layout.addWidget(self.pb_getCSV)
        layout.addWidget(self.pb_Cancel)
        
    def rbAreaUI(self, Dialog):
        layout = QHBoxLayout(Dialog)
        layout.addWidget(self.rb_section)
        layout.addWidget(self.rb_moment)
        return layout


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_sub_state()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
