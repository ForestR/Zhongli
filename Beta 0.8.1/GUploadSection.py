# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 10:56:21 2020

创建俊洋一日志处理程序的父类构造函数——装舱状态识别

@author: Da YIN
"""

import pandas as pd
import General as gn
import datetime
from pandas.io.common import EmptyDataError, ParserError


# class getUploadSection(object): # Python 2
class getUploadSection: # Python 3 

    def __init__(self, dir_import, year, month, day1, day2):
        self.dir_import = dir_import
        self.year = year
        self.month = month
        self.day1 = day1
        self.day2 = day2
        self.df = self.setUp()


    def setUp(self): 
        self.dic_poi = {20:("Dredging_L",3,1),
                        21:("Dredging_R",3,5)}    
        self.dict_log = {1:("PRC",24,"左耙挖泥流速"),
                         5:("PRC",34,"右耙挖泥流速")}
        df = pd.DataFrame()
        
        '''计算左耙工作区间'''
        new_log = []
        self.action = 20
        for self.day in range(self.day1, 1 + self.day2):
            log_act = self.getlogact()
            log_act = self.dredge(log_act)
            for x in log_act: new_log.append(x)
        log_act = self.revise(new_log)
        if log_act != []:
            order = ["StartStamp","StopStamp","Interval","Action"]
            df_dgl = pd.DataFrame(log_act,columns = order)
            df = df.append(df_dgl,ignore_index=True)
            # print(df.head(3)); print('');

        '''计算右耙工作区间'''
        new_log = []
        self.action = 21
        for self.day in range(self.day1, 1 + self.day2):
            log_act = self.getlogact()
            log_act = self.dredge(log_act)
            for x in log_act: new_log.append(x)
        log_act = self.revise(new_log)
        if log_act != []:
            order = ["StartStamp","StopStamp","Interval","Action"]
            df_dgr = pd.DataFrame(log_act,columns = order)
            df = df.append(df_dgr,ignore_index=True)
            # print(df.head(3)); print('');
        
        try:
            df.sort_values(by=["StartStamp"],ascending=[True],inplace=True)   
            # print(df.head(3)); print('');

            '''计算双耙工作区间'''
            tmp = []
            self.action = 22
            df_int = gn.intervalIntersection(df_dgl, df_dgr)
            tmp += df_int
            df_int = pd.DataFrame(df_int,columns = order)
            res = gn.intervalDiff(df_dgl, df_int)
            tmp += res 
            res = gn.intervalDiff(df_dgr, df_int)
            tmp += res
            df_new = pd.DataFrame(tmp,columns = order)
            df_new = df_new.sort_values(by="StartStamp")
            df_new.reset_index(drop=True,inplace=True)  # 修正索引
            return df_new
        
        except KeyError:
            df_new = pd.DataFrame()
            return df_new
    
        # df_ex = self.decode(df_new)
        # print(df_ex.head(3))

        # # 格式化输出
        # str1 = "%04d_%02d_%02d~%02d_Status"%(self.year,self.month,self.day1,self.day2)
        # col_name = df_ex.columns.tolist()
        # df_ex.to_csv(str1+".csv",encoding="utf_8_sig",index=False,
        #             sep=',',columns=col_name)        


# =============================================================================
# Dredging
# =============================================================================
    def dredge(self, log_act):
        new_log = []
        for i in range(len(log_act)):
            start_stamp = log_act[i][0]
            stop_stamp = log_act[i][1]
            tmp = [start_stamp, stop_stamp, stop_stamp-start_stamp, self.action]
            new_log.append(tmp)
        log_act = new_log
        return log_act


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
        time_list = gn.get_section(series, 'PRC')
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
            if df.iloc[i,3] == 20:
                df_ex.iloc[i,3] = '左耙'
            elif df.iloc[i,3] == 21:
                df_ex.iloc[i,3] = '右耙'
            else:
                df_ex.iloc[i,3] = '双耙'      
        # print(df_ex.head(3))
        return df_ex


if __name__ == '__main__':
    dir_import = "D:\MyCode\Python\Junyang1_data_analysis\Data"
    # year = 2018; month = 11; day1 = 2; day2 = 3;
    year = 2017; month = 5; day1 = 1; day2 = 3;
    section = getUploadSection(dir_import, year, month, day1, day2)
