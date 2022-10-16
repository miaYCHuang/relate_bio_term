# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:48:34 2022

@author: YC
"""
import pandas as pd
import matplotlib.pyplot as plt

# def countLevel():

#     dic={}
#     for title in lst_title:
#         lst = df1[title].tolist()
#         lst_count=[]
#         for i in range(1,11,1):#1-10
#             lst_count.append(lst.count(i))
#         dic[title]= lst_count
#     df = pd.DataFrame(dic)
#     return df
#        # df.to_csv('./dataset/gram/'+name+'_'+str(num)+'-gram.csv',index=0)
# df_ansCnt=countLevel()

# df_ansCnt.to_csv('ansCnt.csv',index=0)

#%%
#答案處理
#去離群
import numpy as np
from collections import Counter
from itertools import groupby

df1= pd.read_csv('temp_reD.csv')

lst_mean=[]
lst_mode=[]
for i in range(1,101,1):
    ans = sorted(df1[str(i)])
    print(ans)
    #眾數 (相同數量取平均)
    freqs = groupby(Counter(ans).most_common(), lambda x:x[1])
    lst_frq=[val for val,count in next(freqs)[1]]
    lst_mode.append(np.mean(lst_frq))
    print(np.mean(lst_frq))
    # array = np.array(ans)
    # vals,counts = np.unique(array, return_counts=True)
    # index = np.argmax(counts)
    # lst_mode.append(vals[index])
    # print(vals[index])
    
    
    #去最大最小取平均
    ans.pop(0)#去第一個
    ans.pop(7)#去最後一個
    lst_mean.append(round(sum(ans)/7, 4))
    print(ans)
    print("*********")
dict = {'mean': lst_mean,'mode': lst_mode}
df_all = pd.DataFrame(dict)
df_all.to_csv('ansFin.csv',index=0)

#%%


l = [1,2,3,3,3,4,4,4,5,5,6,6,6]



