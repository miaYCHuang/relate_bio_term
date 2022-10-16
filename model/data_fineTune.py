# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 20:42:30 2022
處理微調資料
@author: YC
"""
import pandas as pd
from gensim.models.word2vec import Word2Vec
import pickle
from scipy import spatial
from scipy.stats import spearmanr

#%%
#w2v model分gram計算  所以  1-4各向量合併
# d t s 各 分1-4
file = open( "./dataset/fine-tune_data/vector_w2v_all_d_1_term.p", "rb")
v1 = pickle.load(file)
file.close()
file = open( "./dataset/fine-tune_data/vector_w2v_all_d_2_term.p", "rb")
v2 = pickle.load(file)
file.close()
file = open( "./dataset/fine-tune_data/vector_w2v_all_d_3_term.p", "rb")
v3 = pickle.load(file)
file.close()
file = open( "./dataset/fine-tune_data/vector_w2v_all_d_4_term.p", "rb")
v4 = pickle.load(file)
file.close()

df = pd.concat([v1, v2,v3,v4], ignore_index = True, axis = 0)
pickle.dump( df, open( "./vector/w2v_all_d_50.p", "wb" ) )




#%%
#===============
# 微調資料
# bio_all_word_3
# w2v_pubmed_cui
#===============
#透過術語集D S T各50對術語 放入模型取得向量

df1= pd.read_csv('term_word.csv')
t = df1['t_cui'].tolist()
d = df1['d_cui'].tolist()
s = df1['s_cui'].tolist()

model = Word2Vec.load('./result/w2v/pubmed/w2v_pubmed_meta.model')

#CUI = ['C0005684','C1269683','C0853697']
cnt=0
vec_t=[]
vec_d=[]
vec_s=[]
for i in range(df1.shape[0]):
    try:
        vec_t.append(model.wv[t[i]])
        vec_d.append(model.wv[d[i]])
        vec_s.append(model.wv[s[i]])
    except:
        cnt+=1
        print('NO',i)
print(cnt,"個 -> 找不到")      
dict = {'d': df1['d'].tolist(),'vec_d': vec_d     ,'t': df1['t'].tolist(),'vec_t': vec_t     ,'s': df1['s'].tolist(),'vec_s': vec_s}
df_new = pd.DataFrame(dict)
print(df_new)

pickle.dump( df_new, open( "./vector/w2v_pubmed_meta_50.p", "wb" ) )

#%%
#組合5K
#計算每對COS
word_a=[]
word_b=[]
vec_a=[]
vec_b=[]
cos=[]

for i in range(df_new.shape[0]):
    for j in range(df_new.shape[0]):
        
        word_a.append(df_new['t'][i])
        word_b.append(df_new['d'][j])
        vec_a.append(df_new['vec_t'][i])
        vec_b.append(df_new['vec_d'][j])
        result = 1 - spatial.distance.cosine(df_new['vec_t'][i], df_new['vec_d'][j])
        cos.append(result)
        
        word_a.append(df_new['t'][i])
        word_b.append(df_new['s'][j])
        vec_a.append(df_new['vec_t'][i])
        vec_b.append(df_new['vec_s'][j])
        result = 1 - spatial.distance.cosine(df_new['vec_t'][i], df_new['vec_s'][j])
        cos.append(result)

#dict = {'sentence_a': word_a,'vec_a': vec_a,'sentence_b': word_b,'vec_b': vec_b,'cosine': cos}
dict = {'sentence_a': word_a,'sentence_b': word_b,'cosine': cos}
df_all = pd.DataFrame(dict)
df_all.to_csv('./dataset/fine-tune_data/w2v_pm_cui_5K.csv',index=0)


#%%
#刪除標準集中存在的術語對
df1= pd.read_csv('./dataset/fine-tune_data/w2v_pm_cui_5K.csv')
print(df1.columns.values)
a1 = df1['sentence_a'].tolist()
b1 = df1['sentence_b'].tolist()


df= pd.read_csv('ans.csv')
print(df.columns.values)
a = df['pair1'].tolist()
b = df['pair2'].tolist()

cnt=0
lst_id=[]
for i  in range(len(a)):
    print(i,a[i],b[i])
    mask1 = df1["sentence_a"] == a[i]
    mask2 = df1["sentence_b"] == b[i]
    #print(df1[(mask1 & mask2)])
    index = df1[(mask1 & mask2)].index
    for idx in index:
        print(idx)
        lst_id.append(idx)
    print(" ")

print(len(lst_id))

df1.drop(lst_id, axis=0, inplace=True)

df1.to_csv('./dataset/fine-tune_data/w2v_pm_cui_5K_del.csv',index=0)







