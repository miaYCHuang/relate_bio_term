# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:58:07 2022

@author: YC
"""

from itertools import count
from operator import le
from pymetamap import MetaMap
import csv
import pandas as pd
from collections import Counter

#MetaMAP Resource error 
#https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/OutOfMemory.pdf
#ConceptMMI(index='USER', mm='MMI', score='4.21', preferred_name="Alzheimer's Disease", cui='C0002395', semtypes='[dsyn]', trigger='["ALZHEIMER DISEASE"-tx-46-"Alzheimer disease"-noun-0]', location='TX', pos_info='6119/17', tree_codes='')
# 放list裡面run效果好像比較好
mm = MetaMap.get_instance('/home/martin-metamp/Desktop/Metamap/public_mm_linux_main_2020/public_mm/bin/metamap20')



#===================================================
# 計算文本映射出的CUI出現的頻率
#計數文本的各個MetaMap出現數量(不重複)
#MetaMAP Resource error 可先刪除該項目 再用findOneMeta計算後  合併檔案
#===================================================
def CountMeta(csv_name):

    df = pd.read_csv('./update5K/'+ csv_name +'.csv')
    #df = pd.read_csv('combineAllDrugs2.csv',encoding="gb18030")#,encoding="gb18030"
    #df = pd.read_csv(csv_name+'.csv')#,encoding="gb18030" new_wiki2
    #print(df)

    #data = df['asc_data'].tolist()
    data = df['abstract'].tolist()
    #data = df['DS_new'].tolist()


    lst_err=[]
    lst=[]
    c=0
    for row in data:
        c+=1
        print(csv_name ,'row=',c)
        if isinstance(row, str):#有值非空
            try:
                sent_tmp = []
                sent_tmp.append(row)
                #print("sent=",sent_tmp, end = "\n\n")
                str_cui = ''
                concepts,error = mm.extract_concepts(sent_tmp)
                #c+=1

                for concept in concepts:
                    
                    string = str(concept) #每一筆matamap     
                    #if c==3: print("C3=",string)
                    ConceptType = string[:string.index("(")]
                    #c+=1
                    if ConceptType=='ConceptMMI':
                        #preferred_name
                        preferred_t1 = string.index("name=")
                        preferred_t2 = string.index(", cui")
                        preferred = string[preferred_t1+6:preferred_t2-1]
                        
                        #semtypes
                        semtypes_t1 = string.index("'[")            
                        semtypes_t2 = string.index("]',")    
                        semtypes = string[semtypes_t1+2:semtypes_t2]
                        
                        #CUI
                        cui_t1 = string.index('cui')
                        cui_t2 = string.index(', semtypes')
                        cui = string[cui_t1:cui_t2]
                        cui = cui.replace("'","")
                        cui = cui.replace("cui=","")
                        if 'lbpr' in semtypes or 'lbtr' in semtypes or 'diap' in semtypes or 'dsyn' in semtypes or 'sosy' in semtypes or 'cgab' in semtypes or 'fndg' in semtypes or 'inpo' in semtypes or 'menp' in semtypes or 'mobd' in semtypes or 'neop' in semtypes or 'patf' in semtypes or 'phsf' in semtypes or 'topp' in semtypes or 'inch' in semtypes or 'phsu' in semtypes or 'bacs' in semtypes or 'elii' in semtypes or 'spco' in semtypes or 'orch' in semtypes or 'ortf' in semtypes or 'aapp' in semtypes or 'enzy' in semtypes or 'euka' in semtypes or 'imft' in semtypes or 'medd' in semtypes or 'horm' in semtypes :
                        #if 'lbpr' in semtypes or 'lbtr' in semtypes or 'diap' in semtypes or 'dsyn' in semtypes or 'sosy' in semtypes or 'cgab' in semtypes or 'fndg' in semtypes or 'inpo' in semtypes or 'menp' in semtypes or 'mobd' in semtypes or 'neop' in semtypes or 'patf' in semtypes or 'phsf' in semtypes or 'topp' in semtypes:
                            #print(preferred,semtypes,cui)
                            tmp=[preferred,semtypes,cui]
                            lst.append(tmp)
                            str_cui = str_cui+cui+','

                with open('./CUI/cui_'+csv_name+'.txt', 'a') as f:
                #with open('./CUI/cui_'+csv_name+'.txt', 'a') as f:
                    f.write(str_cui+'\n')
                f.close()
             
            except Exception as e:
                print(csv_name +"檔案錯誤")
                print(e)
                string_e = csv_name+','+str(c)
                lst_err.append(string_e)
        
    
    #print("c=",c)
    #print("lst len=",len(lst))
    #print(lst)
    
            
                        

    remove=[]
    count=[]

    #計算次數
    for i in range(len(lst)):
        cnt=1
        for j in range(len(lst)):        
            if lst[i] == lst[j]:
                if i != j :
                    cnt+=1
        count.append(cnt)

    #找重複
    for i in range(len(lst)):
        for j in range(len(lst)):
            #print(i,"  VS  ",j)
            #print(cnt)
            
            if lst[i] == lst[j]:
                if i != j : 
                    #print(i,"Equal",j)
                    remove.append(i)
                    lst[i]=[]#清空
                    #print(lst[i])

    cnt=0
    #去重複
    for nan in remove:
        count.pop(nan-cnt)
        lst.pop(nan-cnt)
        cnt+=1

    #將次數加入lst
    for i in range(len(lst)):
        lst[i].append(count[i])
        #print(lst[i])
        
    #轉DataFrame
    df = pd.DataFrame(lst, columns = ['preferred','semtypes','cui','count'])
    #print(df)

    #df.to_csv('frq_drugs.csv',index=0)
    #df.to_csv('./pubmed_tmp/'+csv_name+'.csv',index=0)
    df.to_csv('./update_feq/'+csv_name+'.csv',index=0)
    return lst_err






#===================================================
# 計算one string映射出的CUI
# 用於測試 or 跑錯誤項目
#===================================================
def findOneMeta():

    search_name=[]
    preferred_lst=[]
    semtypes_lst=[]
    cui_lst=[]
    Dic_abbreviation={}
    cnt=0
#measurement
    row="Cold"

    sents = []
    sents.append(row)
    print(sents)

    concepts,error = mm.extract_concepts(sents) #放list[str]  str好像跑不出來?
                
    lst=[]
    cnt=0
    for concept in concepts:#一筆CSV的多個matamap data
        
        #print (concept)
        string = str(concept) #每一筆matamap            
        ConceptType = string[:string.index("(")]#ConceptAA   ConceptMMI

        if ConceptType=='ConceptAA':#縮寫與全寫
            #short_form
            short_form_t1 = string.index("short_form=")            
            short_form_t2 = string.index(", long")    
            short_form = string[short_form_t1+12:short_form_t2-1]
            #print(short_form)

            #long_form
            long_form_t1 = string.index("long_form=")            
            long_form_t2 = string.index(", num_tokens_short_form")    
            long_form = string[long_form_t1+11:long_form_t2-1]
            #print(long_form)

            Dic_abbreviation[short_form]=long_form      

        elif ConceptType=='ConceptMMI':
            
            cnt+=1
            
            #semtypes
            #promblem -> preferred_name='Thyroid Stimulating Hormone [EPC]'
            semtypes_t1 = string.index("'[")            
            semtypes_t2 = string.index("]',")    
            semtypes = string[semtypes_t1+2:semtypes_t2]

            
            #preferred_name
            preferred_t1 = string.index("name=")
            preferred_t2 = string.index(", cui")
            preferred = string[preferred_t1+6:preferred_t2-1]
                        
            #CUI
            cui_t1 = string.index('cui')
            cui_t2 = string.index(', semtypes')
            cui = string[cui_t1:cui_t2]
            cui = cui.replace("'","")
            cui = cui.replace("cui=","")
        
            if cnt == 1: 
                search_name.append(row)
            else:
                search_name.append('')
            print(cnt)
            preferred_lst.append(preferred)
            cui_lst.append(cui)
            semtypes_lst.append(semtypes)
            print(preferred,semtypes,cui)
            '''
            if 'lbpr' in semtypes or 'lbtr' in semtypes or 'diap' in semtypes or 'dsyn' in semtypes or 'sosy' in semtypes:
                #print(preferred,semtypes,cui)
                tmp=[preferred,semtypes,cui]
                lst.append(tmp)
            '''
            #跑出error的item 單獨跑再合併
            tmp=[preferred,semtypes,cui]
            lst.append(tmp)
            
    remove=[]
    count=[]

    #計算次數
    for i in range(len(lst)):
        cnt=1
        for j in range(len(lst)):        
            if lst[i] == lst[j]:
                if i != j :
                    cnt+=1
        count.append(cnt)
    print(count)     
    print(len(count)) 
    #找重複
    for i in range(len(lst)):
        for j in range(len(lst)):
            #print(i,"  VS  ",j)
            #print(cnt)
            
            if lst[i] == lst[j]:
                if i != j : 
                    #print(i,"Equal",j)
                    remove.append(i)
                    lst[i]=[]#清空
                    #print(lst[i])
    #print(lst)     
    print(len(lst)) 
    print(remove)
    cnt=0
    #去重複
    for nan in remove:
        count.pop(nan-cnt)
        lst.pop(nan-cnt)
        cnt+=1
    #print(lst)
    print(len(lst))
    #print(count)     
    print(len(count))
    #將次數加入lst
    for i in range(len(lst)):
        lst[i].append(count[i])
        #print(lst[i])
    print(lst)
    
    #轉DataFrame
    df = pd.DataFrame(lst, columns = ['preferred','semtypes','cui','count'])
    print(df)
    #print(df['preferred'])
    #df.to_csv('./Meta_wiki_81_2.csv',index=0)





#文本轉出全部CUI

def toAllCui(csv_name):
    
    df = pd.read_csv('./test1_simple.csv')
    data = df['wiki_diagnosis'].tolist()

    with open('./CUI/wiki2AllCUI.csv','w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        lst_err=[]
        lst=[]
        c=0
        for row in data:
            c+=1
            print(csv_name ,'row=',c)
            if isinstance(row, str):#有值非空
                try:
                    sent_tmp = []
                    sent_tmp.append(row)
                    #print("sent=",sent_tmp, end = "\n\n")

                    concepts,error = mm.extract_concepts(sent_tmp)
                    #c+=1

                    for concept in concepts:
                        
                        string = str(concept) #每一筆matamap     
                        
                        #if c==3: print("C3=",string)
                        ConceptType = string[:string.index("(")]
                        #c+=1
                        if ConceptType=='ConceptMMI':
                            conceptItem = str(concept).split(', ')
                          
                            if len(conceptItem) == 10:#正常
                                string = conceptItem[3].strip().replace("'","")
                                preferred = string[string.index("=")+1:]
                                print(preferred)

                                string = conceptItem[4].strip().replace("'","")
                                cui = string[string.index("=")+1:]
                                print(cui)

                                string = conceptItem[5].strip().replace("'","")
                                semtypes = string[string.index("=")+1:]
                                print(semtypes.replace("[","").replace("]",""))

                                if 'lbpr' in semtypes or 'lbtr' in semtypes or 'diap' in semtypes or 'dsyn' in semtypes or 'sosy' in semtypes:
                                    #print(preferred,semtypes,cui)
                                    tmp=[preferred,semtypes,cui]
                                    lst.append(tmp)

                            else:
                                print(str(concept))


                            
                        #print("c=",c)
                        #print(preferred,semtypes,cui)
                
                except Exception as e:
                    print(csv_name +"檔案錯誤")
                    print(e)
                    string_e = csv_name+','+str(c)
                    lst_err.append(string_e)


            print('row done')
            print(MMS_array)
            #writer.writerow(MMS_array)
            MMS_array=[]

    print('done')    

#===============================  Main  ===============================
findOneMeta()
#CountMeta('asc_com_drugs')
'''
str_err = CountMeta('asc_com_drugs')
if  str_err != []:#error
    with open('ERROR_frq_drugs.txt', 'a',encoding="utf-8") as f:
        for err in str_err:                
            f.write(err+'\n')
    f.close()
#findAllMeta()
#findOneMeta()



#pubmed
df1= pd.read_csv('ICD_upd.csv')
ICD10 = df1['ICD10'].tolist()

for i in range(10,len(ICD10)):
#for i in range(len(ICD10)-1,-1,-1):
#for i in range(len(ICD10)):
    print(i)
    
    str_err = CountMeta(ICD10[i].strip())
    if  str_err != []:#error
        with open('ERROR_upd.txt', 'a',encoding="utf-8") as f:
            for err in str_err:                
                f.write(err+'\n')
        f.close()
'''
#CountMeta('asc_com_wiki')  
#toAllCui('')

#===============================  Main  ===============================