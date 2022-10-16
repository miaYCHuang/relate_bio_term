# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:35:48 2022

@author: YC
"""

import pandas as pd

#---------------------------------
# 合併檔案 
# wiki,drugs 資料集中的 DiseaseTest(DT) abstract(ab) DiseaseSymptom(DS)
# pm 的每筆疾病
# 重複的筆數 count加總 其餘變數不變
# 合併經MetaMap匯出的檔案(包括CountMeta()、出現Resource error透過findOneMeta() || PM CountMeta()不含出現Resource error的項目)
#---------------------------------
def com2data(csv1,csv2):
    #df1 = pd.read_csv('./Meta/'+csv1)
    df1 = pd.read_csv('./Meta/pubmed/'+csv1)
 
    #df2 = pd.read_csv('./Meta/'+csv2)
    df2 = pd.read_csv('./Meta/pubmed/'+csv2)

    
    com=[]
    lst_drop_1 = []
    lst_drop_2 = []
    for i in range(df1.shape[0]):    
        for j in range(df2.shape[0]):
            if df1['preferred'][i] == df2['preferred'][j]:
                if df1['semtypes'][i] == df2['semtypes'][j]:
                    if df1['cui'][i] == df2['cui'][j]:                    
                        lst_drop_1.append(i)
                        lst_drop_2.append(j)
                        com.append([df1['preferred'][i],df1['semtypes'][i],df1['cui'][i],int(df1['count'][i])+int(df2['count'][j])])
                        
                       
                        
    
    #移除1 2重複項目
    df_1_dp = df1.drop(df1.index[lst_drop_1])
    df_2_dp = df2.drop(df2.index[lst_drop_2])
    
    df_com = pd.DataFrame(com, columns = ['preferred','semtypes','cui','count'])

    #合併1+2+重複
    all_csv = pd.concat([df_1_dp,df_2_dp,df_com])
    print(all_csv)
    
    all_csv.to_csv('./Meta/pubmed/metaCom_pubmed.csv',index=0)

#wiki,drugs
#com2data('metaCom.csv','metaCom_wiki.csv')
#com2data('metaCom.csv','Meta_drugs_DS.csv')#'Meta_wiki_DT.csv','Meta_wiki_ab.csv'
#com2data('metaCom_drugs.csv','Meta_drugs_133.csv')#'Meta_drugs_DT.csv','Meta_drugs_DT.csv'   'metaCom.csv','Meta_drugs_ab.csv'



# 合併檔案內資料
def combine3drugs(data):
    #df = pd.read_csv('new_test_drugs2.csv') #,encoding='cp1252'
    df = pd.read_csv('./dataset/wiki_DS.csv',encoding='cp1252')
    #df = pd.read_csv('./dataset/combineAllDrugs2.csv',encoding= 'unicode_escape') #,encoding='cp1252'
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
    df.to_csv('./dataset/wiki_DS.csv',index=0)
    #df.to_csv('./result/comineDrugs_DS.csv',index=0)#index=0 沒有第一col的id










#================================ MAin ===================================

#wiki合併摘要與症狀col 視為 疾病與症狀檔
combine3drugs(['ab_new','DS_new'])
   
'''    
#pubmed
df1= pd.read_csv('1.csv')
ICD10 = df1['ICD10'].tolist()
for i in range(len(ICD10)):
    if i == 0 :
        print(ICD10[i],ICD10[i+1])
        com2data(ICD10[i]+'.csv',ICD10[i+1]+'.csv')
    elif i > 1:
        print(ICD10[i],'metaCom_pubmed')
        com2data(ICD10[i]+'.csv','metaCom_pubmed.csv')
'''


#=========================================================================


