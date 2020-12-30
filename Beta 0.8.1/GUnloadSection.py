# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:14:18 2020

创建俊洋一日志处理程序的父类构造函数——卸载状态识别

@author: Da YIN
"""

import pandas as pd
import numpy as np
import General as gn
import datetime
from pandas.io.common import EmptyDataError, ParserError


# class getUploadSection(object): # Python 2
class getUnloadSection: # Python 3 

    def __init__(self, dir_import, year, month, day1, day2):
        self.dir_import = dir_import
        self.year = year
        self.month = month
        self.day1 = day1
        self.day2 = day2
        self.df = self.setUp()


    def setUp(self): 
        self.dic_poi = {10:("Dumping",6,0),
                        11:("Rainbowing",3,13),
                        12:("Shorepumping",3,13)}    

        df = pd.DataFrame()
        
        '''判定直抛工作区间'''
        new_log = []
        self.action = 10 
        self.dict_log = {0:("DOORS",5,"大泥门组1控制")}
        for self.day in range(self.day1, 1 + self.day2):
            log_act = self.getlogact()
            log_act = self.dump(log_act)
            for x in log_act: new_log.append(x)
        log_act = self.revise(new_log)
        if log_act != []:
            order = ["StartStamp","StopStamp","Interval","Action"]
            df_dump = pd.DataFrame(log_act,columns = order)
            df = df.append(df_dump,ignore_index=True)
            # print(df.head(3)); print('');
        
        '''判定艏吹/虹喷工作区间'''
        new_log = []
        self.action = 11
        self.dict_log = {13:("PRC",14,"排岸流速")} 
        for self.day in range(self.day1, 1 + self.day2):
            log_act = self.getlogact()
            # log_act = self.shore(log_act)
            for x in log_act: new_log.append(x)
        log_act = self.revise(new_log)
        if log_act != []:
            df_shore = self.getshorevel(log_act)
            df_shore.loc[df_shore["ShoreVel"]<5, "Action"] = 12
            del df_shore['ShoreVel']
            df = df.append(df_shore,ignore_index=True)
            # print(df.head(3)); print('');
        
            df.sort_values(by=["StartStamp"],ascending=[True],inplace=True)
        # print(df.head(3)); print('');
        else:
            df = pd.DataFrame()
        return df
        
        # df_ex = self.decode(df)
        # print(df_ex.head(3))

        # # 格式化输出
        # str1 = "%04d_%02d_%02d~%02d_Status"%(self.year,self.month,self.day1,self.day2)
        # col_name = df_ex.columns.tolist()
        # df_ex.to_csv(str1+".csv",encoding="utf_8_sig",index=False,
        #             sep=',',columns=col_name)       
        
# =============================================================================
# Dump 直抛
# =============================================================================        
    def dump(self, log_act): 
        new_log = []
        for i in range(len(log_act)):
            num = log_act[i][2] // 2  # 对抛泥动作的判定区间适当加宽
            start_stamp = log_act[i][0] - num
            stop_stamp = log_act[i][1] + num
            tmp = [start_stamp, stop_stamp, stop_stamp-start_stamp, self.action]
            new_log.append(tmp)
        log_act = new_log
        return log_act          


# =============================================================================
# Shore 虹喷 & 艏吹
# =============================================================================
    def getshorevel(self, log_act):
        list_val = self.test(log_act) # 有待重构优化
        
        order = ["StartStamp","StopStamp","Interval","Action"]
        df = pd.DataFrame(log_act,columns = order)
        
        list_val = pd.DataFrame(list_val)
        val = list_val[5]
        df["ShoreVel"] = val 
        return df
        

    def getlogact(self):
        (action_n, num, self.j) = self.dic_poi[self.action]
        log_act = self.getData()
        return log_act


    def getData(self):
        # if self.day_isChanged: # 减少重复读取
        (df, status) = self.loadLog()
        
        if status[1]: # 查询日当日数据文件存在
            if status[0]: # 查询日-1日数据文件存在
                list_series = []
                for k in range(2):
                    tmp = df[k]
                    series = tmp[self.dict_log[self.j][1]]
                    list_series.extend(series)     
                series = pd.Series(list_series)
            else: # 查询日-1日数据不存在 
                tmp = df[1]
                series = tmp[self.dict_log[self.j][1]]
        else:
            series = pd.Series([1,1,1])
            
        if self.action == 10:
            log_name = "DOORS"
        else:
            log_name = "PRC"
        time_list = gn.get_section(series, log_name)
        time_list = self.cut_timelist(time_list, status)
        log_act = self.creat_timestamp(time_list)  
        return log_act


    def loadLog(self):
        '''传递变量'''
        year = self.year; month = self.month; day = self.day;

        '''载入日志'''
        list_df = []; list_status = []
        for i in range(2): # 载入连续2日的日志
            today = "%s-%s-%s"%(year,month,day)
            today = pd.Timestamp(today) + (i-1) * pd.Timedelta('1 days')
            (df,status) = self.readCSV(today.year, today.month, today.day)
            list_df.append(df)
            list_status.append(status)
        return list_df, list_status

# =============================================================================
# 截取当日time_list
# =============================================================================
    # 默认每日数据条数为28800（3s一条）
    def cut_timelist(self, time_list, status):
        if status[0]:
            new_list = []
            for i in range(len(time_list)):
                if time_list[i][0] > 28800: break
            if time_list[i][0] > 28800 and time_list[i][1] == 1: 
                [x, y] = time_list[i-1]
                # print(x,y,i,len(time_list))
                new_list.append([x-28800, y])
            for j in range(i,len(time_list)):
                [x , y] = time_list[j]
                new_list.append([x-28800, y])
        else:
            new_list = time_list
        return new_list

# =============================================================================
# 创建时间戳
# =============================================================================
    def creat_timestamp(self, time_list):
        year = self.year; month = self.month; day = self.day; action = self.action;
        start_time = "%04d-%02d-%02d"%(year,month,day)
        date_time = pd.Timestamp(start_time) - datetime.datetime(year,1,1) # 时间戳锚定日
        time_stamp = date_time.days*86400 + date_time.seconds # 将日期转换为时间戳
        
        log_act = []
        for i in range(len(time_list)-1):
            if time_list[i][1] == 0:
                start_stamp = time_stamp + 3*time_list[i][0]
                stop_stamp = time_stamp + 3*time_list[i+1][0]
                tmp = [start_stamp, stop_stamp, stop_stamp-start_stamp, action]
                log_act.append(tmp)

        return log_act    

# =============================================================================
# 将输入stamp码转换为日期
# =============================================================================
    def stamp2date(self,time_stamp,year):
        str1 = pd.to_datetime(time_stamp,unit='s',
                              origin=pd.Timestamp('%s-1-1'%year))
        
        return str1

# =============================================================================
# 修正log数据
# =============================================================================
    def revise(self, log_rec):
        for i in range(len(log_rec)):
            for j in range(i+1,len(log_rec)):         
                if log_rec[j][0] >= log_rec[i][0] and log_rec[j][0] <= log_rec[i][1]:
                    log_rec[i][1] = log_rec[j][1]             
                if log_rec[j][1] >= log_rec[i][0] and log_rec[j][1] <= log_rec[i][1]:
                    log_rec[i][0] = log_rec[j][0]           
            log_rec[i][2] = log_rec[i][1] - log_rec[i][0]
            
        new_log = []
        for i in range(len(log_rec)):
            if log_rec[i] not in new_log:
                new_log.append(log_rec[i])
                    
        return new_log

# =============================================================================
# 读取文件
# =============================================================================
    def readCSV(self, year, month, day):
        '''传递变量'''
        if self.action == 10:
            log_name = "DOORS"
        else:
            log_name = "PRC"
        directory = self.dir_import
        
        '''打开文件'''
        date = "%04d_%02d_%02d"%(year,month,day) 
        filename = directory + "/"+date+"/"+date+"_%s_LOG_T.csv"%log_name
        try:
            df = pd.read_csv(filename, sep='\\s+', skiprows=[0], header=None) # 原始数据
            status = 1
        except EmptyDataError: # csv文件数据为空
            # self.ErrorDialog.show()
            # self.ErrorDialog.setFixedSize(350,100)
            # self.ErrorDialog.label_Tips.setText("文件为空: "+date+"_%s_LOG_T.csv"%log_name)
            print("EmptyDataError: "+filename)
            df = pd.DataFrame()
            status = 0
        except ParserError:
            # Expected 133 fields in line 6, saw 134
            '''注意：该函数与python自带的fopen.readline()和Excel自带的分割函数的运算逻辑都不一样'''
            df = pd.read_csv(filename, sep='\\s+', skiprows=[0], header=None, delimiter="\t")
            status = 1
        except FileNotFoundError:
            # csv does not exist
            # self.ErrorDialog.show()
            # self.ErrorDialog.setFixedSize(350,100)
            # self.ErrorDialog.label_Tips.setText("文件缺失: "+date+"_%s_LOG_T.csv"%log_name)            
            print("FileNotFoundError: "+filename)
            df = pd.DataFrame()
            status = 0
        return df, status


# =============================================================================
# 获取指定序列在指定状态下的均值
# =============================================================================
    def test(self, log_act): 
        '''内测代码，有待重构'''
        year = self.year;
        list_stamp = []; list_dat = []; i = 0; 
        
        list = self.getdate(i,log_act,year)
        list_dat.append(list)
        today = list[4]   
        
        for i in range(1,len(log_act)):
            list = self.getdate(i,log_act,year)
            if today == list[4]:
                list_dat.append(list)
            else:
                list_stamp.append(list_dat)
                list_dat = []
                list_dat.append(list)
                today = list[4]
        list_stamp.append(list_dat)
        
        list_val = [];
        for i in range(len(list_stamp)):
            list_dat = list_stamp[i].copy()
            list = list_dat[0].copy()
            month = list[2]
            day2 = list[4]
            
            self.day = day2
            (df,status) = self.loadLog()
        
            for j in range(len(list_dat)):
                tmp = list_dat[j].copy()
                start_stamp = tmp[0]
                stop_stamp = tmp[1]
                day1 = tmp[3]
                
                if status[1]:
                    if day1 == day2:
                        tmp = df[1]
                        series = tmp[self.dict_log[self.j][1]]
                        val = self.getval(series,status,
                                     year,month,day1,start_stamp,stop_stamp)
                    else:
                        list_series = []
                        for k in range(2):
                            tmp = df[k]
                            series = tmp[self.dict_log[self.j][1]]
                            list_series.extend(series)     
                        series = pd.Series(list_series)              
                        val = self.getval(series,status,
                                     year,month,day1,start_stamp,stop_stamp)               
                else:
                    val = np.NaN
                tmp = list_dat[j].copy()
                tmp.append(val)
                list_val.append(tmp)
             
        return list_val

    

    def getdate(self, i, log_act, year):
        if log_act != []:
            start_stamp = log_act[i][0]
            stop_stamp = log_act[i][1]
            
            # 时间戳转换为日期
            date_time = pd.to_datetime(start_stamp,unit='s',
                                       origin=pd.Timestamp('%s-1-1'%year))
            month = date_time.month
            day1 = date_time.day
            date_time = pd.to_datetime(stop_stamp,unit='s',
                                       origin=pd.Timestamp('%s-1-1'%year))
            day2 = date_time.day
            list = [start_stamp, stop_stamp, month, day1, day2]
        else:
            list = [10000, 10000, 1, 1, 1]
        return list

    def getval(self,series,status,year,month,day,start_stamp,stop_stamp):
        time_list = gn.get_section(series, 'PRC')
        time_list = self.cut_timelist(time_list, status)
            
        start_time = "%04d-%02d-%02d"%(year,month,day)
        date_time = pd.Timestamp(start_time) - datetime.datetime(year,1,1) # 时间戳锚定日
        time_stamp = date_time.days*86400 + date_time.seconds # 将日期转换为时间戳
        
        start_tlist = (start_stamp - time_stamp) // 3
        stop_tlist = (stop_stamp - time_stamp) // 3
            
        list_val = []
        step = (stop_tlist - start_tlist) // 100
        for i in range(5,100-5):
            tmp = start_tlist + i * step
            list_val.append(series[tmp])
        val = np.mean(list_val)
        val = np.float16("%.4f"%val)
        
        return val


# =============================================================================
# 数据解码,将dataframe数值转换为一般人能理解的语句
# =============================================================================
    def decode(self, df):
        df_ex = pd.DataFrame()
        df_ex['开始时刻'] = df['StartStamp']
        df_ex['结束时刻'] = df['StopStamp']
        df_ex['持续时间(min)'] = df['Interval']
        df_ex['工作状态'] = df['Action']
        
        for i in range(df.shape[0]):
            df_ex.iloc[i,0] = self.stamp2date(df.iloc[i,0],self.year)
        for i in range(df.shape[0]):
            df_ex.iloc[i,1] = self.stamp2date(df.iloc[i,1],self.year)        
        for i in range(df.shape[0]):
            df_ex.iloc[i,2] = df.iloc[i,2] / 20
        for i in range(df.shape[0]):
            if df.iloc[i,3] == 10:
                df_ex.iloc[i,3] = '直抛'
            elif df.iloc[i,3] == 11:
                df_ex.iloc[i,3] = '虹喷'
            else:
                df_ex.iloc[i,3] = '艏吹'      
        return df_ex



if __name__ == '__main__':
    dir_import = "D:\MyCode\Python\Junyang1_data_analysis\Data"
    # year = 2018; month = 11; day1 = 2; day2 = 3;
    year = 2017; month = 5; day1 = 1; day2 = 3;
    section = getUnloadSection(dir_import, year, month, day1, day2)
