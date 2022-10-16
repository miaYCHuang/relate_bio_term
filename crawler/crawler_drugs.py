# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:10:30 2021

ICD3.csv 
"ICD10 string"沒空格所以不能用isinstance(i, str)
"phenotype"有空格

ICD3_nan.csv
"ICD10 string"有空格
"phenotype"有空格

@author: user
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
delay_choices = [8, 5, 10, 6, 9, 11]  #延遲的秒數
'''→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→
    爬三個Drugs網頁資料
←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←'''
#df = pd.read_csv('ICD4.csv')
df = pd.read_csv('temp_reD.csv')
#df = pd.read_csv('ICD3noData.csv')
print(df)#查看CSV資料

#反被BAN
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36", #使用者代理
}


ICD = df['key'].tolist() # 'ICD10 string'


print("ICD",len(ICD))
#print(ICD)

lst_ICD=[]
lst_ICD2=[]
lst_ICD3=[]
for i in ICD:
    if isinstance(i, str):#字串  ICD3.csv沒空格
        n=i.replace("(","")
        n=i.replace(")","")
        n=i.replace(" ","-")
        #print(n)
        
        
        #網頁1
        r = requests.get("https://www.drugs.com/mcd/"+n, headers=headers) #將網頁資料GET下來
        soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
        if soup.title.text=="Page Not Found (404) - Drugs.com":
            lst_ICD.append("404")
        else:
            try:
                #t1 = soup.find("h2", text="Diagnosis").find_next_siblings()#<h2>Diagnosis</h2>後
                #t1 = soup.find("h2", text="Symptoms").find_next_siblings()#<h2>Symptoms</h2>後
                t1 = soup.find("h2", text="Overview").find_next_siblings()
                #print(t1)
                string=""
                for s in t1:
            
                    if s.name=="h2" :#遇到下一個<h2>則停止
                        break;
                    else:
                        string+=s.text
                #print(string)
                lst_ICD.append(string)
                delay = random.choice(delay_choices)  #隨機選取秒數
                time.sleep(delay)  #延遲
            except Exception as e:
                lst_ICD.append("NO Diagnosis")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
        
            
        #網頁2
        r2 = requests.get("https://www.drugs.com/health-guide/"+n+".html", headers=headers) #將網頁資料GET下來
        soup2 = BeautifulSoup(r2.text,"html.parser") #將網頁資料以html.parser
        if soup2.title.text=="Page Not Found (404) - Drugs.com":
            lst_ICD2.append("404")
        else:
            try:
                '''
                #t1 = soup2.find("h2", text="Diagnosis").find_next_siblings()#<h2>Diagnosis</h2>後
                t1 = soup2.find("h2", text="Symptoms").find_next_siblings()#<h2>Symptoms</h2>後
                #print(t1)
                string=""
                for s in t1:
                    if s.name=="h2" :#遇到下一個<h2>則停止
                        break;
                    else:
                        string+=s.text
                #print(string)
                '''
               #因next_siblings會多出現</img>所以用previous_siblings向前找overview資料
                t1 = soup2.find("h2", id="symptoms").find_previous_siblings()
                string=""
                for s in t1:
                    string=s.text + string #倒裝
                print(string)
                
                
                
                lst_ICD2.append(string)
                delay = random.choice(delay_choices)  #隨機選取秒數
                time.sleep(delay)  #延遲
            except Exception as e:
                lst_ICD2.append("NO Diagnosis")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
                
        
        
        #網頁3  What is XXX?  overview
        r3 = requests.get("https://www.drugs.com/cg/"+n+".html", headers=headers) #將網頁資料GET下來
        soup3 = BeautifulSoup(r3.text,"html.parser") #將網頁資料以html.parser
        if soup3.title.text=="Page Not Found (404) - Drugs.com":
            lst_ICD3.append("404")
        else:
            try:
                
                t3 = soup3.find("h2", id="overview").find_next_siblings()
                #print(t3)
                string=""
                for s in t3:
                    if s.name=="h2" :#遇到下一個<h2>則停止
                        break;
                    else:
                        string+=s.text
                #print(string)
                
                lst_ICD3.append(string)
                delay = random.choice(delay_choices)  #隨機選取秒數
                time.sleep(delay)  #延遲
            except Exception as e:
                lst_ICD3.append("NO Diagnosis")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
        
        '''
        #網頁3 diagnosed / signs and symptoms
        if soup3.title.text=="Page Not Found (404) - Drugs.com":
            lst_ICD3.append("404")
        else:
            cg = soup3.find_all('h2')
            length=0
            for s in cg:
                #if s.text.find('diagnosed?') !=-1:#找含有"diagnosed?"
                if s.text.find('signs and symptoms') !=-1:
                    #print(s.text)
                    try:
                        h2ToEnd = soup3.find("h2", text=s.text).find_next_siblings()#<h2>Diagnosis</h2>後
                        #print(t2)
                        string=""
                        for s in h2ToEnd:
                            if s.name=="h2" :#遇到下一個<h2>則停止
                                break;
                            else:
                                string+=s.text
                        #print(string)
                        
                        lst_ICD3.append(string)
                        delay = random.choice(delay_choices)  #隨機選取秒數
                        time.sleep(delay)  #延遲
                    except Exception as e:
                        lst_ICD3.append("NO Diagnosis")
                        error_class = e.__class__.__name__
                        #print(error_class,":",e)
                else:#找不到h2文字有diagnosed?
                    length+=1;
                    if length==len(cg):#全部h2都沒diagnosed?
                        lst_ICD3.append("NO Diagnosis")
        '''
    else:#nan
        lst_ICD.append("")
        lst_ICD2.append("")
        lst_ICD3.append("")



print("lst_ICD",len(lst_ICD))
print("lst_ICD2",len(lst_ICD2))
print("lst_ICD3",len(lst_ICD3))
#dict = {'ICD_DsWeb2':lst_ICD2}
dict = {'ICD_DsWeb1':lst_ICD,'ICD_DsWeb2':lst_ICD2,'ICD_DsWeb3':lst_ICD3} 
df = pd.DataFrame(dict) 
df.to_csv('output_DrugWeb.csv',index=0) #index=0 沒有第一col的id

'''
Phe = df['phenotype'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype

print("Phe",len(Phe))
#print(ICD)

lst_Phe=[]
lst_Phe2=[]
lst_Phe3=[]
for i in Phe:
    if isinstance(i, str):#字串  ICD3.csv  phenotype 有空格
        n=i.replace(" ","-")
        #print(n)
        
        
        #網頁1
        r = requests.get("https://www.drugs.com/mcd/"+n, headers=headers) #將網頁資料GET下來
        soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
        if soup.title.text=="Page Not Found (404) - Drugs.com":
            lst_Phe.append("404")
        else:
            try:
                t1 = soup.find("h2", text="Diagnosis").find_next_siblings()#<h2>Diagnosis</h2>後
                #t1 = soup.find("h2", text="Symptoms").find_next_siblings()#<h2>Symptoms</h2>後
                #print(t1)
                string=""
                for s in t1:
            
                    if s.name=="h2" :#遇到下一個<h2>則停止
                        break;
                    else:
                        string+=s.text
                #print(string)
                
                lst_Phe.append(string)
                delay = random.choice(delay_choices)  #隨機選取秒數
                time.sleep(delay)  #延遲
            except Exception as e:
                lst_Phe.append("NO Diagnosis")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
         
            
        #網頁2
        r2 = requests.get("https://www.drugs.com/health-guide/"+n+".html", headers=headers) #將網頁資料GET下來
        soup2 = BeautifulSoup(r2.text,"html.parser") #將網頁資料以html.parser
        if soup2.title.text=="Page Not Found (404) - Drugs.com":
            lst_Phe2.append("404")
        else:
            try:
                t1 = soup2.find("h2", text="Diagnosis").find_next_siblings()#<h2>Diagnosis</h2>後
                #t1 = soup2.find("h2", text="Symptoms").find_next_siblings()#<h2>Symptoms</h2>後
                #print(t1)
                string=""
                for s in t1:
                    if s.name=="h2" :#遇到下一個<h2>則停止
                        break;
                    else:
                        string+=s.text
                #print(string)
                
                lst_Phe2.append(string)
                delay = random.choice(delay_choices)  #隨機選取秒數
                time.sleep(delay)  #延遲
            except Exception as e:
                lst_Phe2.append("NO Diagnosis")
                error_class = e.__class__.__name__
                #print(error_class,":",e)
                
        
        #網頁3
        r3 = requests.get("https://www.drugs.com/cg/"+n+".html", headers=headers) #將網頁資料GET下來
        soup3 = BeautifulSoup(r3.text,"html.parser") #將網頁資料以html.parser
        if soup3.title.text=="Page Not Found (404) - Drugs.com":
            lst_Phe3.append("404")
        else:
            cg = soup3.find_all('h2')
            length=0
            for s in cg:
                if s.text.find('diagnosed?') !=-1:
                #if s.text.find('signs and symptoms') !=-1:
                    #print(s.text)
                    try:
                        h2ToEnd = soup3.find("h2", text=s.text).find_next_siblings()#<h2>Diagnosis</h2>後
                        #print(t2)
                        string=""
                        for st in h2ToEnd:
                            if st.name=="h2" :#遇到下一個<h2>則停止
                                break;
                            else:
                                string+=st.text
                        #print(string)
                        
                        lst_Phe3.append(string)
                        delay = random.choice(delay_choices)  #隨機選取秒數
                        time.sleep(delay)  #延遲
                    except Exception as e:
                        lst_Phe3.append("NO Diagnosis")
                        error_class = e.__class__.__name__
                        #print(error_class,":",e)
                else:
                    length+=1;
                    if length==len(cg):
                        lst_Phe3.append("NO Diagnosis")
    else:#nan
        lst_Phe.append("")
        lst_Phe2.append("")
        lst_Phe3.append("")
  
print("lst_Phe",len(lst_Phe))
print("lst_Phe2",len(lst_Phe2))
print("lst_Phe3",len(lst_Phe3))

#dict = {'ICD_DsWeb1':lst_ICD,'ICD_DsWeb2':lst_ICD2,'ICD_DsWeb3':lst_ICD3,'Phe_DsWeb1':lst_Phe,'Phe_DsWeb2':lst_Phe2,'Phe_DsWeb3':lst_Phe3}
dict = {'ICD_DsWeb1':lst_ICD,'ICD_DsWeb2':lst_ICD2,'ICD_DsWeb3':lst_ICD3}
#dict = {'Phe_DsWeb1':lst_Phe,'Phe_DsWeb2':lst_Phe2,'Phe_DsWeb3':lst_Phe3} 
df = pd.DataFrame(dict) 
df.to_csv('./Output/output_DrugWeb.csv',index=0) #index=0 沒有第一col的id
'''




'''
#→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→
#    Drugs搜尋頁面
#←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←


df = pd.read_csv('ICD3.csv')
#print(df)#查看CSV資料
ICD = df['ICD10 string'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
#print(len(ICD))

name=[]
for i in ICD:
    if isinstance(i, str):#字串
        n=i.replace(" ","+")
        n=n.replace("(","%28")
        n=n.replace(")","%29")
        n=n.replace("/","%2F")
        n=n.replace("[","%5B")
        n=n.replace("]","%5D")
        n=n.replace(",","%2C")
        n=n.replace("'","%27")
        print(n)
        r = requests.get("https://www.drugs.com/search.php?searchterm="+n+"&sources%5B%5D=") #將網頁資料GET下來
        soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
        #print(soup)
        try:
            t1 = soup.find("p" , class_="ddc-text-size-large-2")
            name.append(t1.a.text)
        except Exception as e:
            name.append(" ")
            error_class = e.__class__.__name__
            print(error_class,":",e)
    else:
        name.append(" ")
phe = df['phenotype'].tolist() # 1 col變成LIST  'title' ICD10 string phenotype
#print(len(ICD))



#搜尋頁面
name_phe=[]
for i in phe:
    if isinstance(i, str):#字串
        n=i.replace(" ","+")
        n=n.replace("(","%28")
        n=n.replace(")","%29")
        n=n.replace("/","%2F")
        n=n.replace("[","%5B")
        n=n.replace("]","%5D")
        n=n.replace(",","%2C")
        n=n.replace("'","%27")
        #print(n)
        r = requests.get("https://www.drugs.com/search.php?searchterm="+n+"&sources%5B%5D=") #將網頁資料GET下來
        soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
        #print(soup)
        try:
            t1 = soup.find("p" , class_="ddc-text-size-large-2")
            print(i)
            print(t1.a.text)
            name_phe.append(t1.a.text)
        except Exception as e:
            name_phe.append(" ")
            error_class = e.__class__.__name__
            #print(error_class,":",e)
    else:
        name_phe.append(" ")
print(name)
print(name_phe)
print(len(name))
print(len(name_phe))

dict = {'ICD_DsName':name,'Phe_DsName':name_phe} 
df = pd.DataFrame(dict) 
df.to_csv('output_DrugName.csv',index=0)#index=0 沒有第一col的id
'''