# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:28:20 2020

@author: Da YIN
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QProgressBar, 
                             QTextBrowser, QPushButton)
from PyQt5.QtGui import QIcon

class Ui_sub_progress(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("数据处理进度")
        self.setWindowIcon(QIcon("ship.svg"))
        self.resize(500, 400)
        # 创建顶层布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        # 创建进度条
        self.progressBar = QProgressBar()
        # self.progressBar.setProperty("value",0)
        self.progressBar.setValue(0)
        # 创建文本浏览器
        self.textBrowser = QTextBrowser()
        # 创建按钮
        self.pb_OK = QPushButton(u"确定", self)
        self.pb_Cancel = QPushButton(u"取消", self)
        # 添加到布局
        layout.addWidget(self.progressBar)
        layout.addWidget(self.textBrowser)
        layout.addWidget(self.pb_OK)
        layout.addWidget(self.pb_Cancel)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_sub_progress()
    window.show()
    sys.exit(app.exec_())
