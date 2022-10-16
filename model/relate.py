# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:17:56 2022

@author: YC
"""
import pickle
import pandas as pd
#========================
#將t-d t-s合併成一個檔案
#統一
#檢查
#========================

#get t-d
file = open( "./vector/w2v/w2v_pubmed_word_t2d.p", "rb")
#file = open( "./vector/bio/bio_all_cui_t2d.p", "rb")
df_td = pickle.load(file)
file.close()
print(df_td.columns.values)#取得title
#title改名
df_td = df_td.rename(columns={"doc_t": "doc_1", "test": "map_1", "vec_t": "vec_1", "doc_d": "doc_2", "disease": "map_2", "vec_d": "vec_2"})
#df_td = df_td.rename(columns={"doc_t": "doc_1", "map_t": "map_1", "vec_t": "vec_1", "doc_d": "doc_2", "map_d": "map_2", "vec_d": "vec_2"})



#get t-s
file = open( "./vector/w2v/w2v_pubmed_word_t2s_2.p", "rb")
#file = open( "./vector/bio/bio_all_cui_t2s.p", "rb")
df_ts = pickle.load(file)
file.close()
print(df_ts.columns.values)#取得title
#df_ts.to_csv('./vector/w2v/t.csv',index=0)
#title改名
df_ts = df_ts.rename(columns={"doc_t": "doc_1", "map_t": "map_1", "vec_t": "vec_1", "doc_s": "doc_2", "map_s": "map_2", "vec_s": "vec_2"})



df_new = pd.concat([df_td,df_ts],axis=0, ignore_index=True)#合併
df_new = df_new.drop(['cosine', 'cosine_Std'], axis=1)
pickle.dump( df_new, open( "./vector/ans/w2v_pubmed_word.p", "wb" ) )

#%%
#檢查向量是否正確
#w2v
from gensim.models.word2vec import Word2Vec
import numpy as np

def LoadModel(num,fileName):
    if num==1:
        model = Word2Vec.load('./result/w2v/'+fileName+'/w2v_'+fileName+'_1.model')
    elif num==2:
        model = Word2Vec.load('./result/w2v/'+fileName+'/w2v_'+fileName+'_2.model')
    elif num==3:
        model = Word2Vec.load('./result/w2v/'+fileName+'/w2v_'+fileName+'_3.model')
    elif num==4:
        model = Word2Vec.load('./result/w2v/'+fileName+'/w2v_'+fileName+'_4.model')
    return model
        
file = open( "./vector/ans/w2v_wiki_word.p", "rb")
df = pickle.load(file)
file.close()

lst = [0,2,17,37,38,54,66,70,77,78]

for n in lst:
    #print(df.iloc[n])
    print(len(df['map_1'][n].split()),df['map_1'][n])
    print(len(df['map_2'][n].split()),df['map_2'][n])
    
    model_1 = LoadModel(len(df['map_1'][n].split()),'wiki')
    model_2 = LoadModel(len(df['map_2'][n].split()),'wiki')

    
    #比較是否相同
    if np.array_equal(model_1.wv[df['map_1'][n].lower()], df['vec_1'][n]) == False:
        print("1:不相同")
    else:
        print("1:相同")
        
    if np.array_equal(model_2.wv[df['map_2'][n].lower()], df['vec_2'][n]) == False:
        print("2:不相同")
    else:
        print("2:相同")
    print("*****************")

#%%
#檢查向量是否正確
#w2v  cui
# WIKI DRUG 缺值

fileName = "all"
file = open( "./vector/ans/w2v_"+fileName+"_cui.p", "rb")
df = pickle.load(file)
file.close()
print(len(df))

lst_empty = df.index[(df[ "vec_1" ] == "" ) | (df[ "vec_2" ] == "" )]
lst_empty = list(set(lst_empty))#去重複
print(len(lst_empty))

#只用於CUI  WIKI DRUG
df.drop(lst_empty,axis= 0 ,inplace= True )#刪除不存在VEC的
df = df.reset_index(drop= True)#重置index
print(len(df))



lst = [0,2,17,37,38,54,66,70,77,78]
#lst = [0,7,16]
for n in lst:
    #print(df.iloc[n])
    #print(len(df['doc_1'][n].split()),df['doc_1'][n])
    #print(len(df['doc_2'][n].split()),df['doc_2'][n])

  
    model_1 = Word2Vec.load('./result/w2v/'+fileName+'/w2v_'+fileName+'_meta.model')  
    #比較是否相同
    if np.array_equal(model_1.wv[df['map_1'][n]], df['vec_1'][n]) == False:
        print("1:不相同")
    else:
        print("1:相同")
    
    if np.array_equal(model_1.wv[df['map_2'][n]], df['vec_2'][n]) == False:
        print("2:不相同")
    else:
        print("2:相同")
    print("*****************")
    
#%%
#檢查向量是否正確
#bioWV word
import numpy as np
       
lst_id =['1','2','3','4']
for gram in lst_id:
    
    print("gram:",gram)
    fileName = 'drugs'
  
    #file = open( "./vector/ans/bio_"+fileName+"_word_"+gram+".p", "rb")
    file = open( "./vector/ans/bio_"+fileName+"_cui.p", "rb")
    df = pickle.load(file)
    file.close()
    
    #lst = [0,2,17,37,38,54,66,70,77,78]
    lst = [37,38,54,66]
    for n in lst:
        #print(df.iloc[n])
        print(len(df['doc_1'][n].split()),df['doc_1'][n])
        print(len(df['doc_2'][n].split()),df['doc_2'][n])

        model_1 = Word2Vec.load('C:/Users/YC/OneDrive - 國立中正大學/桌面/BioWordVec-master/bio/'+fileName+'/bio_'+fileName+'_'+gram)    
        
        #比較是否相同
        if np.array_equal(model_1.wv[df['doc_1'][n].lower()], df['vec_1'][n]) == False:
            print("1:不相同")
        else:
            print("1:相同")
    
        if np.array_equal(model_1.wv[df['doc_2'][n].lower()], df['vec_2'][n]) == False:
            print("2:不相同")
        else:
            print("2:相同")
        print("*****************")


#%%
#檢查向量是否正確
#bioWV  cui

fileName = "drugs"
file = open( "./vector/ans/bio_"+fileName+"_cui.p", "rb")

df = pickle.load(file)
file.close()

#lst = [0,2,17,37,38,54,66,70,77,78]
lst = [0,7,16]
for n in lst:
    #print(df.iloc[n])
    #print(len(df['doc_1'][n].split()),df['doc_1'][n])
    #print(len(df['doc_2'][n].split()),df['doc_2'][n])
    
    #model_1 = FastText.load('./BioWordVec-master/bio/pubmed/bio_'+fileName+'_meta') 
    model_1 = Word2Vec.load('C:/Users/YC/OneDrive - 國立中正大學/桌面/BioWordVec-master/bio/'+fileName+'/bio_'+fileName+'_meta')    
  
    #比較是否相同

    if np.array_equal(model_1.wv[df['doc_1'][n].lower()], df['vec_1'][n]) == False:
        print("1:不相同")
    else:
        print("1:相同")
    

    if np.array_equal(model_1.wv[df['doc_2'][n].lower()], df['vec_2'][n]) == False:
        print("2:不相同")
    else:
        print("2:相同")
    print("*****************")

#%%
#檢查向量是否正確
#1+向量 = 2-4 gram

#載術語
file = open( "./vector/ans/w2v_wiki_word.p", "rb")
df = pickle.load(file)
file.close()

#斷字
def splitWord(new_data):
    data_Subj = []
    for i in range(len(new_data)):
        d = [x for x in new_data[i].split(' ') if x] #斷字&去空格
        data_Subj.append(d) 
            
    print(len(data_Subj))   
    return data_Subj

def embedding_feats_subj(list_of_lists):
    DIMENSION = 200
    zero_vector = np.zeros(DIMENSION)
    feats = []
    for tokens in list_of_lists:
        feat_for_this =  np.zeros(DIMENSION)
        count_for_this = 0 + 1e-5 # to avoid divide-by-zero 
        for token in tokens:
            token=token.strip().lower()
            if token in w2v_model_subj.wv:
                feat_for_this += w2v_model_subj.wv[token]
                count_for_this +=1
        if(count_for_this!=0):
            feats.append(feat_for_this/count_for_this) 
        else:
            print(tokens)
            feats.append(zero_vector)
    return feats


map1=splitWord(df['map_1'].tolist())
map2=splitWord(df['map_2'].tolist())


lenth3=[i for i in map1 if len(i)==3]
print(lenth3[0])
stri = (' '.join(lenth3[0])).lower()
print(stri)



w2v_model_subj = Word2Vec.load('./result/w2v/wiki/w2v_wiki_1.model')
   
vec= embedding_feats_subj([lenth3[0]])

print(vec)


model_2 = Word2Vec.load('./result/w2v/wiki/w2v_wiki_3.model') 

print(model_2.wv[stri])
#比較是否相同

if np.array_equal(vec, model_2.wv[stri]) == False:
    print("1:不相同")
else:
    print("1:相同")

    
#%%    

file = open( "./result/bio_paper.p", "rb")
df = pickle.load(file)
file.close()

#%%
#計算cosine  euclidean
#https://medium.com/geekculture/cosine-similarity-and-cosine-distance-48eed889a5c4
# spearmanr
from scipy import spatial
from scipy.stats import spearmanr
import numpy as np
import scipy.stats
def Normalization(x):
    return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]
'''
wiki
drugs
pubmed
all
'''
#files='w2v_all_word'
#files='bio_all_word_3'
files='w2v_pubmed_cui'
#files='bio_wiki_word_1_Vcom'# w2v_all_word_Vcom  bio_pubmed_word_1_Vcom   !! 記得改 vec_com_1 !!
file = open( "./vector/ans/"+files+".p", "rb")
df = pickle.load(file)
file.close()


# file = open( "./result/bio_paper.p", "rb")
# df = pickle.load(file)
# file.close()




lst_cos=[]
lst_eu=[]
for i in range(df.shape[0]):
    result_c = 1 - spatial.distance.cosine(df['vec_1'][i], df['vec_2'][i])
    #result_c = 1 - spatial.distance.cosine(df['vec_com_1'][i], df['vec_com_2'][i])
    lst_cos.append(result_c)
    
    result_e = spatial.distance.euclidean(df['vec_1'][i], df['vec_2'][i])
    #result_e = spatial.distance.euclidean(df['vec_com_1'][i], df['vec_com_2'][i])
    lst_eu.append(result_e*(-1))#*(-1) 讓數值從小到大(不相關-相關)




df_new = df.assign(cosine = lst_cos,  euclidean = lst_eu  )#增加在原本後面


df_ans = pd.read_csv('ans.csv')
y = df_ans['mean'].tolist()
# y = df_ans['median'].tolist()
# y = df_ans['mode'].tolist()


nor = scipy.stats.shapiro(df_new['cosine'])
print(nor[1])
if nor[1]<0.05:
    print("不是常態")
else:
    print("常態")
    pearson = scipy.stats.pearsonr(df_new['cosine'], y)
    if pearson[1] < 0.05:
        print(round(pearson[0], 2),"*")
    else:
        print(round(pearson[0], 2))




# y.pop(96)
# df_new['cosine'].pop(96)
# df_new['euclidean'].pop(96)
# print(len(y),len(df_new['cosine']))

# import numpy as np
# cos = np.array(df_new['cosine'])
# eu = np.array(df_new['euclidean'])
# y = np.array(y)
# corr = np.corrcoef(cos, y)
# print("COS",round(corr[0][1],2))
# corr = np.corrcoef(eu, y)
# print("EU",round(corr[0][1],2))


# correlation, p = spearmanr(df_new['cosine'], y)#cosine
# print('Correlation_cos:', round(correlation, 2))
# correlation, p = spearmanr(df_new['euclidean'], y)#euclidean
# print('Correlation_eu:', round(correlation, 2))
# print("========================")
# correlation, p = spearmanr(df_new['cosine'][0:50], y[0:50])#cosine
# print('Correlation_cos:', round(correlation, 2))

# correlation, p = spearmanr(df_new['euclidean'][0:50], y[0:50])#euclidean
# print('Correlation_eu:', round(correlation, 2))

# print("========================")

# correlation, p = spearmanr(df_new['cosine'][50:100], y[50:100])#cosine
# print('Correlation_cos:', round(correlation, 2))

# correlation, p = spearmanr(df_new['euclidean'][50:100], y[50:100])#euclidean
# print('Correlation_eu:', round(correlation, 2))

                               
                               

#%%
#計算cosine  euclidean
# spearmanr
# w2v -> wiki drugs CUI 缺值
from scipy import spatial
from scipy.stats import spearmanr
import numpy as np

lst_empty=[]


files='bio_drugs_cui'#w2v_wiki_cui
file = open( "./vector/ans/"+files+".p", "rb")
df = pickle.load(file)
file.close()
print(len(df))

lst_empty = df.index[(df[ "vec_1" ] == "" ) | (df[ "vec_2" ] == "" )]#存不存在VEC的INDEX
lst_empty = list(set(lst_empty))
print(len(lst_empty))#去重複




# lst_empty.append(96)#去96題
# print(lst_empty)




#只用於CUI  WIKI DRUG
df.drop(lst_empty,axis= 0 ,inplace= True )#刪除不存在VEC的
df = df.reset_index(drop= True)#重置index
print(len(df))


lst_cos=[]
lst_eu=[]
for i in range(df.shape[0]):
    result_c = 1 - spatial.distance.cosine(df['vec_1'][i], df['vec_2'][i])
    lst_cos.append(result_c)
    
    result_e = spatial.distance.euclidean(df['vec_1'][i], df['vec_2'][i])
    lst_eu.append(result_e*(-1))#*(-1) 讓數值從小到大(不相關-相關)
    
    
df_new = df.assign(cosine = lst_cos,  euclidean = lst_eu  )#增加在原本後面
print(len(df_new))

#pickle.dump( df_new, open( "./vector/ans/relate/" + files + "_relate.p", "wb" ) )



df_ans = pd.read_csv('ans.csv')
df_ans.drop(lst_empty,axis= 0 ,inplace= True )#刪除不存在VEC的
y = df_ans['mean'].tolist()
#y = df_ans['median'].tolist()
#y = df_ans['mode'].tolist()


nor = scipy.stats.shapiro(df_new['cosine'])
print(nor[1])
if nor[1]<0.05:
    print("不是常態")
else:
    print("常態")
    pearson = scipy.stats.pearsonr(df_new['cosine'], y)
    if pearson[1] < 0.05:
        print(round(pearson[0], 2),"*")
    else:
        print(round(pearson[0], 2))
    
    
# import numpy as np
# cos = np.array(df_new['cosine'])
# eu = np.array(df_new['euclidean'])
# y = np.array(y)
# corr = np.corrcoef(cos, y)
# print("COS",round(corr[0][1],2))
# corr = np.corrcoef(eu, y)
# print("EU",round(corr[0][1],2))

# correlation, p = spearmanr(df_new['cosine'], y)#cosine
# print('Correlation_cos:', round(correlation, 2))

# correlation, p = spearmanr(df_new['euclidean'], y)#euclidean
# print('Correlation_eu:', round(correlation, 2))
# print("========================")
# correlation, p = spearmanr(df_new['cosine'][0:50], y[0:50])#cosine
# print('Correlation_cos:', round(correlation, 2))

# correlation, p = spearmanr(df_new['euclidean'][0:50], y[0:50])#euclidean
# print('Correlation_eu:', round(correlation, 2))

# print("========================")

# correlation, p = spearmanr(df_new['cosine'][50:100], y[50:100])#cosine
# print('Correlation_cos:', round(correlation, 2))

# correlation, p = spearmanr(df_new['euclidean'][50:100], y[50:100])#euclidean
# print('Correlation_eu:', round(correlation, 2))




#%%
#長條圖
#https://pythonguides.com/stacked-bar-chart-matplotlib/
#https://www.pythoncharts.com/matplotlib/stacked-bar-charts-labels/

import matplotlib.pyplot as plt
#ALL
# agg_tips = pd.DataFrame({
#     'W2V': [0.45 ,0.48, 0.42],
#     'Bio-cui': [0 ,0, 0],
#     'Bio-1': [0.27 ,0.17,  0.37],
#     'Bio-2': [0.42 ,0.35,  0.55],
#     'Bio-3': [0.47 ,0.38,  0.59],
#     'Bio-4': [0.43 ,0.33,  0.56],
#   })
# agg_tips2 = pd.DataFrame({
#     'W2V': [0.63 ,0.54, 0.74],
#     'Bio-cui': [0.46 ,0.32, 0.63],
#     'Bio-1': [0 ,0,  0],
#     'Bio-2': [0 ,0,  0],
#     'Bio-3': [0 ,0,  0],
#     'Bio-4': [0 ,0,  0],
#   })
#PM
# agg_tips = pd.DataFrame({
#     'W2V': [0.12 ,0.01, 0.3],
#     'Bio-cui': [0 ,0, 0],
#     'Bio-1': [0.24 ,0.17,  0.32],
#     'Bio-2': [0.4 ,0.34,  0.53],
#     'Bio-3': [0.43 ,0.36,  0.53],
#     'Bio-4': [0.44 ,0.33,  0.59],
#   })
# agg_tips2 = pd.DataFrame({
#     'W2V': [0.64 ,0.54, 0.77],
#     'Bio-cui': [0.52 ,0.38, 0.69],
#     'Bio-1': [0 ,0,  0],
#     'Bio-2': [0 ,0,  0],
#     'Bio-3': [0 ,0,  0],
#     'Bio-4': [0 ,0,  0],
#   })
#DRUGS
agg_tips = pd.DataFrame({
    'W2V': [0.06 ,0.01, 0.16],
    'Bio-cui': [0 ,0, 0],
    'Bio-1': [0.19 ,0.24,  0.16],
    'Bio-2': [0.23 ,0.29,  0.26],
    'Bio-3': [0.25 ,0.27,  0.25],
    'Bio-4': [0.23 ,0.29,  0.22],
  })
agg_tips2 = pd.DataFrame({
    'W2V': [0.11 ,0.28, 0.15],#-0.15
    'Bio-cui': [0.12 ,-0.0, 0.25],
    'Bio-1': [0 ,0,  0],
    'Bio-2': [0 ,0,  0],
    'Bio-3': [0 ,0,  0],
    'Bio-4': [0 ,0,  0],
  })
#WIKI
# agg_tips = pd.DataFrame({
#     'W2V': [0.34 ,0.26, 0.4],
#     'Bio-cui': [0 ,0, 0],
#     'Bio-1': [0.22 ,0.27,  0.18],
#     'Bio-2': [0.21 ,0.27,  0.17],
#     'Bio-3': [0.23 ,0.28,  0.2],
#     'Bio-4': [0.21 ,0.28,  0.14],
#   })
# agg_tips2 = pd.DataFrame({
#     'W2V': [0.05 ,0.02, 0.21],
#     'Bio-cui': [0.11 ,0.02, 0.21],
#     'Bio-1': [0 ,0,  0],
#     'Bio-2': [0 ,0,  0],
#     'Bio-3': [0 ,0,  0],
#     'Bio-4': [0 ,0,  0],
#   })


N=agg_tips.shape[0]
len_x = np.arange(N)
width=0.4
w1= len_x - width/2
w2= len_x + width/2

print(agg_tips.shape)

fig, ax = plt.subplots()
Class = ["All","test-disease","test-symptom"]
colors = ['#B9D7EA', '#769FCD','#769FCD', '#769FCD', '#769FCD', '#769FCD']
bottom = np.zeros(len(agg_tips))
bottom2 = np.zeros(len(agg_tips))
#顏色
for i, col in enumerate(agg_tips.columns):
  print("i:",i, "COL:",col )
  print(agg_tips[col],type(agg_tips[col]))

  ax.bar(#agg_tips.index
    w1, agg_tips[col], bottom=bottom, label=col, color=colors[i],width=0.4,edgecolor='k')#width=0.2 ,hatch="."
  bottom += np.array(agg_tips[col])
  
  #new=[abs(i)  for i in agg_tips2[col]]
  
  ax.bar(w2, agg_tips2[col] , bottom=bottom2, color=colors[i],width=0.4,edgecolor='k')#, label=col
  bottom2 += np.array(agg_tips2[col])


totals = agg_tips.sum(axis=1)
y_offset = 0.01
#最上平均值
for i, total in enumerate(totals):
  print(i,total)
  mean = round(total/5,2)
  axis_x=totals.index[i]-0.2
  ax.text(axis_x, total + y_offset, mean, ha='center',weight='bold'
          )#weight='bold'

totals = agg_tips2.sum(axis=1)
y_offset = 0.05
#最上平均值
for i, total in enumerate(totals):
  print(i,total)
  mean = round(total/2,2)
  axis_x=totals.index[i]+0.2
  ax.text(axis_x, total + y_offset, mean, ha='center'
          )
  
  

#中間數值 
for bar in ax.patches:
    
    height = bar.get_height()
    width = bar.get_width()
    x = bar.get_x()
    y = bar.get_y()
    label_text = round(height, 2)
    label_x = x + width / 2
    label_y = y + height / 2
    if label_text != 0.0:
        # ax.text(label_x, label_y, label_text, ha='center',    
        # va='center')
        
        if label_text >=0.01 :#0.05
            ax.text(label_x, label_y, label_text, ha='center',    
                va='center')
        
ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')  #介紹位置



ax.set_xticks(len_x)#x長度
ax.set_xticklabels(Class)#,rotation='horizontal'

ax.set_title('Training Dataset - Drugs.com')
ax.set_xlabel('Word/CUI')
ax.set_ylabel("Sum of Spearman's Rank Correlations")


  

  
#%%
#畫圖
#https://stackoverflow.com/questions/68608526/creating-and-annotating-a-grouped-barplot-in-python

#ALL
# df = pd.DataFrame.from_dict({
#   'W2V:1-4 gram': {'All': 0.45, 'test-disease': 0.48, 'test-symptom': 0.42},
#   'W2V:1 gram+vec': {'All': 0.11, 'test-disease': 0.08, 'test-symptom': 0.13},
#   'Bio:mean(1+2+3+4 gram)': {'All': 0.4, 'test-disease': 0.3, 'test-symptom': 0.52},
#   'Bio:1 gram+vec': {'All': 0.19, 'test-disease': 0.19, 'test-symptom': 0.24}
#   })
#PM
df = pd.DataFrame.from_dict({
  'W2V:1-4 gram': {'All': 0.12, 'test-disease': 0.01, 'test-symptom': 0.3},
  'W2V:1 gram+vec': {'All': 0.1, 'test-disease': 0.2, 'test-symptom': 0.05},
  'Bio:mean(1+2+3+4 gram)': {'All': 0.38, 'test-disease': 0.3, 'test-symptom': 0.49},
  'Bio:1 gram+vec': {'All': 0.15, 'test-disease': 0.2, 'test-symptom': 0.19}
  })
#DRUGS
# df = pd.DataFrame.from_dict({
#   'W2V:1-4 gram': {'All': 0.06, 'test-disease': 0.01, 'test-symptom': 0.16},
#   'W2V:1 gram+vec': {'All': -0.09, 'test-disease': -0.03, 'test-symptom': -0.15},
#   'Bio:mean(1+2+3+4 gram)': {'All': 0.23, 'test-disease': 0.27, 'test-symptom': 0.22},
#   'Bio:1 gram+vec': {'All': 0.12, 'test-disease': 0.23, 'test-symptom': 0.09}
#   })
#WIKI
# df = pd.DataFrame.from_dict({
#   'W2V:1-4 gram': {'All': 0.34, 'test-disease': 0.26, 'test-symptom': 0.4},
#   'W2V:1 gram+vec': {'All': 0.21, 'test-disease': 0.21, 'test-symptom': 0.2},
#   'Bio:mean(1+2+3+4 gram)': {'All': 0.22, 'test-disease': 0.28, 'test-symptom': 0.17},
#   'Bio:1 gram+vec': {'All': 0.12, 'test-disease': 0.24, 'test-symptom': 0.06}
#   })



fig, ax = plt.subplots(figsize=(8, 4))

df.plot.bar(rot=0, ax=ax, zorder=2,
    color=["#C4DDFF", "cornflowerblue", "#FFBBBB", "salmon"])#color=["cornflowerblue", "yellowgreen", "gold", "salmon"]

for container in ax.containers:
    print(container)
    ax.bar_label(container, padding=3)


plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.grid(True, axis='y', c="lightgrey", zorder=0)
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.set_title('Training Dataset - PubMed')
ax.set_ylabel("Spearman's Rank Correlations")