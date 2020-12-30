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
def timel():
    array = np.arange(1440)
    hour = array//60
    minute = np.mod(array,60)
        
    tmp = list(array)
    for i in range(1440):
        tmp[i] = "%02d:%02d"%(hour[i],minute[i])
        
    return tmp


# =============================================================================
# 创建时间戳
# =============================================================================
def create_timestamp(year, month, day):
    start_time = "%04d-%02d-%02d"%(year,month,day)
    date_time = pd.Timestamp(start_time) - datetime.datetime(year,1,1) # 时间戳锚定日
    time_stamp = date_time.days*86400 + date_time.seconds # 将日期转换为时间戳
    array = np.arange(1440)
    array_stamp = time_stamp + 60*array
    return array_stamp



# =============================================================================
# 可用于分析的有效数据
# =============================================================================
def getlogname(num):
    dict_cat = {}

    dict_cat[0] = {0:("DLM",18,"平均吃水"),  #已经检查
                   1:("DLM",8,"船舶排水量"),
                   2: ("DLM", 94, "泥舱平均液位"),  # 已经检查
                   3: ("DLM", 114, "空船重"),
                   4:("DLM",115,"空船重参数选择(0自动,1手动)"),
                   5:("DLM",116,"空船重（手动）"),                   
                   6:("DLM",91,"泥舱装舱量(t)"),
                   7:("DLM",95,"泥舱装舱量(m3)"),
                   8:("DLM",92,"泥舱装舱量-湿砂(t)"),
                   9: ("DLM", 96, "泥舱装舱量-湿砂(m3)"),
                   10: ("DLM", 93, "泥舱装舱量-干砂(t)"),
                   11: ("DLM", 97, "泥舱装舱量-干砂(m3)")}
    
    dict_cat[1] = {0:("DOORS",9,"左1泥门开度百分比"),
                   1: ("DOORS", 14, "左6泥门开度百分比"),
                   2: ("DOORS", 27, "右3泥门开度百分比"),
                   3:("DOORS",32,"右8泥门开度百分比")}
    
    dict_cat[2] = {0:("PRC",15,"左耙挖泥浓度"),
                   1:("PRC",24,"左耙挖泥流速"),
                   2:("PRC",25,"右耙挖泥浓度"),
                   3:("PRC",34,"右耙挖泥流速")}
    
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
            
    # 每隔60s保留一条数据
    array = np.arange(0,28800,20)
    df3 = df2.iloc[array]
    
    col_name = df3.columns.tolist()
    col_name.insert(0,"时间")
    col_name.insert(1,'Stamp')
    df3 = df3.reindex(columns=col_name)
    
    time = timel()
    df3["时间"] = time
    time_stamp = create_timestamp(year, month, day)
    df3['Stamp'] = time_stamp
    
    return df3






# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    year = 2019; month = 8; day = 13; # 日志日期
    directory = "D:\MyCode\Python\Junyang1_data_analysis\Data"
    
    df3 = getDataFrame(year,month,day,directory)

    # 格式化输出
    str1 = "%04d_%02d_%02d_Status"%(year,month,day)
    df3.to_csv(str1+".csv",encoding="utf_8_sig",index=False,
                sep=',',columns=col_name)
    
    
    # df = pd.DataFrame({'a':(1,3,2,3,3),'b':(4,5,6,7,8)})
    # is_3 = df['a'] == 3
    # print(df[is_3])
    # df['c'] = df.a.apply(lambda x: 1 if x==3 else 0)