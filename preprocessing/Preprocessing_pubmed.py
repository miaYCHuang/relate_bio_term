# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 15:51:16 2022

@author: YC
"""

import re
import pandas as pd
import numpy as np
import os

import string
'''
def is_rare_name(string):
    pattern = re.compile(u"[~!@#$%^&* ]") #生僻字和非法字符
    match = pattern.search(string)
    if match:
        try:
            string.encode("gb2312")
            return True
        except UnicodeEncodeError:
        	return False
        
    else:
        return False




df = pd.read_csv('D:/anaconda_code/PubMed_data/A41.csv')
abstract = df['abstract'].tolist()
for i in range(len(abstract)):
    #abstract[i].encode("gb2312")
    print(is_rare_name(abstract[i]))
    '''

# cop = re.compile("[^a-z^A-Z^0-9^\ ]") # 匹配不是英文、大小写、数字的其他字符
# string1 = cop.sub('', abstract[i]) #将string1中匹配到的字符替换成空字符
# df_new_test.append(string1)
 


#前處理
def preprocPM(csv_name):
    # / - , . () 沒刪
    try:
        df = pd.read_csv('./dataset/PM_updata/new/ASCII/'+csv_name+'.csv')
        abstract = df['new_abstract'].tolist()
    
    
        df_new_test=[]
        for i in range(len(abstract)):
            String1 = abstract[i]
            
            if String1 == '[Figure: see text].' : String1=""            
            elif '[This corrects the article DOI:' in String1: String1=""        
            else:
       
                Delete1Regex = re.compile(r'[?]{3,}')#三格問號以上
                dlt = re.match(Delete1Regex, String1)
                if dlt != None:
                    String1=""
                    #print('dlt?',String1)
    
                String1 = re.sub('\[\<xref[\w\.\-\=\"\,\<\>\ \/]+\<\/xref\>\]', '', String1)# [<xref ref-type="bibr" rid="ref6">6</xref>]
                String1 = re.sub('\(Fig\.[\w\.\-\=\"\,\<\>\ \/]+\)', '', String1)#(Fig. XXXX)
                String1 = re.sub('\[[a-zA-Z0-9\ |a-zA-Z0-9\-]+\]', '', String1)#去除[數字][medical][medical citation needed]或[non-primary source]
                #abstract[i] = re.sub('&lt;', '', abstract[i])
                
                #轉換HTML字元
                String1 = String1.replace("&amp;","&")
                String1 = String1.replace("&quot;","\"")
                String1 = String1.replace("&apos;","'")
                String1 = String1.replace("&gt;",">")
                String1 = String1.replace("&lt;","<")
                #刪除<tag>
                String1 = re.sub('\<[a-zA-Z0-9]+\>', '', String1)#去除<英數>
                String1 = re.sub('\<\/[a-zA-Z0-9]+\>', '', String1)#去除</英數>
               
                #String1 = re.sub('\ [0-9]+\ ', '', String1)
                
                String1 = String1.replace("%"," ")
                String1 = String1.replace('percent',' ')
                String1 = String1.replace('Percent',' ')
                String1 = String1.replace(':','')
                String1 = String1.replace(';','')
                String1 = String1.replace('"','')
                String1 = String1.replace('$','')
                String1 = String1.replace("?","")
                String1 = String1.replace("<"," ")
                String1 = String1.replace(">"," ")
                String1 = String1.replace("≤"," ")
                String1 = String1.replace("≥"," ")
                String1 = String1.replace("°C"," ")
                String1 = String1.replace("°F"," ")
                String1 = String1.replace("°"," ")
                String1 = String1.replace('(s) ',' ')
                String1 = String1.replace("'s",'')
                String1 = String1.replace('\n',' ')
                String1 = String1.replace('[','')
                String1 = String1.replace(']','')
                #String1 = String1.replace(',',' ')
                #String1 = String1.replace('.',' ')
    
                String1 = re.sub('[\ ]{2,}', ' ', String1)
            df_new_test.append(String1)
    
        dict = {'abstract': df_new_test, 'title': df['title'].tolist()}
        df3 = pd.DataFrame(dict)
        #print(df3)
        df3.drop(df3.index[(df3["abstract"] == '' )],axis= 0 ,inplace= True)
        #print(df3)
        df3.to_csv('./dataset/PM_updata/new/preproc/'+csv_name+'.csv',index=0)#index=0 沒有第一col的id
    except Exception as e:
        print(csv_name +"檔案錯誤")
        print(e)



def get5K(csv_name):
    #隨機抽5千筆

    try:
        df = pd.read_csv('./dataset/PM_updata/new/preproc/'+csv_name+'.csv')
        #abstract = df['abstract'].tolist()
        #df = pd.read_csv('./result/I212.csv',encoding = 'gb18030')
        #print(df.shape[0],df.shape[1])
        if(df.shape[0]>5000):
            r=np.random.randint(0,df.shape[0],5000)
            new_df = df.loc[r]
            #print(new_df)
            new_df = new_df.filter(items=['title', 'abstract'])
            new_df.to_csv('./dataset/PM_updata/new/5K/'+csv_name+'.csv',index=False)
        else:
            print(csv_name,"小於5K筆")
            #print("小於一萬筆")
    except Exception as e:
        print(csv_name+"檔案錯誤")
            
            
            
           
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
# 單筆資料的特殊字元
# 去重複
# call is_encomm_char
#---------------------------------
def notASCII(csv_name):

    #df = pd.read_csv('D:/anaconda_code/PubMed_data/'+csv_name+'.csv',encoding= 'unicode_escape')#,encoding="gb18030"
    df = pd.read_csv('./dataset/PM_updata/new/5K/update5K/'+csv_name+'.csv') #error的使用
    abstract = df['abstract'].tolist()

    
    notASCII = []
    for i in range(len(abstract)):
        if is_encomm_char(abstract[i]) != []:
            #print(i,is_encomm_char(abstract[i]))
            for c in is_encomm_char(abstract[i]):
                notASCII.append(c)
            
            #print(i)
    
    notASCII_Deduplication = set(notASCII)#去重複
    lst_notASCII = list(notASCII_Deduplication)
    print(lst_notASCII)
    return lst_notASCII






#---------------------------------
# 處理ASCII外的字元 亂碼
# call notASCII
#---------------------------------
def preAS(csv_name):
    try:
        df = pd.read_csv('./dataset/PM_updata/new/5K/update5K/'+csv_name+'.csv')#error的使用
        #df = pd.read_csv('D:/anaconda_code/PubMed_data/'+csv_name+'.csv',encoding= 'unicode_escape')#,encoding="gb18030"
        abstract = df['abstract'].tolist()
        #print(len(abstract))
        lst_notASCII = notASCII(csv_name)
        #print(lst_notASCII)
        lst_old=[]
        lst_new=[]
        for i in range(len(abstract)):
            String1 = abstract[i]
            lst_old.append(abstract[i])
            
            #取代不常見的字 'Â', '±','Î', '²'...
            for ch in lst_notASCII:
                String1 = String1.replace(ch,'')
                #print(notASCII(csv_name))
            
            lst_new.append(String1)
        #print(df)
        dict = {'asc_data': lst_new}
        #df = df.assign(new_abstract = lst_new)#增加在原本後面
        #print(df)
        df = pd.DataFrame(dict)
        df.to_csv('./dataset/PM_updata/new/5K/ASCII/asc_'+csv_name+'.csv',index=0)#index=0 沒有第一col的id
    except Exception as e:
        print(e)
 

#===================================================
# 檢查檔案是否存在
#===================================================
def checkfile():
    df = pd.read_csv('100.csv')    
    ICD_code = df['ICD10'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype

    lst_error=[]
    cnt=0
    for i in range(len(ICD_code)):
        filepath = 'D:/anaconda_code/ASCII/'+ICD_code[i]+'.csv'
        if os.path.isfile(filepath):
            cnt+=0
        else:
            cnt+=1
            lst_error.append(ICD_code[i])
            print(ICD_code[i])
    print(cnt)
    
    
    dict = {'ICD10': lst_error}
    df = pd.DataFrame(dict) 
    df.to_csv('error_icd.csv',index=0) #index=0 沒有第一col的id








#===========================MAIN============================

df1 = pd.read_csv('ICD_upd.csv')
# df1 = pd.read_csv('100.csv',encoding= 'unicode_escape')
ICD10 = df1['ICD10'].tolist()
for i in range(len(ICD10)):
    #get5K(ICD10[i].strip())
    #print(ICD10[i])
    preAS(ICD10[i].strip())
    #preprocPM(ICD10[i].strip())
    
 

#checkfile()



'''
#%%
#確定疾病是否存在於文本中

df1 = pd.read_csv('ICD_upd.csv')
ICD10 = df1['ICD10'].tolist()
stri = df1['String'].tolist()#疾病名
#print(len(ICD10))
#print(len(stri))
for i in range(len(ICD10)):
    df = pd.read_csv('./dataset/PM_updata/new/5K/'+ICD10[i]+'.csv')
    abstract = df['abstract'].tolist()
    cnt=0
    for j in range(len(abstract)):
        if stri[i].lower() in abstract[j].lower():
            cnt+=1
            #print(ICD10[i],stri[i]," in ",j)
            break
    if cnt==0:
        print(ICD10[i],stri[i]+"不存在於文本")

'''
