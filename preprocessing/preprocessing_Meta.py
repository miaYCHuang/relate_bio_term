# -*- coding: utf-8 -*-
"""
Created on Wed May 25 17:31:31 2022

@author: YC
"""
#分四個資料夾在colab多開幾個分頁跑比較快
#篩選後再合併不然資料太大會跑很久
#篩選症狀
import pandas as pd
import os
def filterData(csv_name,dirs):
    df = pd.read_csv('./Meta/frequency/frq_PM_category/'+dirs+'/'+csv_name)
    #print(len(df))
    '''
    filter1= df["semtypes"] == "cgab"
    filter2= df["semtypes"] == "fndg"
    filter3= df["semtypes"] == "inpo"
    filter4= df["semtypes"] == "menp"
    filter5= df["semtypes"] == "mobd"
    filter6= df["semtypes"] == "neop"
    filter7= df["semtypes"] == "patf"
    filter8= df["semtypes"] == "phsf"
    filter9= df["semtypes"] == "sosy"
    '''
    filter1= df["semtypes"] == "topp"
    filter2= df["semtypes"] == "inch"
    filter3= df["semtypes"] == "phsu"
    filter4= df["semtypes"] == "bacs"
    filter5= df["semtypes"] == "elii"
    filter6= df["semtypes"] == "spco"
    filter7= df["semtypes"] == "orch"
    filter8= df["semtypes"] == "ortf"
    filter9= df["semtypes"] == "aapp"
    filter10= df["semtypes"] == "enzy"
    filter11= df["semtypes"] == "euka"
    filter12= df["semtypes"] == "imft"
    filter13= df["semtypes"] == "medd"
    filter14= df["semtypes"] == "horm"
    filter15= df["semtypes"] == "lbpr"
    filter16= df["semtypes"] == "lbtr"
    filter17= df["semtypes"] == "diap"

    
    filterAll = df[ filter1 | filter2 | filter3 | filter4 | filter5 | filter6 | filter7 | filter8 | filter9 | filter10 | filter11 | filter12 | filter13 | filter14 | filter15 | filter16 | filter17]
    #print(filterAll)
    #print(len(filterAll))
    #print(type(filterAll))
    
    filterAll.to_csv('./Meta/frequency/frq_PM_category/'+dirs+'/filter/'+csv_name,index=0)

def getDirData(dirs_cate):
    allList = os.walk('./Meta/frequency/frq_PM_category/'+dirs_cate)
    for root, dirs, files in allList:
        return files
    #print(len(files),type(files))    


list_dir=['1','2','3','4']



for dirs_cate in list_dir: 
    
    files = getDirData(dirs_cate)
    print(files)
    
    for i in range(len(files)):   
        filterData(files[i],dirs_cate)

#%%
#取得資料夾下所有資料名稱
import os
allList = os.walk('./Meta/frequency/frq_PM_category/1/filter_test')

# 列出所有子目錄與子目錄底下所有的檔案

for root, dirs, files in allList:

#   列出目前讀取到的路徑

  print("path：", root)

#   列出在這個路徑下讀取到的資料夾(第一層讀完才會讀第二層)

  print("directory：", dirs)

#   列出在這個路徑下讀取到的所有檔案

  print("file：", files)
#%%
'''
import pandas as pd

def com2data(csv1,csv2):
    #df1 = pd.read_csv('./Meta/'+csv1)
    df1 = pd.read_csv('./Meta/frequency/frq_PM_category/2/filter/'+csv1)
 
    #df2 = pd.read_csv('./Meta/'+csv2)
    df2 = pd.read_csv('./Meta/frequency/frq_PM_category/2/filter/'+csv2)

    
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
    #print(df_1_dp)
    #print(df_2_dp)
    #print(com)
    df_com = pd.DataFrame(com, columns = ['preferred','semtypes','cui','count'])
    #print(df_com)
    #合併1+2+重複
    all_csv = pd.concat([df_1_dp,df_2_dp,df_com])
    print(all_csv)
    
    all_csv.to_csv('./Meta/frequency/frq_PM_category/2/filter/metaCom_pubmed.csv',index=0)

#wiki,drugs
#com2data('metaCom.csv','metaCom_wiki.csv')
#com2data('metaCom.csv','Meta_drugs_DS.csv')#'Meta_wiki_DT.csv','Meta_wiki_ab.csv'
#com2data('metaCom_drugs.csv','Meta_drugs_133.csv')#'Meta_drugs_DT.csv','Meta_drugs_DT.csv'   'metaCom.csv','Meta_drugs_ab.csv'

#pubmed
#df1= pd.read_csv('100.csv')
#ICD10 = df1['ICD10'].tolist()
for i in range(len(files)):
    if i == 0 :
        print(files[i],files[i+1])
        com2data(files[i],files[i+1])
    elif i > 1:
        print(files[i],'metaCom_pubmed.csv')
        com2data(files[i],'metaCom_pubmed.csv')
   print("file：", files)
   
'''
#合併兩csv資料 (metamap計算頻率的檔)
#重複合併 更新count(加總)
#上面算法太慢 6M30S
#此為更新版 29S
#快13倍  不然資料太大要等好幾天
#http://violin-tao.blogspot.com/2017/06/pandas-2-concat-merge.html

from numpy import empty
import pandas as pd

def com2data(csv1,csv2):
  df1 = pd.read_csv('./Meta/frequency/frq_PM_category/1/filter_test/'+csv1)
  df2 = pd.read_csv('./Meta/frequency/frq_PM_category/1/filter_test/'+csv2)

  for i in range(df1.shape[0]):
    
    match = df2.loc[ (df2['preferred'] == df1['preferred'][i]) & (df2['semtypes'] == df1['semtypes'][i]) & (df2['cui'] == df1['cui'][i]) ]
    if match.empty != True:#不為空=有匹配到
      
      count1 = int(df1['count'][i])

      for idx in match.index:
        print('1:',i,'2:',idx)
        count1 = count1 + int(df2['count'][idx])#合併計數至df1
        df2 = df2.drop([idx])#df2刪除該筆重複資料

      #data.loc[0:2,['Num','NAME']] = [100,'Python']
      df1.loc[i,['count']] = [count1]#更新df1計數

  df_new = pd.concat([df1,df2],axis=0, ignore_index=True)#合併更新完的1+去重複的2 #axis=0為直向合併 ignore_index=True為忽略原始index 
  df_new.to_csv('./Meta/frequency/frq_PM_category/1/filter_test/metaCom_pubmed.csv',index=0)
  #files.download('1.csv')


for i in range(len(files)):
    if i == 0 :
        print(files[i],files[i+1])
        com2data(files[i],files[i+1])
    elif i > 1:
        print(files[i],'metaCom_pubmed.csv')
        com2data(files[i],'metaCom_pubmed.csv')
        
#com2data('1test.csv','2test.csv')#四資料夾合併完後 合併"合併後的"四個檔案 -> PM所有詞的出現頻率(metamap)
#有了三資料集的頻率後跑freqMerge.sas 
#%%
#以某變數排序後取前幾位

df = pd.read_csv('./Meta/frequency/test/frequency_all_test.csv')
print(df)
df1 = df.sort_values(['count_p'],ascending=False).head(200)
df1.to_csv('./Meta/frequency/test/frequency_all_p200.csv',index=0)
#df1 = df1.sort_values(['count_d'],ascending=False).tail(100)
#print(df1)
#df1.to_csv('./Meta/frequency/frequency_all_d200.csv',index=0)#100-200

#================================
# 症狀從W D P (各個前百中)各挑17/17/16 =50個
# 檢驗從W D P (各個前百中)各挑3/3/3 補齊50個
#================================
#%%
#取出兩檔案都有的項目

def com2data(csv1,csv2):
    df1 = pd.read_csv('./Meta/frequency/'+csv1)
    df2 = pd.read_csv('./Meta/frequency/'+csv2)
    
    lst_match=[]
    for i in range(df1.shape[0]):
      
        match = df2.loc[ (df2['preferred'] == df1['preferred'][i]) & (df2['semtypes'] == df1['semtypes'][i]) & (df2['cui'] == df1['cui'][i]) ]
        if match.empty != True:#不為空=有匹配到
            lst_match.append(i)
    print(len(lst_match))
    df1.loc[lst_match].to_csv('./Meta/frequency/frequency_all_dpw400.csv',index=0)
    print(df1.loc[lst_match])




com2data('frequency_all_dp400.csv','frequency_all_w400.csv')


#%%
#取區間
#排序不同  不能直接從200取後100
#取100-200項目(把200中100的項目去掉)
def com2data(csv1,csv2):
    df1 = pd.read_csv('./Meta/frequency/'+csv1)
    df2 = pd.read_csv('./Meta/frequency/'+csv2)

    lst_match=[]
    for i in range(df1.shape[0]):
      
        match = df2.loc[ (df2['preferred'] == df1['preferred'][i]) & (df2['semtypes'] == df1['semtypes'][i]) & (df2['cui'] == df1['cui'][i]) ]
        if match.empty != True:#不為空=有匹配到
            df1 = df1.drop([i])  
    print(len(df1))
    df1.to_csv('./Meta/frequency/frequency_all_dpw300to400.csv',index=0)
#200放前  100放後
com2data('frequency_all_dpw300to400.csv','frequency_all_dpw200to300.csv')

#%%
#CUI合併檔案
#將所有疾病(100)的CUI全部放入一個檔  以作為後續資料集 47萬筆
import pickle
import pandas as pd

df1= pd.read_csv('100.csv')
ICD10 = df1['ICD10'].tolist()
total_CUI = []
with open('./Meta/CUI/cui_pubmed.txt', 'w+') as new_f:
    
    for i in range(len(ICD10)):
        
        f = open('./Meta/CUI/PM_CUI_UPDATE/cui_'+ICD10[i].strip()+'.txt')
        for line in f.readlines():
            if line.strip()!='':  #空格為meta出現錯誤情況
                lst_strings = line.strip().split(',')
                lst_strings.remove('')#去除空值
                
                string = " ".join(lst_strings)#以空格隔開因為bioWV以空格切分
                print(string)
                
                new_f.write(string+'\n')
                total_CUI.append(string)
     
        f.close
new_f.close()
    
print(len(total_CUI))

#%% 
total_CUI = []
with open('./Meta/CUI/drugs.txt', 'w+') as new_f:
    f = open('./Meta/CUI/cui_drugs.txt')
    for line in f.readlines():
        if line.strip()!='':  #空格為meta出現錯誤情況
            lst_strings = line.strip().split(',')
            lst_strings.remove('')#去除空值
            
            string = " ".join(lst_strings)#以空格隔開因為bioWV以空格切分
            print(string)
            
            new_f.write(string+'\n')
            total_CUI.append(string)
    f.close()
new_f.close()
print(len(total_CUI))








