# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:20:26 2020

本界面为用户提供一个文本框用于输入自定义代码，
每当文本框内容发生变更后将光标置于文本末端，
# 提供一个链接按钮用于引导到HELP文档，
提供确定，取消按钮。

@author: Da YIN
"""


from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget,
                             QPushButton, QTextEdit)
from PyQt5.QtGui import QIcon


show2str = '''@general
def getlogname(num):
    dict_cat = {}
    dict_cat[0] = {0:("ELECTRICAL",14,"泥泵分配功率（吹岸）")}
    dict_cat[1] = {0:("JETPUMPS",8,"左冲水驱动功率"),
                   1:("JETPUMPS",42,"右冲水驱动功率")}
    dict_cat[2] = {0:("DRGPUMPS",26,"左水下泵驱动功率"),
                   1:("DRGPUMPS",60,"右水下泵驱动功率")}
    dict_cat[3] = {0:("PRC",15,"左耙挖泥浓度"),
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
    dict_cat[4] = {0:("STPM",6,"左耙吸入海图深度"),
                   1:("STPM",38,"右耙吸入海图深度")}
    dict_cat[5] = {0:("APC",19,"左耙中控制器实际值"),
                   1:("APC",32,"右耙中控制器实际值"),
                   2:("APC",25,"左耙流速"),
                   3:("APC",38,"右耙流速")}
    dict_cat[6] = {0:("DOORS",5,"大泥门组1控制")}
    dict_cat[7] = {0:("DLM",6,"自动吃水控制器容量"),
                   1:("DLM",8,"排水量"),
                   2:("DLM",40,"吃水平均"),
                   3:("DLM",75,"泥舱左舯液位平均值"),
                   4:("DLM",82,"泥舱右舯液位平均值"),
                   5:("DLM",91,"泥舱装载量"),
                   6:("DLM",92,"泥舱原状土（湿砂）装载量"),
                   7:("DLM",93,"泥舱固体（干砂）装载量")}
    dict_cat[8] = {0:("PROPULSION",13,"左推进实际螺距"),
                   1:("PROPULSION",14,"右推进实际螺距")}
    dict_cat[9] = {0:("POWER",30,"左轴发电机功率"),
                   1:("POWER",33,"左轴发电机无功功率"),
                   2:("POWER",44,"右轴发电机功率"),
                   3:("POWER",47,"右轴发电机无功功率")}    
    dict_log = dict_cat[num]
    
    return dict_log'''

class Ui_subWin_custom(object):

    def setupUi(self, Dialog):
        Dialog.setWindowTitle("自定义输出")
        Dialog.setWindowIcon(QIcon("ship.svg"))
        Dialog.resize(500, 400)
        # 创建顶层布局
        layout = QVBoxLayout(Dialog)
        Dialog.setLayout(layout)
        # 创建滚动文本
        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setText(show2str)
        layout.addWidget(self.textEdit)
        # 创建按钮
        self.pb_hyperlink = QPushButton(u"打开服务器日志手册", Dialog)
        self.pb_OK = QPushButton(u"确定", Dialog)
        self.pb_Cancel = QPushButton(u"取消", Dialog)
        # 添加到布局
        layout.addWidget(self.pb_hyperlink)
        layout.addWidget(self.pb_OK)
        layout.addWidget(self.pb_Cancel)


if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    widget = QWidget()
    UI = Ui_subWin_custom()
    UI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
