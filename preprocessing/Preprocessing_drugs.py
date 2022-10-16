# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:36:07 2022

@author: YC
"""
import pandas as pd
import numpy as np
import re

# 合併檔案內資料
def combine3drugs(data):
    #df = pd.read_csv('new_test_drugs2.csv') #,encoding='cp1252'
    df = pd.read_csv('./dataset/combineAllDrugs2.csv',encoding= 'unicode_escape') #,encoding='cp1252'
    print(df)


    
    lst_new=[]
    
    for i in range(df.shape[0]):# df.shape[0] -> row
        string=""
        for name in data:
            print(name)
            if isinstance(df[name][i], str):#不是NaN 
                string+=df[name][i]+" "
        print(string)
        lst_new.append(string)
        
    print(len(lst_new))
    
    dict = {'combineData':lst_new} 
    df = pd.DataFrame(dict) 
    df.to_csv('./dataset/com_drugs.csv',index=0)
    #df.to_csv('./result/comineDrugs_DS.csv',index=0)#index=0 沒有第一col的id
#合併combineDrugs_DT ab DS -> combineAllDrugs2


#---------------------------------
# drugs 前處理
# df.shape[0] -> row
# df.shape[1] -> col
# CSV 先取代 — 英文補充符號
# ??讀不出來進CSV刪除(格式轉換出現的??)
#---------------------------------
def preprocDrugs(col):
    
    #df = pd.read_csv('temp_reD.csv',encoding="gb18030")
    #df = pd.read_csv('new_test_drugs.csv')#沒轉乾淨再轉一次
    df = pd.read_csv('./result/combineAllDrugs2.csv',encoding="gb18030")#沒轉乾淨再轉一次
    dict = {}
    
    for c in col:
        drugs = df[c].tolist()
        
        df_new_test=[]
        for i in range(len(drugs)):
            String1 = str(drugs[i]).replace('404','')
            #String1 = drugs[i].replace('404','')
            
            
            f = open('drugs_slash.txt', 'r')
            for line in f.readlines():
                String1 = String1.replace(line.strip(),' ')#計量單位            
            f.close
            
            String1 = String1.replace('and/or','and or')
            String1 = String1.replace('Cardiology/American','Cardiology American')
            String1 = String1.replace('Sequential/Sepsis-related','Sequential Sepsis-related')
            String1 = String1.replace('ME/CFS','ME CFS')
 
            #沒句號的地方加句號
            PeriodRegex = re.compile(r'[A-Za-z0-9]+\n')#匹配換行前沒句點
            result_P = PeriodRegex.findall(String1)
            #print(result_P)
            for line in result_P:
                tmp = line.replace("\n",".\n")
                print(tmp)
                print(line)
                String1 = String1.replace(line,tmp) 
                
                
            String1 = String1.replace('NO Diagnosis','')
            String1 = String1.replace("?"," ")
            String1 = String1.replace("??"," ")
            String1 = String1.replace('"',' ')
            String1 = String1.replace(',',' ')
            #String1 = String1.replace('.',' ')
            String1 = String1.replace(':',' ')
            String1 = String1.replace(';',' ')
            String1 = String1.replace('%',' ')
            String1 = String1.replace('$',' ')
            String1 = String1.replace('percent',' ')
            String1 = String1.replace('Percent',' ')
            String1 = String1.replace('(s) ',' ')
            String1 = String1.replace('\n',' ')
            String1 = String1.replace("'s",'')
            String1 = re.sub('[\ ]{2,}', ' ', String1)#保留一個空格
            
            df_new_test.append(String1)
        
        #dict[c+'_old'] = drugs
        #dict[c+'_new'] = df_new_test
        dict[c] = df_new_test
    
    df = pd.DataFrame(dict) 
    #df.to_csv('./new_test_drugs.csv',index=0)#index=0 沒有第一col的id
    df.to_csv('./new_test_drugs2.csv',index=0)
    

#---------------------------------
# 找 xxx/xxx
# 先執行preprocDrugs將符號取代成空格(防止' ME/CFS.')
# 再執行findAllSlash
# 先回去執行preprocDrugs取代
#---------------------------------
def findAllSlash(col):
    
    df = pd.read_csv('new_test_drugs.csv',encoding="gb18030")
    df_result=[]
    for c in col:
        drugs = df[c].tolist()#一col
        for i in range(len(drugs)):#一col中的一筆
            SlashRegex = re.compile(r'\ [a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\ |\([a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\)')
            result = SlashRegex.findall(str(drugs[i]))
            #print(result)
            #Slash = '\n'.join(result)
            #print('Phone Number: \n' + Slash)
            df_result = df_result + result
        
    #print(len(df_result))
        #print(df_result)
    df_result_Deduplication = set(df_result)#去重複
    lst_slash = list(df_result_Deduplication)
    mylist = sorted(lst_slash, reverse=True)#括號放前先刪 (mg/dL), mg/dL
    
    #print(df_result_Deduplication)

    
    with open('drugs_slash.txt', 'w') as f: # w → 複寫 r → 讀取 a → 增寫
        for i in mylist:    
            f.write(i+"\n")
    f.close()

# !!刪掉不想刪的!!
# and/or 
# Sequential/Sepsis-related 
# ME/CFS 
# Cardiology/American 


    
# ================= Main =================


#col = ['DT1','DT2','DT3','ab1','ab2','ab3','DS1','DS2','DS3']#全都 141 row
#col = ['DT1_new','DT2_new','DT3_new','ab1_new','ab2_new','ab3_new','DS1_new','DS2_new','DS3_new']
col = ['DT','ab','DS']
#preprocDrugs(col)
#findAllSlash(col)

#data = ['DT1_new','DT2_new','DT3_new','ab1_new','ab2_new','ab3_new','DS1_new','DS2_new','DS3_new']
#data = ['DT1_new','DT2_new','DT3_new']
#data = ['ab1_new','ab2_new','ab3_new']
#data = ['DT_new','ab_new','DS_new']
#data = ['DS1_new','DS2_new','DS3_new']
#combine3drugs(data)
combine3drugs(col)

#檢查
'''
df = pd.read_csv('new_test_drugs2.csv',encoding="gb18030")
drugs = df['DT2_new'].tolist()
print(len(drugs))
print(drugs[48])
'''










