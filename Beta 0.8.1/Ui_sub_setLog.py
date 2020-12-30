# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 10:40:35 2020

本界面用于选取日志及对应日志内的具体参数。

@author: Da YIN
"""

from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QTabWidget, QCheckBox,
                             QWidget, QPushButton, QComboBox, QStackedLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Ui_subWin_setLog(object):
        
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("参数选取")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        # Dialog.resize(500, 400)
        Dialog.setFixedSize(500, 600)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # 创建顶层布局
        self.layout = QVBoxLayout(Dialog)
        Dialog.setLayout(self.layout)
        # 创建按钮
        self.pb_custom = QPushButton(u"输出参数自定义", Dialog)
        self.pb_OK = QPushButton(u"确定", Dialog)
        self.pb_Cancel = QPushButton(u"取消", Dialog) 
        # 创建复选框
        self.getDict(Dialog)
        self.checkBox(Dialog)
        # 选择布局模块
        # self.TabUI(Dialog)
        self.ComboUI(Dialog)
        # 添加到布局
        self.layout.addWidget(self.pb_custom)
        self.layout.addWidget(self.pb_OK)
        self.layout.addWidget(self.pb_Cancel)  


    def ComboUI(self, Dialog):
        # 创建下拉菜单
        self.pageCombo = QComboBox(Dialog)
        items = []
        for i in range(len(self.dict_cat)):
            items.append(self.dict_cat[i][0][0])
        self.pageCombo.addItems(items)
        self.pageCombo.activated.connect(self.switchPage)
        
        # 创建堆栈
        self.stackedLayout = QStackedLayout()      

        for i in range(len(self.dict_cat)):
            widget = QWidget(Dialog)
            layout = QVBoxLayout(Dialog)
            for j in range(len(self.dict_cat[i])):
                layout.addWidget(self.checkBox[i][j])
                
            widget.setLayout(layout)
            self.stackedLayout.addWidget(widget)
            
        # 添加到布局
        self.layout.addWidget(self.pageCombo)
        self.layout.addLayout(self.stackedLayout)
        
        
    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())        
        
        
    def TabUI(self, Dialog):
        # 创建选项卡
        self.tabs = QTabWidget()
        
        for i in range(len(self.dict_cat)):
            widget = QWidget(Dialog)
            layout = QVBoxLayout(Dialog)
            for j in range(len(self.dict_cat[i])):
                layout.addWidget(self.checkBox[i][j])
                
            widget.setLayout(layout)
            self.tabs.addTab(widget,self.dict_cat[i][j][0])    

        # 添加到布局
        self.layout.addWidget(self.tabs)

        
    def checkBox(self, Dialog):
        self.checkBox = {}
        for i in range(len(self.dict_cat)):
            self.checkBox[i] = {}
            for j in range(len(self.dict_cat[i])):
                text = str(self.dict_cat[i][j][1]) + " " + self.dict_cat[i][j][2]
                self.checkBox[i][j] = QCheckBox(text)
                
    
    def getDict(self, Dialog):
        self.dict_cat = {}
        self.dict_cat[0] = {0:("ELECTRICAL",14,"泥泵分配功率（吹岸）")}
        self.dict_cat[1] = {0:("JETPUMPS",8,"左冲水驱动功率"),
                            1:("JETPUMPS",42,"右冲水驱动功率")}
        self.dict_cat[2] = {0:("DRGPUMPS",26,"左水下泵驱动功率"),
                            1:("DRGPUMPS",60,"右水下泵驱动功率")}
        self.dict_cat[3] = {0:("PRC",15,"左耙挖泥浓度"),
                            1:("PRC",24,"左耙挖泥流速"),
                            2:("PRC",16,"左耙控泥湿砂（立方）"),
                            3:("PRC",20,"左耙挖泥干砂（立方）"),
                            4:("PRC",25,"右耙挖泥浓度"),
                            5:("PRC",34,"右耙挖泥流速"),
                            6:("PRC",26,"右耙控泥湿砂（立方）"),
                            7:("PRC",30,"右耙挖泥干砂（立方）"),                 
                            8:("PRC",5,"排岸浓度"),
                            9:("PRC",6,"排岸湿砂（立方）"),
                            10:("PRC",7,"排岸湿砂（立方/小时）"),
                            11:("PRC",10,"排岸干砂（立方）"),
                            12:("PRC",11,"排岸干砂（立方/小时）"),
                            13:("PRC",14,"排岸流速")}
        self.dict_cat[4] = {0:("STPM",6,"左耙吸入海图深度"),
                            1:("STPM",38,"右耙吸入海图深度")}
        self.dict_cat[5] = {0:("APC",19,"左耙中控制器实际值"),
                            1:("APC",32,"右耙中控制器实际值"),
                            2:("APC",25,"左耙流速"),
                            3:("APC",38,"右耙流速")}
        self.dict_cat[6] = {0:("DOORS",5,"大泥门组1控制")}
        self.dict_cat[7] = {0:("DLM",6,"自动吃水控制器容量"),
                            1:("DLM",8,"排水量"),
                            2:("DLM",40,"吃水平均"),
                            3:("DLM",75,"泥舱左舯液位平均值"),
                            4:("DLM",82,"泥舱右舯液位平均值"),
                            5:("DLM",91,"泥舱装载量"),
                            6:("DLM",92,"泥舱原状土（湿砂）装载量"),
                            7:("DLM",93,"泥舱固体（干砂）装载量")}
        self.dict_cat[8] = {0:("PROPULSION",13,"左推进实际螺距"),
                            1:("PROPULSION",14,"右推进实际螺距")}
        self.dict_cat[9] = {0:("POWER",30,"左轴发电机功率"),
                            1:("POWER",33,"左轴发电机无功功率"),
                            2:("POWER",44,"右轴发电机功率"),
                            3:("POWER",47,"右轴发电机无功功率")}
        
        
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_subWin_setLog()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
