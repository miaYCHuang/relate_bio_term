# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:34:45 2022

@author: YC
"""
import re
import pandas as pd
import numpy as np



#SAS 讀取
import pandas as pd
import os
df = pd.read_csv('100.csv')
#df = pd.read_csv('ICD3noData.csv')
print(df)
ICD10 = df['ICD10'].tolist()
print(len(ICD10))

#SAS
#strr='PROC IMPORT\nDATAFILE='+'"'+'D:\\anaconda_code\MA\\'+ICD10[i]+'.csv'+'"'+'\nOUT=P'+i+'\nDBMS=CSV\nREPLACE;\nGETNAMES=YES;\nRUN;\n'
list=[]
for i in range(len(ICD10)):
    strr='PROC IMPORT\nDATAFILE='+'"'+'D:\\anaconda_code\PubMed_data\\'+ICD10[i]+'.csv'+'"'+'\nOUT=PM.P'+str(i+1)+'\nDBMS=CSV\nREPLACE;\nGETNAMES=YES;\nRUN;\n\n'
    list.append(strr)
path = 'PM_sas.txt'
f = open(path, 'w')
f.writelines(list)
f.close()


