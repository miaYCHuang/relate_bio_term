
from typing import List
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import unicodedata



#===================================================
# PubMed資料前處理
# (2)PubMed網站的資料
# 以PMID 爬 摘要
# 'Publication Year'與'create date'取2017-2021內
#===================================================
def getAbstract(ICD):
    for i in range(len(ICD)):
        df = pd.read_csv('C:/Users/YC/Downloads/'+ICD[i]+'.csv')
    
        
        print(df)
        df_PM1 = df.filter(items=['PMID','Title', 'Create Date','Publication Year'])#保留col
        print(df_PM1.shape)
        #df_PM1.drop(df_PM1.index[(df_PM1[ "Create Date" ] == "?" )],axis= 0 ,inplace= True )#date中有?的值刪除整row
        year_lim = set(df_PM1['Publication Year'])
        year_lim.discard(2017)
        year_lim.discard(2018)
        year_lim.discard(2019)
        year_lim.discard(2020)
        year_lim.discard(2021)
        print(year_lim)
    
        for pub_y in year_lim:
            df_PM1.drop(df_PM1.index[(df_PM1[ "Publication Year" ] == pub_y )],axis= 0 ,inplace= True)
        print(df_PM1)
        print(df_PM1.shape)
    
        df_PM_Nnan = df_PM1.dropna(axis=0, how='any')#刪除所有空值 因其不改變原始df所以給定新變數
        print(df_PM_Nnan)
        print(df_PM_Nnan.shape)
    
        #cnt=0
        for date in df_PM_Nnan['Create Date']:
            year = date.split('/')
            #print(year)
            if int(year[0])<2017 or int(year[0])>2021:#時間範圍外的刪除
                #cnt=cnt+1
                #print('Out',year[0])
                df_PM_Nnan.drop(df_PM_Nnan.index[(df_PM_Nnan[ "Create Date" ] == date )],axis= 0 ,inplace= True)
    
        print(df_PM_Nnan)
        print(df_PM_Nnan.shape)
        #df_PM_Nnan = df_PM1.dropna(axis=0, how='any')#刪除所有空值 因其不改變原始df所以給定新變數
    
    
    
    
        abstract = []
        for id in df_PM_Nnan['PMID']:
            print(id)
            r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+str(id)) #將網頁資料GET下來
            soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
            
            if soup.find("div", class_="abstract-content selected") == None:
                abstract.append('NO')
            else:
                
    
                pub_abs = soup.find_all("div", class_="abstract-content selected")
                
                
                st=""
                for p_tag in pub_abs:
                    
                    abs = p_tag.find_all('p')
                
                    #print(type(abs))
                    for n in abs:#每頁格式不同有1~多<p>
                        #print(type(n))
                        st = st + n.text.strip()
                    
                    st = st.replace('\n',"")
                    st = re.sub('[\ ]{2,}', ' ', st)#去除多個空白
                    print(st)
                    abstract.append(st)
    
        print(len(abstract))
    
        df_abs = df_PM_Nnan.assign(Abstract = abstract)#新增一col
        print(df_abs)
        print(df_abs.shape)
    
        df_abs.drop(df_abs.index[(df_abs[ "Abstract" ] == "NO" )],axis= 0 ,inplace= True )
        print(df_abs)
        print(df_abs.shape)
    
        #df_abs.to_csv("./result/output.csv")
        df_abs.to_csv('./result/'+ICD[i]+'.csv')
        
        
        
        
#===================================================
# 以PMID爬下的摘要會有亂碼
# 因此轉乘ascii
#https://www.796t.com/post/N2puNXE=.html
#===================================================

def Transcoding(ICD):
    for i in range(len(ICD)):
        df = pd.read_csv('./result/'+ICD[i]+'.csv',encoding= 'unicode_escape')
        print(df)
        abstract = df['Abstract'].tolist()
        title = df['Title'].tolist()
        print(len(abstract))
        print(len(title))
        
        new_abs=[]
        new_ti=[]
        for j in range(df.shape[0]):
            new_abs.append(unicodedata.normalize('NFKD', str(abstract[j])).encode('ascii','ignore'))
            new_ti.append(unicodedata.normalize('NFKD', str(title[j])).encode('ascii','ignore'))            
        dict = {'title':new_ti ,'abstract': new_abs,'date':df['Create Date'] } #'Create Date'格式與Orange 'date'同
        df1 = pd.DataFrame(dict)
        df1.to_csv('./result/'+ICD[i]+'2.csv',index=False)
        
        
        
        #處理格式b'.......'
        df = pd.read_csv('./result/'+ICD[i]+'2.csv',encoding='ascii')
        new_abs_pre = []
        new_ti_pre = []
        for k in range(df.shape[0]):
            new_abs_pre.append(df['abstract'][k][2:-1])
            new_ti_pre.append(df['title'][k][2:-1])
        dict = {'title':new_ti_pre ,'abstract': new_abs_pre,'date':df['date'] } 
        df1 = pd.DataFrame(dict)        
        df1.to_csv('./result/'+ICD[i]+'2.csv',index=False)



#-------------------------Main--------------------------
# df = pd.read_csv('C:/Users/YC/Desktop/17yTo21y/tt/t.csv')
ICD = ['N10','K35','I21']
getAbstract(ICD)
Transcoding(ICD)



