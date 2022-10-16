# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 13:21:20 2021

@author: user
"""

import pandas as pd
import wikipedia




def wikiWeb():
    #df = pd.read_csv('ICD3noData.csv')
    df = pd.read_csv('temp_reD.csv')#暫存資料
    #df = pd.read_csv('ICD4.csv')
    #print(df)#查看CSV資料
    
    ICD = df['ICD10 string'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
    print(len(ICD))
    ICD_wikiData=[]
    ICD_wikiName= []
    for i in ICD:
        if isinstance(i, str):#字串
            #print(type(i))
            
            #if i.find("and") != -1:#-1=no","
            #    cnt+=1
            #    print(i)
            
            #print(i)
            #search=wikipedia.search(i , results=5)
            #print(search)
            try:
                wiki = wikipedia.page(i)
                page = wiki.content#全文
                title = wiki.title
                
                D=page.find("== Signs and symptoms ==") 
                #D=page.find("== Diagnosis ==")
                if D != -1:#有Diagnosis
                    DtoEnd=page[D:]#保留== Diagnosis ==以下文章
                    #找到第三個==  也就是== Diagnosis ==的下一個==
                    find1=DtoEnd.find("==")
                    #print(find1)
                    find2=DtoEnd.find("==",find1+1)
                    #print(find2)
                    find3=DtoEnd.find("==",find2+1)
                    #print(find3)
                    
                    Diagnosis=DtoEnd[:find3]#只保留== Diagnosis == 的內容
                    #print(Diagnosis)
                    ICD_wikiData.append(Diagnosis)
                    if title.lower()!=i.lower():
                        ICD_wikiName.append(title)#名字不同
                    else:
                        ICD_wikiName.append("same")#名字相同
                else:#沒有Diagnosis
                        ICD_wikiData.append("NO Diagnosis")
                        ICD_wikiName.append("no")
            except Exception as e:
                ICD_wikiData.append("404")
                ICD_wikiName.append("404")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
        else:#NaN
            ICD_wikiData.append("")
            ICD_wikiName.append("")
    
    print(len(ICD_wikiData))
    print(len(ICD_wikiName))
    print(ICD_wikiName)
    ICD_WD=[]
    for row in ICD_wikiData:
            ICD_WD.append(row.replace("==", "_")) #=在csv會變成公式        
    #print(ICD_WD)
    
    
    '''
    Phe = df['phenotype'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
    Phe_wikiName= []
    Phe_wikiData=[]
    for i in Phe:
        if isinstance(i, str):#字串
            #print(i)
            #search=wikipedia.search(i , results=5)
            #print(search)
            try:
                wiki = wikipedia.page(i)
                page = wiki.content#全文
                title = wiki.title
                #D=page.find("== Signs and symptoms ==")
                D=page.find("== Diagnosis ==")
                if D != -1:#有Diagnosis
                    DtoEnd=page[D:]#保留== Diagnosis ==以下文章
                    #找到第三個==  也就是== Diagnosis ==的下一個==
                    find1=DtoEnd.find("==")
                    #print(find1)
                    find2=DtoEnd.find("==",find1+1)
                    #print(find2)
                    find3=DtoEnd.find("==",find2+1)
                    #print(find3)
                    
                    Diagnosis=DtoEnd[:find3]#只保留== Diagnosis == 的內容
                    #print(Diagnosis)
                    Phe_wikiData.append(Diagnosis)
                    if title.lower()!=i.lower():
                        Phe_wikiName.append(title)
                    else:
                        Phe_wikiName.append("same")
                else:#沒有Diagnosis
                        Phe_wikiData.append("NO Diagnosis")
                        Phe_wikiName.append("no")
            except Exception as e:
                #print(i)
                Phe_wikiData.append("404")
                Phe_wikiName.append("404")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
        else:#NaN
            Phe_wikiData.append("")
            Phe_wikiName.append("")
    
    print(len(Phe_wikiName))
    Phe_WD=[]
    for row in Phe_wikiData:
            Phe_WD.append(row.replace("==", "_")) #=在csv會變成公式        
    #print(list_Phe)
    '''
    dict = {'ICD_wiki': ICD_WD , 'ICD_wikiName':ICD_wikiName} 
    #dict = {'pheD_wiki':Phe_WD, 'Phe_wikiName':Phe_wikiName} 
    #dict = {'ICD_wiki': ICD_WD , 'ICD_wikiName':ICD_wikiName, 'pheD_wiki':Phe_WD, 'Phe_wikiName':Phe_wikiName} 
    df = pd.DataFrame(dict) 
    df.to_csv('./Output/output_wikiWeb.csv',index=0)#index=0 沒有第一col的id

def wikiAPI():
    df = pd.read_csv('temp_reD.csv')#空格先取代0
    print(df)
    key = df['key'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
    lst_summary=[]
    for i in key:        
        if i != '0':        
            try:
                #注意非英文字母會有亂碼!  自己刪除或是轉換編碼
                wiki = wikipedia.page(i)
                summary = wiki.summary
                lst_summary.append(summary)
                print(summary)
                
            except Exception as e:
                #手動+wiki_preprocessing
                lst_summary.append("errr")
                error_class = e.__class__.__name__
                print(error_class,":",e)
        else:
            lst_summary.append("")
            
    dict = {'summary': lst_summary}
    df = pd.DataFrame(dict) 
    df.to_csv('./Output/output_wikisum.csv',index=0)#index=0 沒有第一col的id
wikiAPI()

