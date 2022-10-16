# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:44:44 2022
停用詞
https://blog.droidtown.co/post/188714326387/articutnlp04
cmd打 -> import nltk -> nltk.download('stopwords')
@author: YC
"""
import re
import pandas as pd
import numpy as np
import os


#---------------------------------
# 找尋特殊字元
#---------------------------------
def is_encomm_char(ch):
    """
    https://www.tangkin.com/index.php/archives/py_ascii.html
    chk txt is include alphabeta,number,symbol
    :param ch:
    :return:CHK_TXT_NOEN noen txt num,NOEN_TXT
    :return txt_num:noen txt
    簣
    """
    CHK_TXT_NOEN = 0
    NOEN_TXT = []
    
    for t in ch:
        #print(t,"--------",ord(t))
        if ord(t) not in range(30, 127):
            CHK_TXT_NOEN += 1
            NOEN_TXT.append(t)
        else:
            pass
    
    return  NOEN_TXT#CHK_TXT_NOEN,





#---------------------------------
# 單筆資料的特殊字元 100筆中的一筆
# 去重複
#---------------------------------
def notASCII(csv_name):
    
    df = pd.read_csv('./dataset/'+csv_name+'.csv',encoding= 'unicode_escape') #error的使用
    abstract = df['combineData'].tolist()
    #abstract = df['abstract'].tolist()
    
    notASCII = []
    for i in range(len(abstract)):
        if isinstance(abstract[i], str):#不是NaN 
            if is_encomm_char(abstract[i]) != []:
                #print(i,is_encomm_char(abstract[i]))
                for c in is_encomm_char(abstract[i]):
                    notASCII.append(c)
            
            #print(i)
    #print('OK')
    notASCII_Deduplication = set(notASCII)#去重複
    
    lst_notASCII = list(notASCII_Deduplication)
    print('not ASCII:',lst_notASCII)
    
    return lst_notASCII






#---------------------------------
# 處理ASCII外的字元 亂碼
# PM 之前跑過可以不跑
#---------------------------------
def preAS(csv_name):
    try:
        df = pd.read_csv('./dataset/'+csv_name+'.csv',encoding= 'unicode_escape')#error的使用
        #df = pd.read_csv('D:/anaconda_code/PubMed_data/'+csv_name+'.csv',encoding= 'unicode_escape')#,encoding="gb18030"
       
        abstract = df['combineData'].tolist()
        #abstract = df['abstract'].tolist()
        
        #print(len(abstract))
        lst_notASCII = notASCII(csv_name)
        
        
        #print(lst_notASCII)
        lst_old=[]
        lst_new=[]
        for i in range(len(abstract)):
            if isinstance(abstract[i], str):#不是NaN 
                String1 = abstract[i]
                lst_old.append(abstract[i])
                
                #取代不常見的字 'Â', '±','Î', '²'...
                for ch in lst_notASCII:
                    String1 = String1.replace(ch,'')
                    #print(notASCII(csv_name))
                
                lst_new.append(String1)
        #print(df)
        dict = {'asc_data': lst_new}
        df = pd.DataFrame(dict)
        #df = df.assign(asc_data = lst_new)#增加在原本後面
        #print(df)
        df.to_csv('./dataset/asc_'+csv_name+'.csv',index=0)#index=0 沒有第一col的id
        #df.to_csv('./dataset/PM/asc_'+csv_name+'.csv',index=0)#index=0 沒有第一col的id
        
      
    except Exception as e:
        print(e)



def preprocfinal(csv_name):
    df = pd.read_csv('./dataset/asc_'+csv_name+'.csv')
    #df = pd.read_csv('./dataset/PM_updata/new/5K/'+csv_name+'.csv')
    
    #col = df['abstract'].tolist()#asc_data
    col = df['asc_data'].tolist()#asc_data
    dict={}


        
    df_new_test=[]
    for i in range(len(col)):
        String1 = str(col[i]).replace('?','')
        String1 = String1.replace("(","")
        String1 = String1.replace(")","")
        String1 = String1.replace("[","")
        String1 = String1.replace("]","")
        #String1 = re.sub('\.\ ', ' ', String1) #PubmedM不跑
        String1 = re.sub('\,\ ', ' ', String1)
        String1 = re.sub('\ \-\ ', ' ', String1)
        String1 = re.sub('[\ ]{2,}', ' ', String1)#保留一個空格
        
        
        
        
        #PubmedM不跑
        DotRegex = re.compile(r'[a-z]+\.[A-Z]+')#小寫.大寫
        result = DotRegex.findall(String1)
        if result:
            print(i,result)
            for rem in result:
                #print(rem)
                String1 = String1.replace(rem,rem.replace('.',' '))#(heartbeat.R,heartbeat R)
                #print(String1)
        
        
        
        
        df_new_test.append(String1)
        
        

    dict['pre_asc_data'] = df_new_test
    
    df = pd.DataFrame(dict) 
    #df.to_csv('./dataset/PM_updata/new/5K/pre_asc_'+csv_name+'.csv',index=0)
    df.to_csv('./dataset/pre_asc_'+csv_name+'.csv',index=0)
  


#---------------------------------
# 轉小寫
# 去停用詞
#---------------------------------
def stop_word(csv_name):
    from nltk.corpus import stopwords
    #df = pd.read_csv('./dataset/PM_updata/new/5K/pre_asc_'+csv_name+'.csv')
    df = pd.read_csv('./dataset/pre_asc_'+csv_name+'.csv')
    col = df['pre_asc_data'].tolist()
    dict={}
    
    lst_new = []
    EngStopWords = set(stopwords.words('english'))#這裡設定稍後取用 English 的停用詞語料庫
    #text = "Your healthcare provider will take your blood pressure at several visits"
    #low_text = text.lower()
    #print(low_text)
    
    
    for i in range(len(col)):
        low_text = col[i].lower()
        
        String = ''
        for word in low_text.split():
            if word in EngStopWords:
                pass #停用詞
            else:
                String = String + word +" "
    
        print(String)
        lst_new.append(String)
    
    dict['stop_pre_asc_data'] = lst_new
    
    df = pd.DataFrame(dict) 
    df.to_csv('./dataset/stop_pre_asc_'+csv_name+'.csv',index=0)
    #df.to_csv('./dataset/PM_updata/new/5K/stop_pre_asc_'+csv_name+'.csv',index=0)
    
#---------------------------------
# 檢查
# 檢查檢驗項目是否在文本
# 確保檢驗在文本中 不會導致模型輸不出的狀況
#---------------------------------        

def intxtornot(csv_name):
    lst = []
    df = pd.read_csv('./dataset/PM/stop_pre_asc_'+csv_name+'.csv')
    col = df['stop_pre_asc_data'].tolist()
    
    df2 = pd.read_csv('t.csv')
    test = df2['pair1'].tolist()
    
    for j in range(len(test)):
        for i in range(len(col)):
        
            if test[j].lower() in col[i] :
                print(test[j],":",j," match ",csv_name,":",i )
                lst.append(j)
                break
    
    return list(set(lst))
    




        
#wiki drugs   
#preAS('com_drugs')#com_drugs wiki_T
#preprocfinal('com_drugs')
stop_word('com_drugs')#com_wiki



'''
lst_cnt=[]
#PM
df1= pd.read_csv('ICD_upd.csv')#100.csv
ICD10 = df1['ICD10'].tolist()
for i in range(len(ICD10)):
    #preAS(ICD10[i])
    #preprocfinal(ICD10[i])
    stop_word(ICD10[i])
    #lst_cnt = lst_cnt + intxtornot(ICD10[i])
    #print(set(lst_cnt))

'''
#S = intxtornot('J15')
#print(S,len(S))



#%%

import os
#path=input('请输入文件路径(结尾加上/)：')       

#获取该目录下所有文件，存入列表中
fileList=os.listdir('./dataset/PM_updata/new/5K/update5K')

n=0
for i in fileList:
    
    #设置旧文件名（就是路径+文件名）
    oldname='./dataset/PM_updata/new/5K/update5K/'+ os.sep + fileList[n]   # os.sep添加系统分隔符
    
    #设置新文件名
    newname='./dataset/PM_new/ASCII/' + os.sep +'asc_'+fileList[n]
    
    os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
    print(oldname,'======>',newname)
    
    n+=1

    
#%%
#找對應術語
dc_df= pd.read_csv('pair_t2s.csv',encoding='ANSI')#doctor
dc_word = dc_df['pair_s'].tolist()

print(len(dc_word))

df= pd.read_csv('temp_reD.csv',encoding='ANSI')
word = df['s'].tolist()

print(len(word))

lst_id=[]
for key in dc_word:
    print(key)
    cnt=0
    for i in range(len(word)):
        if key in word[i]:
            cnt+=1
            #Cholesterol -> Cholesterol 與 HDL Cholesterol
            #Pain-> Abdominal Pain 與 Chest Pain 與 Pain 與 Back Pain
            #自行修改
            if cnt>1 :
                lst_id.append(i)
                print(key,"||",i,word[i])
            
print(len(lst_id))

print()
df_t = df.iloc[lst_id]
print(df_t)
#df_t = df_t[['word_d_wiki','word_d_drugs','word_d_pubmed']]
#df_t = df_t[['word_t_wiki','word_t_drugs','word_t']]
df_t = df_t[['word_s_wiki','word_s_drugs','word_s_pubmed']]
print(df_t)
df_t = df_t.assign(doctor_s = dc_word)#增加在原本後面
print(df_t)
df_t.to_csv('./pair_s.csv',index=0)

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    