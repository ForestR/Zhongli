# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:48:23 2020

@author: Da YIN
"""

import pandas as pd
# import datetime
import numpy as np
from pandas.io.common import EmptyDataError, ParserError
import datetime


# =============================================================================
# 导入CSV数据
# =============================================================================
def importdata(year,month,day,log_name,directory):
    '''打开文件'''
    date = "%04d_%02d_%02d"%(year,month,day) 
    filename = directory + "/"+date+"/"+date+"_%s_LOG_T.csv"%log_name
    try:
        df = pd.read_csv(filename, sep='\\s+', skiprows=[0], 
                          header=None) # 原始数据
        status = 1
        
    except EmptyDataError:
        # csv文件数据为空
        print("EmptyDataError: "+filename)
        df = pd.DataFrame()
        status = 0
        
    except ParserError:
        # Expected 133 fields in line 6, saw 134
        df = pd.read_csv(filename, sep='\\s+', skiprows=[0], 
                          header=None, delimiter="\t")
        status = 1
        
    except FileNotFoundError:
        # csv does not exist
        print("FileNotFoundError: "+filename)
        df = pd.DataFrame()
        status = 0
        
    return df,status

# =============================================================================
# 创建时间列
# =============================================================================
def timel(size):
    length = int(np.ceil(size/20))
    array = np.arange(length) # 1440
    hour = array//60
    minute = np.mod(array,60)
        
    tmp = list(array)
    for i in range(length): # 1440
        tmp[i] = "%02d:%02d"%(hour[i],minute[i])
        
    return tmp

# =============================================================================
# 创建时间戳
# =============================================================================
def create_timestamp(year, month, day, size):
    start_time = "%04d-%02d-%02d"%(year,month,day)
    date_time = pd.Timestamp(start_time) - datetime.datetime(2010,1,1) # 时间戳锚定日
    time_stamp = date_time.days*86400 + date_time.seconds # 将日期转换为时间戳
    length = int(np.ceil(size/20))
    array = np.arange(length) # 1440
    array_stamp = time_stamp + 60*array
    return array_stamp

# =============================================================================
# 可用于分析的有效数据
# =============================================================================
def getlogname(num):
    dict_cat = {}

    dict_cat[0] = {0:("DLM",18,"平均吃水"),  #已经检查
                   1:("DLM",8,"船舶排水量"),
                   2: ("DLM",94,"泥舱平均液位"),  # 已经检查
                   3: ("DLM",114,"空船重"),
                   4:("DLM",115,"空船重参数选择(0自动,1手动)"),
                   5:("DLM",116,"空船重（手动）"),                   
                   6:("DLM",91,"泥舱装舱量(t)"),
                   7:("DLM",95,"泥舱装舱量(m3)"),
                   8:("DLM",92,"泥舱装舱量-湿砂(t)"),
                   9: ("DLM",96,"泥舱装舱量-湿砂(m3)"),
                   10: ("DLM",93,"泥舱装舱量-干砂(t)"),
                   11: ("DLM",97,"泥舱装舱量-干砂(m3)")}
    
    dict_cat[1] = {0:("DOORS",5,"大泥门组1"),
                   1: ("DOORS",7,"大泥门组3"),
                   2: ("DOORS",9,"左1泥门开度百分比"),
                   3:("DOORS",32,"右8泥门开度百分比")}
    
    dict_cat[2] = {0:("PRC",5,"排岸浓度"),
                   1:("PRC",14,"排岸流速"),
                   2:("PRC",15,"左耙挖泥浓度"),
                   3:("PRC",24,"左耙挖泥流速"),
                   4:("PRC",25,"右耙挖泥浓度"),
                   5:("PRC",34,"右耙挖泥流速")}
    
    dict_cat[3] = {0:("STPM",12,"左耙吸入海图深度"),
                   1:("STPM",44,"右耙吸入海图深度")}

    dict_cat[4] = {0:("DRGPUMPS",26,"左水下泵驱动功率"),
                   1:("DRGPUMPS",60,"右水下泵驱动功率"),
                   2:("DRGPUMPS",6,"左舱内泵驱动功率"),
                   3:("DRGPUMPS",40,"右舱内泵驱动功率")}

    dict_cat[5] = {0: ("POWER", 6, "右辅机功率kw"),
                   1: ("POWER", 9, "左主机功率"),
                   2: ("POWER", 12, "右主机功率"),
                   3: ("POWER", 15, "左辅机功率")}

    dict_log = dict_cat[num]
    return dict_log


def getDataFrame(year,month,day,directory):
    df2 = pd.DataFrame()
    for i in range(6):
        dict_log = getlogname(i)
        log_name = dict_log[0][0] # 日志名
        df,status = importdata(year,month,day,log_name,directory)
        
        # 检测时间戳列索引计数是否与预期一致
        try:
            date = df.iloc[0,2]
            if type(date) == str:
                for j in range(len(dict_log)): # 134行数据时
                    cid = dict_log[j][1]
                    cstr = dict_log[j][2]
                    df2[cstr] = df[cid]
            else:
                for j in range(len(dict_log)): # 136行数据时
                    cid = dict_log[j][1] - 2
                    cstr = dict_log[j][2]
                    df2[cstr] = df[cid]
                    
            if i == 0:
                df2 = amendment(df, df2) # 修正错位
                    
        except IndexError:
            print(year,month,day,log_name,'日志为空')
        except KeyError:
            print(year,month,day,log_name,'日志为空')
            
    # 每隔60s保留一条数据
    # array = np.arange(0,28800,20)
    array = np.arange(0,df2.shape[0],20)
    df3 = df2.iloc[array]
    
    
    
    col_name = df3.columns.tolist()
    col_name.insert(0,'日期')
    col_name.insert(1,"时间")
    col_name.insert(2,'Stamp')
    df3 = df3.reindex(columns=col_name)
    
    df3['日期'] = "%04d-%02d-%02d"%(year,month,day)
    time = timel(df2.shape[0])
    df3["时间"] = time
    time_stamp = create_timestamp(year, month, day, df2.shape[0])
    df3['Stamp'] = time_stamp
    
    df4 = judgeStatus(df3,year,month,day)
    return df4


def judgeStatus(df,year,month,day):
    try:
        df['主机总功率'] = df['左主机功率'] + df['右主机功率'] # 应汪工要求添加
    except KeyError:
        print(year,month,day,'主机功率缺失')
    
    df['作业状态'] = '待定' # 新建列
    
    try:
        cond1 = df['大泥门组1'] > 70 # 直抛
        
        cond2_1 = df['排岸流速'] > 2
        cond2_2 = df['排岸流速'] <= 5
        cond2_3 = df['排岸流速'] > 5
        try:
            cond2_4 = df['左舱内泵驱动功率'] + df['右舱内泵驱动功率'] > 2000
            cond2a = (cond2_1 & cond2_4) & cond2_2 # 艏吹
            cond2b = cond2_3 & cond2_4 # 虹喷
        except KeyError:
            cond2a = cond2_1 & cond2_2 # 艏吹
            cond2b = cond2_3 # 虹喷
            
        cond3_1 = df['左耙挖泥流速'] > 4
        try:
            cond3_2 = df['左水下泵驱动功率'] > 1000
            cond3 = cond3_1 & cond3_2 # 左耙挖泥 # 使用and语句，减少状态的突变
        except KeyError:
            cond3 = cond3_1 # 左耙挖泥
        
        cond4_1 = df['右耙挖泥流速'] > 4
        try:
            cond4_2 = df['右水下泵驱动功率'] > 1000
            cond4 = cond4_1 & cond4_2 # 右耙挖泥
        except KeyError:
            cond4 = cond4_1
        
        # 注意：检修时会满水空砂，不宜使用'泥舱装舱量(m3)'，例190813
        # 注意：此处阈值应根据实际情况调整
        try:
            cond5 = df['泥舱装舱量-湿砂(m3)'] > 5000 # 重载 
            df.loc[cond5, '作业状态'] = '重载'
            df.loc[~ cond5, '作业状态'] = '轻载' # 注意：此处把停工的情况也囊括在'轻载'中了
        except KeyError:
            pass
    
        # 按优先级从低到高的顺序进行状态复写
        df.loc[cond4, '作业状态'] = '右耙'
        df.loc[cond3, '作业状态'] = '左耙'
        df.loc[cond3 & cond4, '作业状态'] = '双耙'
        df.loc[cond2b, '作业状态'] = '虹喷'
        df.loc[cond2a, '作业状态'] = '艏吹'
        df.loc[cond1, '作业状态'] = '直抛'
    except KeyError:
        print(year,month,day,'核心判据缺失')
    return df

def amendment(df, df2):
    try:
        cond = df2['空船重'] == 0
        if df2.loc[cond].shape[0] > 0: # DLM数据读取发生错位
            df_tmp = pd.DataFrame()
            df_tmp['泥舱比重计算值'] = df[113]

            # 顺次替换错位数据
            df2.loc[cond,'空船重（手动）'] = df2.loc[cond,'空船重参数选择(0自动,1手动)']
            df2.loc[cond,'空船重参数选择(0自动,1手动)'] = df2.loc[cond,'空船重']
            df2.loc[cond,'空船重'] = df_tmp.loc[cond,'泥舱比重计算值']

    except KeyError:
        print(year,month,day,'空船重缺失')
    return df2


# =============================================================================
# TEST
# =============================================================================
if __name__ == "__main__":
    # year = 2018; month = 2; day = 1; # 日志日期
    # directory = "D:\MyCode\Python\Junyang1_data_analysis\Data"
    # df4,df = getDataFrame(year,month,day,directory)
    
    dir_import = 'D:\MyCode\Python\Junyang1_data_analysis\Data'
    dir_export = 'D:\MyProject\耙吸船定额分析\[201231]俊洋一数据库\_2019'
    year = 2019
    # month = 2; day1 = 1; day2 = 1;
    
    dic = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30,
           7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    day1 = 1
    for month in range(11,12):
        day2 = dic[month]
        for day in range(day1, 1+day2):
            df = getDataFrame(year,month,day,dir_import)
            
            str1 = "%04d_%02d_%02d_Moment"%(year,month,day)
            filename = r''+dir_export+"/"+str1+".csv"
            col_name = df.columns.tolist()
            df.to_csv(filename,encoding="utf_8_sig",index=False,
                      sep=',',columns=col_name)