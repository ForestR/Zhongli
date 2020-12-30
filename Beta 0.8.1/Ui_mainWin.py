# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:52:26 2020

主界面UI，设有菜单栏，状态栏及三个按钮

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QMenuBar, QMenu, QAction, QStatusBar)
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import Qt

class Ui_main(object):
        
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("“俊洋一”船机日志辅助分析程序 0.8.1")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        Dialog.centralwidget = QWidget()
        Dialog.setCentralWidget(Dialog.centralwidget)
        # self.resize(500, 400)
        Dialog.setFixedSize(500, 400)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog.centralwidget)
        Dialog.setLayout(layout)
        # 创建菜单栏
        self.menubar = QMenuBar(Dialog)       
        self.menu_help = QMenu("帮助")
        self.menubar.addMenu(self.menu_help)
        Dialog.setMenuBar(self.menubar)
        # 创建菜单项
        self.action_helpDoc = QAction(QIcon("doc.svg"),"帮助文档")
        self.action_author = QAction(QIcon("github.svg"),"关于作者")
        self.action_helpDoc.setStatusTip("打开帮助文档")
        self.action_author.setStatusTip("显示作者信息")
        # 添加到菜单
        self.menu_help.addAction(self.action_helpDoc)
        self.menu_help.addAction(self.action_author)
        # 创建状态栏
        self.statusbar = QStatusBar(Dialog)
        Dialog.setStatusBar(self.statusbar)
        # 创建按钮
        self.pb_sub_visiual = QPushButton("可视化分析",Dialog)
        self.pb_sub_state = QPushButton("状态判定",Dialog)
        self.pb_Cancel = QPushButton("退出程序",Dialog)
        # 添加到布局
        layout.addWidget(self.pb_sub_visiual)
        layout.addWidget(self.pb_sub_state)
        layout.addWidget(self.pb_Cancel)
        
     
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = QMainWindow()
    UI = Ui_main()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
