# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:41:18 2022

正規表達
https://yanwei-liu.medium.com/python%E6%AD%A3%E8%A6%8F%E8%A1%A8%E9%81%94%E5%BC%8F-fbffb92972dc

txt
https://ithelp.ithome.com.tw/articles/10202725
https://oxygentw.net/blog/computer/python-file-utf8-encoding/

UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa1 in position 13240: invalid start byte
https://blog.csdn.net/angela_0612/article/details/80405179

NaN
https://www.796t.com/post/NDFvNg==.html

LookupError
https://stackoverflow.com/questions/4867197/failed-loading-english-pickle-with-nltk-data-load

@author: YC
"""

import pandas as pd
import re
from nltk.tokenize import sent_tokenize
#---------------------------------
# wiki簡單(前)前處理
# 將wiki文章貼到wiki_pre.txt處理後
# 使用wiki_preNew.txt貼到CSV
#---------------------------------
def initialWiki():
    with open('wiki_pre.txt', 'r',encoding="utf-8") as f:
        data = f.read()
        #print(type(data))
        data = data.replace("<"," ")
        data = data.replace(">"," ")
        data = data.replace("≤"," ")
        data = data.replace("≥"," ")
        data = data.replace("%"," ")
        data = data.replace("°C"," ")
        data = data.replace("°F"," ")
        data = data.replace("°"," ")
        data = re.sub('\[[a-zA-Z0-9\ |a-zA-Z0-9\-]+\]', '', data)#去除[數字][medical][medical citation needed]或[non-primary source]
        data = re.sub('\:.[0-9]+', '', data)
        data = re.sub('[\ ]{2,}', ' ', data)
        data = data.replace("( ","(")
        data = data.replace(" )",")")
    print(data)
    f.close()
    
    with open('wiki_preNew.txt', 'w',encoding="utf-8") as f:
        f.write(data)
    f.close()



#---------------------------------
# 在總表100.xlsx中
# 1.' – '取代成' '
# 2.'–'取代成'-'
# 找'數-數'
#---------------------------------
def findAllHyphen(col):
    
    df = pd.read_csv('temp_reD.csv',encoding="gb18030")
    df_result_S=[]
    df_result_H=[]
    for c in col:
        drugs = df[c].tolist()#一col
        for i in range(len(drugs)):#一col中的一筆
            HyphenRegex = re.compile(r'\ [0-9.]+\-[0-9.]+\ |\([0-9.]+\-[0-9.]+\)')
            result_H = HyphenRegex.findall(str(drugs[i]))
            #print(result)
            #Slash = '\n'.join(result)
            #print('Phone Number: \n' + Slash)
            
            SlashRegex = re.compile(r'\ [a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\ |\([a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\)')
            result_S = SlashRegex.findall(str(drugs[i]))
            
            df_result_H = df_result_H + result_H
            df_result_S = df_result_S + result_S
        
    #print(len(df_result))
        #print(df_result)
    df_result_H_Deduplication = set(df_result_H)#去重複
    lst_hyphen = list(df_result_H_Deduplication)
    lst_hyphen = sorted(lst_hyphen, reverse=True)
    
    df_result_S_Deduplication = set(df_result_S)#去重複
    lst_slash = list(df_result_S_Deduplication)
    lst_slash = sorted(lst_slash, reverse=True)#括號放前先刪 (mg/dL), mg/dL
    
    print(lst_slash)
    print(lst_hyphen)

    
    with open('wiki_slash.txt', 'w') as f: # w → 複寫 r → 讀取 a → 增寫
        for i in lst_slash:    
            f.write(i+"\n")
    f.close()
    with open('wiki_hyphen.txt', 'w') as f: # w → 複寫 r → 讀取 a → 增寫
        for i in lst_hyphen:    
            f.write(i+"\n")
    f.close()

# !!刪掉不想刪的!!


def preprocWiki(col):
    df = pd.read_csv('temp_reD.csv',encoding="gb18030")#沒轉乾淨再轉一次
    
    dict = {}
    
    for c in col:
        wiki = df[c].tolist()
        
        df_new_test=[]
        for i in range(len(wiki)):
            String1 = str(wiki[i]).replace('404','')
            
            

            f = open('wiki_hyphen.txt', 'r')
            for line in f.readlines():
                tmp = line.strip().replace("-"," to ")
                String1 = String1.replace(line.strip(),tmp) 
            f.close
            print(String1)

            f = open('wiki_slash.txt', 'r')
            for line in f.readlines():
                String1 = String1.replace(line.strip()," ")  
            f.close
            print(String1)
            String1 = String1.replace('/',' ')

 
            
            String1 = String1.replace('NO Diagnosis','')
            String1 = String1.replace('i.e.','in other words,')
            String1 = String1.replace('e.g.','for example')
            String1 = String1.replace("?","")#轉不了會變成問號
            String1 = String1.replace('"','')#("hole")
            String1 = String1.replace(':',' ')
            String1 = String1.replace(';',' ')
            String1 = String1.replace('%','')
            String1 = String1.replace('$','')
            String1 = String1.replace('~','')
            String1 = String1.replace('percent','')
            String1 = String1.replace('Percent','')
            String1 = String1.replace('(s) ','')
            String1 = String1.replace("'s",'')
            
            
            #沒句號的地方加句號
            PeriodRegex = re.compile(r'[A-Za-z0-9]+\n')#匹配換行前沒句點
            result_P = PeriodRegex.findall(String1)
            #print(result_P)
            for line in result_P:
                tmp = line.replace("\n",".\n")
                print(tmp)
                print(line)
                String1 = String1.replace(line,tmp) 
            #print(String1)
            
            String1 = String1.replace('\n',' ')
            String1 = re.sub('[\ ]{2,}', ' ', String1)#保留一個空格
            
            df_new_test.append(String1)
        
        #dict[c+'_old'] = drugs
        dict[c+'_new'] = df_new_test
        #dict[c] = df_new_test
    
    df = pd.DataFrame(dict) 
    #df.to_csv('./new_test_drugs.csv',index=0)#index=0 沒有第一col的id
    df.to_csv('./new_wiki.csv',index=0)  


def SentSegmentation():
    k = 'The World Health Organization definition of diabetes (both type 1 and type 2) is for a single raised glucose reading with symptoms, otherwise raised values on two occasions, of either fasting plasma glucose or equal to 7.0 (126 ) or. with a glucose tolerance test, two hours after the oral dose a plasma glucose or equal to 11.1 (200 ) A random blood sugar of 11.1 (200 ) in association with typical symptoms or a glycated hemoglobin (HbA1c) of or equal to 48 (greater than or equal to 6.5 DCCT ) is another method of diagnosing diabetes. In 2009 an International Expert Committee that included representatives of the American Diabetes Association (ADA), the International Diabetes Federation (IDF), and the European Association for the Study of Diabetes (EASD) recommended that a threshold of or equal to 48 (greater than or equal to 6.5 DCCT ) should be used to diagnose diabetes. This recommendation was adopted by the American Diabetes Association in 2010. Positive tests should be repeated unless the person presents with typical symptoms and blood sugars 11.1 (greater than 200 ). Threshold for diagnosis of diabetes is based on the relationship between results of glucose tolerance tests, fasting glucose or HbA1c and complications such as retinal problems.'
    # breaking text into sentences
    
    text_sentences = sent_tokenize(k)
    print(text_sentences)

    for i, sent in enumerate(text_sentences):
        print("Sentence {}: {}".format(i + 1, sent), end = "\n\n")
        
        
# ================= Main =================

col = ['DT','ab','DS']
#findAllHyphen(col)
preprocWiki(col)




    
    