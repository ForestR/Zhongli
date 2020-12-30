# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:36:23 2020

@author: Da YIN
"""

from PyQt5 import QtCore, QtWidgets
from matplotlib import font_manager
from Ui_sub_visiualization import Ui_sub_visiual
from sub_setDate import sub_setdate
from sub_setFilePath import sub_filepath
from sub_setLog import sub_setlog
from Ui_ValueError import ui_valueError
import pandas as pd
from pandas.io.common import EmptyDataError, ParserError

class sub_visiual(QtWidgets.QWidget, Ui_sub_visiual):
    
    def __init__(self, parent=None):
        super(sub_visiual, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.pb_setFilePath.clicked.connect(self.on_pb_setFilePath_Clicked)
        self.pb_setDate.clicked.connect(self.on_pb_setDate_Clicked)
        self.pb_setLog.clicked.connect(self.on_pb_setLog_Clicked)
        self.pb_plot.clicked.connect(self.on_pb_plot_Clicked)
        self.pb_last.clicked.connect(self.on_pb_last_Clicked)
        self.pb_next.clicked.connect(self.on_pb_next_Clicled)
        # self.pb_export.clicked.connect(self.on_pb_export_Clicked)
        self.pb_Cancel.clicked.connect(self.on_pb_Cancel_Clicked)
        
        self.ChildDialog1 = sub_filepath()
        self.ChildDialog1.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口        
        self.ChildDialog2 = sub_setdate()
        self.ChildDialog2.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口
        self.ChildDialog3 = sub_setlog()
        self.ChildDialog3.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ErrorDialog.setWindowTitle('警告')
        
        
    def on_pb_setFilePath_Clicked(self):
        self.ChildDialog1.show()

    def on_pb_setDate_Clicked(self):
        self.ChildDialog2.show()

    def on_pb_setLog_Clicked(self):
        self.ChildDialog3.show()

    def on_pb_plot_Clicked(self):
        if (self.ChildDialog1.isEnabled and self.ChildDialog2.isEnabled and 
            self.ChildDialog3.isEnabled):
            self.isEnabled = True
            self.day = self.ChildDialog2.day1
            self.day_isChanged = 1
            self.k = 0
            self.j = self.ChildDialog3.list_j[self.k]   
            self.series = self.getData()
            self.pltdata()
        else:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请检查文件【设置】！！")


    def on_pb_last_Clicked(self):
        if self.isEnabled :
            if (self.k > 0):
                self.day_isChanged = 0
                self.k -= 1 # 滚动到上个参数
                self.j = self.ChildDialog3.list_j[self.k]
                self.series = self.getData()
                self.pltdata()
            elif (self.day > self.ChildDialog2.day1):
                self.day_isChanged = 1
                self.day -= 1 # 此处要求同年同月
                self.k = len(self.ChildDialog3.list_j) - 1
                self.j = self.ChildDialog3.list_j[self.k]
                self.series = self.getData()
                self.pltdata()                
            else:
                self.ErrorDialog.show()
                self.ErrorDialog.label_Tips.setText("到此为止了！！")                        
        else:
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请点击【显示图像】！！")
            
    
    def on_pb_next_Clicled(self):
        if self.isEnabled :
            length = len(self.ChildDialog3.list_j)
            if (self.k < length -1):
                self.day_isChanged = 0
                self.k += 1 # 滚动到下个参数
                self.j = self.ChildDialog3.list_j[self.k]
                self.series = self.getData()
                self.pltdata()
            elif (self.day < self.ChildDialog2.day2):
                self.day_isChanged = 1
                self.day += 1 # 此处要求同年同月
                self.k = 0
                self.j = self.ChildDialog3.list_j[self.k]
                self.series = self.getData()
                self.pltdata()
            else:
                self.ErrorDialog.show()
                self.ErrorDialog.label_Tips.setText("到此为止了！！")                
        else:
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请点击【显示图像】！！")
            
    
    # def on_pb_export_Clicked(self):
    #     pass
    
    def on_pb_Cancel_Clicked(self):
        self.close()

    def getData(self):
        index = self.ChildDialog3.i
        dict_log = self.ChildDialog3.dict_cat[index]
        
        if self.day_isChanged: # 减少重复读取
            (self.df, self.status) = self.loadLog()
        
        if self.status[1]: # 查询日当日数据文件存在
            if self.status[0]: # 查询日-1日数据文件存在
                list_series = []
                for k in range(2):
                    tmp = self.df[k]
                    series = tmp[dict_log[self.j][1]]
                    list_series.extend(series)     
                series = pd.Series(list_series)
            else: # 查询日-1日数据不存在 
                tmp = self.df[1]
                series = tmp[dict_log[self.j][1]]
        else:
            series = []
        return series


    def loadLog(self):
        '''传递变量'''
        year = self.ChildDialog2.year
        month = self.ChildDialog2.month
        day = self.day
        
        '''载入日志'''
        list_df = []; list_status = []
        for i in range(2): # 载入连续2日的日志
            today = "%s-%s-%s"%(year,month,day)
            today = pd.Timestamp(today) + (i-1) * pd.Timedelta('1 days')
            (df,status) = self.readCSV(today.year, today.month, today.day)
            list_df.append(df)
            list_status.append(status)
        return list_df, list_status


    def readCSV(self, year, month, day):
        '''传递变量'''
        index = self.ChildDialog3.i
        log_name = self.ChildDialog3.dict_cat[index][0][0]
        directory = self.ChildDialog1.dir_import
        
        '''打开文件'''
        date = "%04d_%02d_%02d"%(year,month,day) 
        filename = directory + "/"+date+"/"+date+"_%s_LOG_T.csv"%log_name
        try:
            df = pd.read_csv(filename, sep='\\s+', skiprows=[0], header=None) # 原始数据
            status = 1
        except EmptyDataError: # csv文件数据为空
            self.ErrorDialog.show()
            self.ErrorDialog.setFixedSize(350,100)
            self.ErrorDialog.label_Tips.setText("文件为空: "+date+"_%s_LOG_T.csv"%log_name)
            # print("EmptyDataError: "+filename)
            df = pd.DataFrame()
            status = 0
        except ParserError:
            # Expected 133 fields in line 6, saw 134
            '''注意：该函数与python自带的fopen.readline()和Excel自带的分割函数的运算逻辑都不一样'''
            df = pd.read_csv(filename, sep='\\s+', skiprows=[0], header=None, delimiter="\t")
            status = 1
        except FileNotFoundError:
            # csv does not exist
            self.ErrorDialog.show()
            self.ErrorDialog.setFixedSize(350,100)
            self.ErrorDialog.label_Tips.setText("文件缺失: "+date+"_%s_LOG_T.csv"%log_name)            
            # print("FileNotFoundError: "+filename)
            df = pd.DataFrame()
            status = 0
        return df, status


    def pltdata(self):
        '''传递变量'''
        year = self.ChildDialog2.year
        month = self.ChildDialog2.month
        day = self.day
        index = self.ChildDialog3.i
        dict_cat = self.ChildDialog3.dict_cat
        series = self.series
        j = self.j

        '''初始化画板'''
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        '''设置网格'''
        num = len(series)
        if num >= 20000*2:
            ax.set_figsize=(32,8)
            ax.set_xlim([0,28800*2])
            ax.axvline(x=num/2,ls="-",c="green") #添加垂直直线
            # ax.axvline(x=num*2/3,ls="-",c="green") #添加垂直直线
        else:
            ax.set_figsize=(16,8)
            ax.set_xlim([0,28800])
        # ax.set_ylim([0,2000])
        ax.grid(ls=":",c='b',) #打开坐标网格
        # ax.axhline(y=0,ls=":",c="yellow") #添加水平直线
        
        '''设置文字'''
        my_font = font_manager.FontProperties(fname="C:\Windows\Fonts\simhei.ttf")
        ax.set_xlabel("step")
        ax.set_ylabel("value")
        str1 = dict_cat[index][j][2]
        if num >= 20000*2:
            date1 = "%04d_%02d_%02d"%(year,month,day-1)
            date2 = "%04d_%02d_%02d"%(year,month,day)
            str2 = date1 + " - " + date2 + "  " + str1
            ax.set_title(str2,fontproperties=my_font)
        else:
            date = "%04d_%02d_%02d"%(year,month,day)
            str2 = date + "  " + str1
            ax.set_title(str2,fontproperties=my_font)
        # ax.legend(prop=my_font)  
        
        '''生成图像'''
        ax.plot(series,'r-',label=str1,color="red",linewidth=2)
        self.canvas.draw()


class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = sub_visiual()
    win.show()
    sys.exit(app.exec_())
