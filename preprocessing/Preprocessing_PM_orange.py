# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:08:15 2022

檢查100個ICD有無重複
PubMed前處理-Orange

https://www.activestate.com/resources/quick-reads/how-to-delete-a-column-row-from-a-dataframe/
https://www.delftstack.com/zh-tw/howto/python-pandas/pandas-drop-rows-with-nan/
http://liao.cpython.org/pandas20.html#204-dropna
https://blog.csdn.net/calorand/article/details/53742290

@author: YC
"""
import pandas as pd
import os


#===================================================
# 檢查100筆資料是否存在
#===================================================
def check():
    df = pd.read_csv('temp_reD.csv')
    #print(df)#查看CSV資料
    
    ICD_code = df['ICD'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
    print(ICD_code)
    
    #lst_check=[]
    for i in range(len(ICD_code)):
        cnt=0
        for j in range(len(ICD_code)):
            if ICD_code[i]==ICD_code[j]:
                cnt=cnt+1
                if cnt >= 2 :
                    print(ICD_code[i])
def check2():
    import os
    allList = os.walk('./dataset/PM_updata/new')
    
    # 列出所有子目錄與子目錄底下所有的檔案
    
    for root, dirs, files in allList:
    
    #   列出在這個路徑下讀取到的所有檔案
    
      print("file：", files)
      
    df = pd.read_csv('ICD_upd.csv')
    ICD_code = df['ICD10'].tolist()
    
    for i in ICD_code:
        if i+".csv" not in files:
            print(i+" NOT IN files")
        
  

#===================================================
# PubMed資料前處理
# (1)Orange取date2017-2021資料 去空值
#===================================================
def Orange():
    df = pd.read_csv('temp_reD.csv',encoding="gb18030")
    ICD_String = df['ICD_String'].tolist()
    #ICD = df['ICD10'].tolist() 
    
    
    #錯誤的項目
    ICD = ['I21','J69','S22','K35','N10']
    #ICD_String =['Acute myocardial infarction','Pneumonitis due to solids and liquids','Fracture of rib(s)', 
    #'sternum and thoracic spine','Acute appendicitis','Acute tubulo-interstitial nephritis']
                
    
    
    
    print("ICD",len(ICD))
    print("ICD_String",len(ICD_String))
    
    
    for i in range(len(ICD_String)):
        
        flag = os.path.isfile('C:/Users/YC/Desktop/17yTo21y/'+ICD_String[i]+'.csv')
    
        
        if flag == False:
            print(ICD[i])
        else:
            try:
                df_PM = pd.read_csv('C:/Users/YC/Desktop/17yTo21y/'+ICD_String[i]+'.csv',encoding="gb18030")
                #df_PM = pd.read_csv('C:/Users/YC/Desktop/17yTo21y/Candidiasis.csv',encoding="gb18030")
                
               
                df_PM1 = df_PM.filter(items=['title', 'abstract','date'])#保留這三col
    
                df_PM1.drop(df_PM1.index[(df_PM1[ "date" ] == "?" )],axis= 0 ,inplace= True )#date中有?的值刪除整row
                
    
                #cnt=0 
                for date in df_PM1['date']:
                    year = date.split('-')
                    #print(year)
                    if int(year[0])<2017 or int(year[0])>2021:#時間範圍外的刪除
                        #cnt=cnt+1
                        #print('Out',year[0])
                        df_PM1.drop(df_PM1.index[(df_PM1[ "date" ] == date )],axis= 0 ,inplace= True )
                        
                #print(df_PM)
                df_PM_Nnan = df_PM1.dropna(axis=0, how='any')#刪除所有空值 因其不改變原始df所以給定新變數
                #print(df_PM_Nnan)
                
                df_PM_Nnan.to_csv("./PubMed_data/t/"+ICD[i]+".csv")
                
            except Exception as e:
                print(e)
                print(f'ICD: {ICD[i]} String: {ICD_String[i]}')


def Orange_update():
    #df = pd.read_csv('ICD_upd.csv',encoding="gb18030")
    #ICD = df['ICD10'].tolist()
    
    ICD=['I25','C50','K76']#出現錯誤 split('/')
    
    for i in range(len(ICD)):
        
        flag = os.path.isfile('./dataset/PM_updata/'+ICD[i]+'.csv')
        #flag = os.path.isfile('./dataset/PM_updata/A41.csv')
        
        if flag == False:
            print(ICD[i],"不存在")
        else:
            try:
                df_PM = pd.read_csv('./dataset/PM_updata/'+ICD[i]+'.csv',encoding="gb18030")
                #df_PM = pd.read_csv('./dataset/PM_updata/A41.csv',encoding="gb18030")
               
                df_PM1 = df_PM.filter(items=['title', 'abstract','date'])#保留這三col
    
                df_PM1.drop(df_PM1.index[(df_PM1[ "date" ] == "?" )],axis= 0 ,inplace= True )#date中有?的值刪除整row
                #print(df_PM1)
           
                for date in df_PM1['date']:
                    #year = date.split('-')
                    year = date.split('/')
                    if int(year[0])<2017 or int(year[0])>2021:#時間範圍外的刪除
                        df_PM1.drop(df_PM1.index[(df_PM1[ "date" ] == date )],axis= 0 ,inplace= True )
                        
                #print(df_PM1)
                df_PM_Nnan = df_PM1.dropna(axis=0, how='any')#刪除所有空值 因其不改變原始df所以給定新變數
                #print(df_PM_Nnan)
                
                df_PM_Nnan.to_csv("./dataset/PM_updata/new/"+ICD[i]+".csv")
                #df_PM_Nnan.to_csv("./dataset/PM_updata/new/A41.csv",index=0)
            except Exception as e:
                print(e)
                #print(f'ICD: {ICD[i]} ')
            
            
Orange_update()
#check2()