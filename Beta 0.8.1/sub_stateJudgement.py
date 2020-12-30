# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:10:53 2020

@author: Da YIN
"""

from PyQt5 import QtCore, QtWidgets
from Ui_sub_stateJudgement import Ui_sub_state
from sub_setDate import sub_setdate
from sub_setFilePath import sub_filepath
from Ui_ValueError import ui_valueError
import pandas as pd 
from GUnloadSection import getUnloadSection
from GUploadSection import getUploadSection
from GPrintf import getDataFrame


class sub_state(QtWidgets.QWidget, Ui_sub_state):
    
    def __init__(self, parent=None):
        super(sub_state, self).__init__(parent)
        self.setupUi(self)
        
        # 以下为业务逻辑
        self.isEnabled = False
        self.pb_setFilePath.clicked.connect(self.on_pb_setFilePath_Clicked)
        self.pb_setDate.clicked.connect(self.on_pb_setDate_Clicked)
        self.pb_getCSV.clicked.connect(self.on_pb_getCSV_Clicked)
        self.pb_Cancel.clicked.connect(self.on_pb_Cancel_Clicked)
        
        self.ChildDialog1 = sub_filepath()
        self.ChildDialog1.setWindowModality(QtCore.Qt.ApplicationModal) # 子窗口阻塞父窗口        
        self.ChildDialog2 = sub_setdate()
        self.ChildDialog2.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.ErrorDialog = valueError()
        self.ErrorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ErrorDialog.setWindowTitle('警告')


    def on_pb_setFilePath_Clicked(self):
        self.ChildDialog1.show()

    def on_pb_setDate_Clicked(self):
        self.ChildDialog2.show()
        
    def on_pb_getCSV_Clicked(self):
        if (self.ChildDialog1.isEnabled and self.ChildDialog2.isEnabled):
            self.isEnabled = True
            dir_import = self.ChildDialog1.dir_import 
            # dir_export = self.ChildDialog1.dir_export
            year = self.ChildDialog2.year
            month = self.ChildDialog2.month
            day1 = self.ChildDialog2.day1
            day2 = self.ChildDialog2.day2
            
            self.child3 = unloadSection(dir_import, year, month, day1, day2)
            self.child4 = uploadSection(dir_import, year, month, day1, day2)
            self.df_unload = self.child3.getUnloadSection.df
            self.df_upload = self.child4.getUploadSection.df
            
            self.getSection()
            self.getMoment()
        
        else:
            self.isEnabled = False
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("请检查文件【设置】！！")
        
        
    def on_pb_Cancel_Clicked(self):
        self.close()        


    def getSection(self):
        dir_export = self.ChildDialog1.dir_export # 有待优化
        year = self.ChildDialog2.year
        month = self.ChildDialog2.month
        day1 = self.ChildDialog2.day1
        day2 = self.ChildDialog2.day2
            
        df = pd.DataFrame()
        df = df.append(self.df_upload,ignore_index=True)
        df = df.append(self.df_unload,ignore_index=True)
        
        if df.shape[0] > 1 :
            df.sort_values(by=["StartStamp"],ascending=[True],inplace=True) # 按值升序
            df.reset_index(drop=True,inplace=True)  # 修正索引
            # print(df.head(5))
            df_new = self.supplement(df)
            self.df = df_new
            # print(df_new.head(5))
        else:
            self.ErrorDialog.show()
            self.ErrorDialog.label_Tips.setText("存在停工，请核对施工日志！！")
            # start = self.create_timestamp(day1)
            # stop = self.create_timestamp(day2) + 86400
            # # 这里将df.shape[0] == 1的情形舍弃了
            # self.df = pd.Series({'StartStamp':strat,'StopStamp':stop,
            #                      'Inerval':stop-strat,'Action':40}) # 停工

        df_ex = self.decode(df_new)
        # print(df_ex.head(5))
        
        str1 = "%04d_%02d_%02d~%02d_Section"%(year,month,day1,day2)
        filename = r''+dir_export+"/"+str1+".csv"
        col_name = df_ex.columns.tolist()
        df_ex.to_csv(filename,encoding="utf_8_sig",index=False,
                    sep=',',columns=col_name)  


    def getMoment(self):
        dir_import = self.ChildDialog1.dir_import # 有待优化
        dir_export = self.ChildDialog1.dir_export
        year = self.ChildDialog2.year
        month = self.ChildDialog2.month
        day1 = self.ChildDialog2.day1
        day2 = self.ChildDialog2.day2
        
        dict_act = {10:'直抛',11:'虹喷',12:'艏吹',
                    20:'左耙',21:'右耙',22:'双耙',
                    30:'轻载',31:'重载',39:'调度',
                    40:'停工',41:'待定'}
        
        for day in range(day1, 1+day2):
            df = getDataFrame(year,month,day,dir_import)
            df['作业状态'] = 0 # 添加列
            cond1 = self.df["StartStamp"] <= df['Stamp'].max() + 2*3600 # 放宽2小时
            cond2 = self.df["StopStamp"] >= df['Stamp'].min() - 2*3600
            df_section = self.df[cond1 & cond2]

            for i in range(df_section.shape[0]):
                action = dict_act[self.df.Action.iloc[i]]  
                start = df_section.StartStamp.iloc[i]
                stop = df_section.StopStamp.iloc[i]
                cond3 = df['Stamp'] >= start
                cond4 = df['Stamp'] < stop
                df.loc[cond3 & cond4, '作业状态'] = action # 列赋值
                
            str1 = "%04d_%02d_%02d_Moment"%(year,month,day)
            filename = r''+dir_export+"/"+str1+".csv"
            col_name = df.columns.tolist()
            df.to_csv(filename,encoding="utf_8_sig",index=False,
                      sep=',',columns=col_name)


    # def create_timestamp(self, day):
    #     import datetime
        
    #     year = self.ChildDialog2.year
    #     month = self.ChildDialog2.month
        
    #     start_time = "%04d-%02d-%02d"%(year, month, day)
    #     date_time = pd.Timestamp(start_time) - datetime.datetime(year,1,1) # 时间戳锚定日
    #     time_stamp = date_time.days*86400 + date_time.seconds # 将日期转换为时间戳 
    #     return time_stamp               

# =============================================================================
# 将输入stamp码转换为日期
# =============================================================================
    def stamp2date(self,time_stamp,year):
        str1 = pd.to_datetime(time_stamp,unit='s',
                              origin=pd.Timestamp('%s-1-1'%year))
        
        return str1
    
    
# =============================================================================
# 对区间缺失的部分进行补全
# =============================================================================
    def supplement(self, df):   
        df_new = pd.DataFrame()
        
        # day1 = self.ChildDialog2.day1
        # day2 = self.ChildDialog2.day2
        # start = self.create_timestamp(day1)
        # stop = self.create_timestamp(day2) + 86400  
        # if df.iloc[0,0] > start:
        #     ans = df.iloc[0,0]  - start
        #     log_act = pd.Series({"StartStamp":start,
        #                           "StopStamp":df.iloc[0,0],
        #                           "Interval":ans,
        #                           "Action": 41})  # 待定
        #     df_new = df_new.append(log_act,ignore_index=True)
        
        df_new = df_new.append(df.iloc[0],ignore_index=True)
        
        for i in range(df.shape[0]-1):
            ans = df.iloc[i+1,0]  - df.iloc[i,1]
            if ans > 300:
                log_act = pd.Series({"StartStamp":df.iloc[i,1],
                                     "StopStamp":df.iloc[i+1,0],
                                     "Interval":ans,
                                     "Action": 0})       
                if df.iloc[i+1,3] >= 20: # 装载
                    if df.iloc[i,3] < 20: # 卸载
                        log_act["Action"] = 30 # 轻载  # 可以结合GPS进行较准
                    else: # 装载
                        log_act["Action"] = 39 # 调度
                else: # 卸载
                    if df.iloc[i,3] >= 20: # 装载
                        log_act["Action"] = 31 # 重载  # 可以结合GPS进行较准
                    else: # 卸载
                        log_act["Action"] = 39 # 调度
                
                if log_act['StopStamp']-log_act['StartStamp'] > 3600*24: # 超24小时算停工
                    log_act["Action"] = 40 # 停工
                    
                df_new = df_new.append(log_act,ignore_index=True)
            df_new = df_new.append(df.iloc[i+1],ignore_index=True)
            
        # if df.iloc[df.shape[0]-1,1] < stop:
        #     ans = stop - df.iloc[df.shape[0]-1]
        #     log_act = pd.Series({"StartStamp":df.iloc[df.shape[0]-1],
        #                           "StopStamp":stop,
        #                           "Interval":ans,
        #                           "Action": 41})  # 待定
        #     df_new = df_new.append(log_act,ignore_index=True)
        
        df_sort = pd.DataFrame()
        df_sort['StartStamp'] = df_new['StartStamp']
        df_sort['StopStamp'] = df_new['StopStamp']
        df_sort['Interval'] = df_new['Interval']
        df_sort['Action'] = df_new['Action']
            
        return df_sort


# =============================================================================
# 数据解码,将dataframe数值转换为一般人能理解的语句
# =============================================================================
    def decode(self, df):
        df_ex = pd.DataFrame()
        df_ex['开始时刻'] = df['StartStamp']
        df_ex['结束时刻'] = df['StopStamp']
        df_ex['持续时间(min)'] = df['Interval']
        df_ex['工作状态'] = df['Action']
        
        dict_act = {10:'直抛',11:'虹喷',12:'艏吹',
                    20:'左耙',21:'右耙',22:'双耙',
                    30:'轻载',31:'重载',39:'调度',
                    40:'停工',41:'待定'}
        
        print(df_ex.shape[0])
        for i in range(df_ex.shape[0]):
            df_ex.iloc[i,0] = self.stamp2date(df_ex.iloc[i,0],self.ChildDialog2.year)
        for i in range(df_ex.shape[0]):
            df_ex.iloc[i,1] = self.stamp2date(df_ex.iloc[i,1],self.ChildDialog2.year)        
        for i in range(df_ex.shape[0]):
            df_ex.iloc[i,2] = df_ex.iloc[i,2] / 60
        for i in range(df_ex.shape[0]):
            df_ex.iloc[i,3] = dict_act[df_ex.iloc[i,3]]            
        return df_ex


class valueError(QtWidgets.QWidget, ui_valueError):
    def __init__(self):
        super(valueError, self).__init__()
        self.setupUi(self)
        self.PbOK.clicked.connect(self.close)

class unloadSection(getUnloadSection): # child class
    def __init__(self, dir_import, year, month, day1, day2):
        # super().__init__()
        # self.setUp()
        self.getUnloadSection = getUnloadSection(dir_import, year, month, day1, day2)

class uploadSection(getUploadSection): # child class
    def __init__(self, dir_import, year, month, day1, day2):
        self.getUploadSection = getUploadSection(dir_import, year, month, day1, day2)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = sub_state()
    win.show()
    sys.exit(app.exec_())
