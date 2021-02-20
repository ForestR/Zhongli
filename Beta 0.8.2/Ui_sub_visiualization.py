# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 20:29:41 2020

二级界面———数据可视化。

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QRadioButton) # QGraphicsView,
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
import matplotlib.pyplot as plt 

class Ui_sub_visiual(object):
    
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("可视化分析")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        Dialog.resize(1000, 500)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建可视化组件
        # self.graphicsViex = QGraphicsView(Dialog)
        self.figure = plt.figure() 
        self.canvas = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas, Dialog) 
        # 创建按钮
        self.pb_setFilePath = QPushButton("目录设置", Dialog)
        self.pb_setDate = QPushButton("日期设置", Dialog)
        self.pb_setLog = QPushButton("参数设置", Dialog)
        self.pb_plot = QPushButton("显示图像", Dialog)
        self.pb_last = QPushButton("上个图像", Dialog)
        self.pb_next = QPushButton("下个图像", Dialog)
        # self.pb_export = QPushButton("图像导出", Dialog)
        self.pb_Cancel = QPushButton(u"返回主菜单", Dialog)
        # 创建单选按钮
        self.rb_singleDay = QRadioButton("仅显示当日数据", Dialog)
        self.rb_doubleDay = QRadioButton("显示连续两日数据(若有)", Dialog)
        # self.rb_singleDay.setChecked(True)
        self.rb_doubleDay.setChecked(True)
        # 添加到布局
        layout.addLayout(self.topAreaUI(Dialog))
        layout.addLayout(self.plotAreaUI(Dialog))
        layout.addWidget(self.pb_Cancel)        

    def topAreaUI(self, Dialog):
        layout = QHBoxLayout(Dialog)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.pb_setFilePath)
        layout.addWidget(self.pb_setDate)
        layout.addWidget(self.pb_setLog)  
        return layout
        
    def plotAreaUI(self, Dialog):
        layout = QVBoxLayout(Dialog)
        # layout.addWidget(self.graphicsViex)
        layout.addWidget(self.canvas)
        layout.addLayout(self.rbAreaUI(Dialog))
        layout.addWidget(self.pb_plot)
        return layout
    
    def rbAreaUI(self, Dialog):
        layout = QHBoxLayout(Dialog)
        layout.addWidget(self.rb_singleDay)
        layout.addWidget(self.rb_doubleDay)
        layout.addWidget(self.pb_last)
        layout.addWidget(self.pb_next)
        return layout


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_sub_visiual()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())