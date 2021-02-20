# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:53:44 2020

@author: Da YIN
"""

import pandas as pd


def get_section(series, log_name):   
    dic_thr_m = {"DOORS":70,
                 "PRC":3}
    threshold = dic_thr_m[log_name]  
    time_list = get_timelist(series, threshold)
    time_list = merge(time_list)
      
    '''
    以下为一般情况下的处理。
    对于类似于171102的挖泥作业状态，不应执行下列函数。
    '''
    num = 28800 // (24*3) # 设定阈值 20min
    dic_thr_i = {"DOORS":0,
                  "PRC":num}
    threshold = dic_thr_i[log_name]
    if threshold > 0 :
        time_list = ignore(time_list, threshold)
        
    return time_list


def get_timelist(series, threshold):
    time_0 = 0; time_1 = 0; # time_2 = 0; 
    time_list = [];
    for i in range(series.shape[0]):
        if series[i] < threshold: # 基于设定阈值判定状态变化
            time_0 = i
        else:
            time_1 = i
        
        if time_1 - time_0 == 1 :
            time_list.append([time_0,0]) 
        elif time_0 - time_1 == 1 :
            time_list.append([time_1,1])
            
    return time_list
    

def merge(time_list):
    # 忽略间断时间小于设定阈值的时段
    num = 28800 # 设定的一天内记录数据的次数
    if len(time_list) >= 4:
        threshold = num // (24*6) # 设定阈值 10min
        time_list_new = []
        
        for i in range(len(time_list)):
            if time_list[i][1] == 0 :
                break
        pointer_start = time_list[i]
        
        for i in range(len(time_list)-2):
            if time_list[i][1] == 0 :
                if (time_list[i+2][0] - time_list[i+1][0]) > threshold:
                    pointer_stop = time_list[i+1]
                    time_list_new.append(pointer_start)
                    time_list_new.append(pointer_stop)
                    pointer_start = time_list[i+2]

        j = len(time_list)
        if time_list[j-1][1] == 1:
            pointer_stop = time_list[j-1]
            time_list_new.append(pointer_start)
            time_list_new.append(pointer_stop)
        elif time_list[j-2][0] > pointer_start[0]:
            pointer_stop = time_list[j-2]
            time_list_new.append(pointer_start)
            time_list_new.append(pointer_stop)
    else:
        time_list_new = time_list
            
    return time_list_new


def ignore(time_list, threshold):
    # 忽略合并后区间长度小于设定阈值的时段
    if len(time_list) >= 2:
        time_list_new = []
        
        for i in range(len(time_list)-1):
            if time_list[i][1] == 0 and (time_list[i+1][0] - time_list[i][0]) > threshold:
                time_list_new.append(time_list[i])
                time_list_new.append(time_list[i+1])
    else:
        time_list_new = time_list
            
    return time_list_new


# =============================================================================
# 计算单/双耙工作区间
# =============================================================================
# 获取区间交集
# A, B 形如 [[0,2],[5,10]...]
def intervalIntersection(A, B):
    i, j = 0, 0 # 双指针
    res = []
    while i < len(A) and j < len(B):
        # a1, a2 = A[i][0], A[i][1]
        # b1, b2 = B[j][0], B[j][1]
        a1, a2 = A.iloc[i,0], A.iloc[i,1]
        b1, b2 = B.iloc[j,0], B.iloc[j,1]
        # 两个区间存在交集
        if b2 >= a1 and a2 >= b1:
            # 计算出交集，加入 res
            c1 = max(a1, b1)
            c2 = min(a2, b2)
            res.append([c1, c2, c2-c1, 22]) # 22代表双耙同时施工
        # 指针前进
        if b2 < a2: j += 1
        else:       i += 1
        
    return res
        

# 获取区间差集
# C为A，B交集
def intervalDiff(A, C):
    i, j = 0, 0
    res = []
    while  i < len(A) and j < len(C):
        a1, a2, action = A.iloc[i,0], A.iloc[i,1], A.iloc[i,3]
        c1, c2 = C.iloc[j,0], C.iloc[j,1]
        # 两区间存在差集
        if (a1 - c1)*(a2 - c2) <= 0:
            # 添加判定阈值，设为3min
            if c1-a1 > 60:
                res.append([a1, c1, c1-a1, action])
            if a2-c2 > 60:
                res.append([c2, a2, a2-c2, action])
        # 指针前进
        if c2 < a2: j += 1
        else:       i += 1
        
    return res


# =============================================================================
# TEST-测试
# =============================================================================
if __name__ == "__main__":
    pass

                
