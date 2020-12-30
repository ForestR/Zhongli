# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:10:10 2020

@author: Da YIN
"""

import os
from PyQt5 import QtWidgets
from Ui_sub_customOutput import Ui_subWin_custom


class sub_custom(QtWidgets.QWidget, Ui_subWin_custom):  
    def __init__(self, parent=None):
        super(sub_custom, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.pb_hyperlink.clicked.connect(self.on_pb_hyperlink_Clicked)
        self.pb_OK.clicked.connect(self.on_pb_OK_Clicked)
        self.pb_Cancel.clicked.connect(self.close)


    def on_pb_hyperlink_Clicked(self):
        os.popen("LOG_items.pdf")

    def on_pb_OK_Clicked(self):
        self.close()
        
  


if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    win = sub_custom()
    win.show()
    sys.exit(app.exec_())
