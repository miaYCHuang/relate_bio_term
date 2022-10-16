"""
Created on Tue May  3 14:18:49 2022

#https://ithelp.ithome.com.tw/articles/10266467
#https://waynestalk.com/python-scipy-spearman-correlation-coefficient/
@author: YC
"""
from nltk.util import ngrams
from collections import Counter
import pandas as pd
import pickle
from gensim.models.word2vec import Word2Vec
from nltk.util import ngrams
from collections import Counter
from gensim.models.word2vec import Word2Vec #version 4.1.2
import pandas as pd
from scipy import spatial
from scipy.stats import spearmanr
#%%
#---------------------------------
# bioWvec用
#['cases minority', 'minority today'] -> total_grams.append(s)
#---------------------------------

def ngram(name,num):

    
    
    total_grams=[]
    '''
    #PUBMED
    df1= pd.read_csv('100.csv')
    ICD10 = df1['ICD10'].tolist()
    for j in range(len(ICD10)):
        df = pd.read_csv('dataset/PM_new/stop_pre_asc_'+ICD10[j]+'.csv')
        col = df['stop_pre_asc_data'].tolist()
    
    
        for i in range(len(col)):
            tokenised = col[i].replace(". "," ").split( ) #['heart','disease','is','a','disease']
            # obtain all unigrams
            data_ngrams = ngrams(tokenised, num)
        
            for phrase in data_ngrams:
                s = ' '.join(list(phrase))
                total_grams.append(s)
        
    print('PM:',len(total_grams))
    '''
    
    
    
    '''
    df = pd.read_csv('./dataset/stop_pre_asc_com_wiki.csv')#wiki
    col = df['stop_pre_asc_data'].tolist()
    for i in range(len(col)):
        
        tokenised = col[i].replace(". "," ").split( ) #['heart','disease','is','a','disease']
        # obtain all unigrams
        
        data_ngrams = ngrams(tokenised, num)

        for phrase in data_ngrams:
            #print(phrase,type(phrase))
            s = ' '.join(list(phrase))
            total_grams.append(s)
            #print(s)
    print('wiki:',len(total_grams))


    '''
    df = pd.read_csv('./dataset/stop_pre_asc_com_drugs.csv')
    col = df['stop_pre_asc_data'].tolist()
    for i in range(len(col)):
        tokenised = col[i].replace(". "," ").split( ) #['heart','disease','is','a','disease']
        # obtain all unigrams
        data_ngrams = ngrams(tokenised, num)
        for phrase in data_ngrams:
            #print(phrase,type(phrase))
            s = ' '.join(list(phrase))
            total_grams.append(s)
            #print(s)
    print('drugs:',len(total_grams))
    


    dict = {'gram': total_grams}
    df_gram = pd.DataFrame(dict)
    df_gram.to_csv('./dataset/gram/'+name+'_'+str(num)+'-gram.csv',index=0)
 
 

    
#call
#ngram('drugs',4)#資料集 幾-gram

lst=[1,2,3,4]
for i in lst:
    ngram('drugs',i)


#%%
#---------------------------------
# word2vec(CBOW)
# 使用n-gram(1~4)
#格式為
#str1=[['heart'],['disease'],['is'],['a'],['disease']]
#str2=[['heart disease'],['disease is'],['is a'],['a disease']]
#str3=[['heart disease is'],['disease is a'],['is a disease']]
#---------------------------------




#df = pd.read_csv('./dataset/stop_pre_asc_com_wiki.csv')#wiki
df = pd.read_csv('./dataset/stop_pre_asc_com_drugs.csv')#drugs
col = df['stop_pre_asc_data'].tolist()
total_grams = []
for i in range(len(col)):
    
    tokenised = col[i].replace(". "," ").split( ) #['heart','disease','is','a','disease']
    # obtain all unigrams
    
    data_ngrams = ngrams(tokenised, 4)

    for phrase in data_ngrams:
        #print(phrase,type(phrase))
        s = ' '.join(list(phrase))
        total_grams.append([s])
        #print(s)
print('筆數',len(total_grams))



#模型
corpus = total_grams
vector = 200
w = 8 #句子中當前詞和預測詞之間的最大距離。
min_count = 0 #忽略總頻率低於此的所有單詞
cbow = 0
skipGram = 1
iterations = 5   #訓練回數
worker = 4

model = Word2Vec(corpus, vector_size = vector, window = w, min_count = min_count, sg = cbow, workers = worker, epochs = iterations)

#model.save('./result/w2v/wiki/w2v_wiki_4.model')
model.save('./result/w2v/drugs/w2v_drugs_4.model')
print(model)

'''
#PM用39跑
def grams(num):

    total_grams = []
    df1= pd.read_csv('D:/tmp/100.csv')
    ICD10 = df1['ICD10'].tolist()
    for j in range(len(ICD10)):

        df = pd.read_csv('D:/tmp/PM_word/stop_pre_asc_'+ICD10[j]+'.csv')
        col = df['stop_pre_asc_data'].tolist()
        for i in range(len(col)):
            tokenised = col[i].split( ) #['heart','disease','is','a','disease']
            # obtain all unigrams
            data_ngrams = ngrams(tokenised, num)

            for phrase in data_ngrams:
                print(phrase,type(phrase))
                s = ' '.join(list(phrase))
                total_grams.append([s])

    print(len(total_grams))



    #模型
    corpus = total_grams
    vector = 200
    w = 8 #句子中當前詞和預測詞之間的最大距離。
    min_count = 0 #忽略總頻率低於此的所有單詞
    cbow = 0
    skipGram = 1
    iterations = 5   #訓練回數
    worker = 4

    model_x = Word2Vec(corpus, vector_size = vector, window = w, min_count = min_count, sg = cbow, workers = worker, epochs = iterations)
    #model_x.save('./result/w2v_e11_uni.model')
    model_x.save('w2v_PM_'+str(num)+'.model')

lst=[1,3,4]
for i in lst:
    grams(i)
'''


#%%
#METAMAP
#不使用n-gram
from nltk.util import ngrams
from gensim.models.word2vec import Word2Vec #version 4.1.2
import pandas as pd


total_grams=[]

 
#D跟W去逗號



f = open('./Meta/CUI/cui_wiki.txt')

for line in f.readlines():
    if line.strip()!='':  
        strings = line.strip().split(',')
        strings.remove('')
        #print(strings)
        total_grams.append(strings)
f.close

f = open('./Meta/CUI/cui_drugs.txt')

for line in f.readlines():
    if line.strip()!='':  
        strings = line.strip().split(',')
        strings.remove('')
        #print(strings)
        total_grams.append(strings)
f.close

#PM去空格
f = open('./Meta/CUI/cui_pubmed.txt')
for line in f.readlines():
    lst_strings = line.strip().split(' ')
    total_grams.append(lst_strings)



print('筆數',len(total_grams))
#模型
corpus = total_grams
vector = 200
w = 8 #句子中當前詞和預測詞之間的最大距離。
min_count = 0 #忽略總頻率低於此的所有單詞
cbow = 0
skipGram = 1
iterations = 5   #訓練回數
worker = 4#官方預設

model = Word2Vec(corpus, vector_size = vector, window = w, min_count = min_count, sg = cbow, workers = worker, epochs = iterations)

#model.save('./result/w2v/wiki/w2v_wiki_meta.model')
#model.save('./result/w2v/drugs/w2v_drugs_meta.model')
#model.save('./result/w2v/pubmed/w2v_pubmed_meta.model')
model.save('./result/w2v/all/w2v_all_meta.model')
print(model)
















#%%
#---------------------------------
# 載入word2vec model
# 計算pair的cos
# spearmanr -> 醫生標記 vs cos
#---------------------------------

from scipy import spatial

#model = Word2Vec.load('./result/w2v_e11_uni&bi.model')
model = Word2Vec.load('./result/w2v/wiki/w2v_wiki_2.model')
'''
for index, word in enumerate(model.wv.index_to_key):
    print(f'word #{index}/{len(model.wv.index_to_key)} = {word}')
''' 

df_pair = pd.read_csv('t.csv')
pair1 = df_pair['pair1'].tolist()
pair2 = df_pair['pair2'].tolist()

lst_cos=[]
lst_abscos=[]
for i in range(len(pair1)):
    
    '''
    #向量合併
    string1 = pair1[i].strip().lower()
    lst1 = string1.split(" ")
    string2 = pair2[i].strip().lower()
    lst2 = string2.split(" ")
    

    vec_A = (model.wv[lst1[0].strip().lower()] + model.wv[lst1[1].strip().lower()])/2
    vec_B = (model.wv[lst2[0].strip().lower()] + model.wv[lst2[1].strip().lower()])/2
    result = 1 - spatial.distance.cosine(vec_A, vec_B)
    lst_cos.append(result)
    lst_abscos.append(abs(result))
    print(pair1[i]," vs ",pair2[i],' : ',result)
    '''
    

    
    
    #向量
    vec_A = model.wv[pair1[i].strip().lower()]
    vec_B = model.wv[pair2[i].strip().lower()]
    #cos
    result = 1 - spatial.distance.cosine(vec_A, vec_B)
    lst_cos.append(result)
    lst_abscos.append(abs(result))
    print(pair1[i]," vs ",pair2[i],' : ',result)


df = df_pair.assign(cosine_e11_unibi_1 = lst_cos)#增加在原本後面
#df.to_csv('t.csv',index=0)
print(df)



#計算spearmanr

print(lst_abscos)
y = [1,1,1,1,1,0]
correlation, p = spearmanr(lst_abscos, y)
print('Correlation:', correlation)
    
correlation, p = spearmanr(lst_cos, y)
print('Correlation:', correlation)
    
    

#%%
from gensim.models.word2vec import Word2Vec
#total_grams=[['C0041260'],['C0011849'],['C0011860']]


#model = Word2Vec.load('./result/w2v/drugs/w2v_drugs_meta.model')
model = Word2Vec.load('./result/w2v/pubmed/w2v_pubmed_meta.model')

#查看model裡的詞
for index, word in enumerate(model.wv.index_to_key):
    if index == 10:
        break
    print(f'word #{index} / {len(model.wv.index_to_key)} is {word}')



vec_A = model.wv['C0009555']

#print(vec_A)



#%%
#檢查該CUI是否在模型中(向量)

import pickle

model = Word2Vec.load('./result/w2v/wiki/w2v_wiki_meta.model')
#model = Word2Vec.load('./result/w2v/drugs/w2v_drugs_meta.model')
#model = Word2Vec.load('./result/w2v/pubmed/w2v_pubmed_meta.model')
#model = Word2Vec.load('./result/w2v/all/w2v_all_meta.model')

df1= pd.read_csv('doctor_t2d.csv')
CUI = df1['cui_d_wiki'].tolist()#cui_t_drugs

CUI = list(set(CUI))
#CUI = ['C0005684','C1269683','C0853697']
cnt=0
vec=[]
for i in range(len(CUI)):
    try:
        vec.append(model.wv[CUI[i]])
    except:
        cnt+=1
        vec.append("")
        print('NO',CUI[i])
print(cnt,"個找不到")      
dict = {'CUI': CUI,'vector': vec}
df_cui = pd.DataFrame(dict)
print(df_cui)
pickle.dump( df_cui, open( "./vector/vec_w2v_wiki_cui_d.p", "wb" ) )

#  跑 -> #組成標準集對數











#%%
#計算標準集去重複後有多少對
df= pd.read_csv('temp_reD.csv',encoding='ANSI')#pair_t2d_fin
df1 = pd.DataFrame({'pair1_t':list(set(df['pair1_t']))})
df2 = pd.DataFrame({'pair1_d':list(set(df['pair1_d']))})
df3 = pd.DataFrame({'pair2_t':list(set(df['pair2_t']))})
df4 = pd.DataFrame({'pair2_s':list(set(df['pair2_s']))})

print(len(list(set(df['pair1_t']))))
print(len(list(set(df['pair1_d']))))
print(len(list(set(df['pair2_t']))))
print(len(list(set(df['pair2_s']))))

df_new=pd.concat([df1,df2,df3,df4], ignore_index=True, axis=1)#長度不齊補0
df_new.to_csv('./doctor.csv',index=0)
#加工對應值doctor_t2s doctor_t2d
#%%
df= pd.read_csv('doctor_t2d.csv')

'''
#%%
#確認最長為多少

df1= pd.read_csv('doctor_t2d.csv',encoding='ANSI')#pair_t2d_fin
word = df1['word_t_wiki'].tolist()
#word_d_wiki     word_d_drugs
#word_t_wiki     word_t_drugs
#word_s_wiki     word_s_drugs
print(word)
max_length = 0;
for i in range(len(word)):

    lst_strings = word[i].strip().split(' ')
    print(lst_strings)    
    if len(lst_strings) > max_length : max_length=len(lst_strings)
print(max_length
'''

#%%
#確認最長為多少
import numpy as np

def isNaN(num):
    return num != num


map_w1=[]
map_w2=[]
map_w3=[]
map_w4=[]


df1= pd.read_csv('doctor_t2d.csv')#pair_t2d_fin
word = df1['word_d_drugs'].tolist()
cnt=0
for i in range(len(word)):
    if(isNaN(word[i]) == False):#col每行不同(去重複後)
        lst_strings = word[i].strip().split(' ')
        if len(lst_strings) == 1:
            string = ' '.join(lst_strings)
            map_w1.append(string)
        elif len(lst_strings) == 2:
            string = ' '.join(lst_strings)
            map_w2.append(string)
        elif len(lst_strings) == 3:
            string = ' '.join(lst_strings)
            map_w3.append(string)
        elif len(lst_strings) == 4:
            string = ' '.join(lst_strings)
            map_w4.append(string)

print(map_w1,len(map_w1))
print(map_w2,len(map_w2))
print(map_w3,len(map_w3))
print(map_w4,len(map_w4))

#總共50個
#%%
#檢查該文字是否在模型中(向量)
#各-gram存向量
#合併所有gram成一檔



def getVector(n):

        #model = Word2Vec.load('./result/w2v/wiki/w2v_wiki_'+n+'.model')
        model = Word2Vec.load('./result/w2v/drugs/w2v_drugs_'+n+'.model')
        #model = Word2Vec.load('./result/w2v/pubmed/w2v_PM_'+n+'.model')#IP:39
    
        cnt=0
        vec=[]
        if n=='1':
            print(map_w1,len(map_w1))
            for i in map_w1:
                try:
                    vec.append(model.wv[i.lower()])
                except:
                    cnt+=1
                    print('NO',i)
            return map_w1,vec
    
        elif n=='2':
            print(map_w2,len(map_w2))
            for i in map_w2:
                try:
                    vec.append(model.wv[i.lower()])
                except:
                    cnt+=1
                    print('NO',i)
            return map_w2,vec
    
        elif n=='3':
            print(map_w3,len(map_w3))
            for i in map_w3:
                try:
                    vec.append(model.wv[i.lower()])
                except:
                    cnt+=1
                    print('NO',i)
            return map_w3,vec
    
        elif n=='4':
            print(map_w4,len(map_w4))
            for i in map_w4:
                try:
                    vec.append(model.wv[i.lower()])
                except:
                    cnt+=1
                    print('NO',i)
            return map_w4,vec
        
        
lst=['1','2','3','4']#,'4'

all_txt=[]
all_vec=[]
for n in lst:
    tmp = getVector(n)
    
    for t in range(len(tmp[0])):
        all_txt.append(tmp[0][t])
        all_vec.append(tmp[1][t])
  

print(len(all_txt))
print(len(all_vec))

        #搜尋的字
dict = {'gram': all_txt,'vector': all_vec}
df_gram = pd.DataFrame(dict)

pickle.dump( df_gram, open( "./vector/vec_w2v_drugs_s.p", "wb" ) )


#%%
#================
#1-gram向量合併
#================

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


map1=splitWord(df['map_1'].tolist())
map2=splitWord(df['map_2'].tolist())


#%%
#取向量平均
import numpy as np

w2v_model_subj = Word2Vec.load('./result/w2v/wiki/w2v_wiki_1.model')

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


vectors1 = embedding_feats_subj(map1)
print(len(vectors1))
vectors2 = embedding_feats_subj(map2)
print(len(vectors2))

#檢查
# for i in range(100):
#     print(map1[i],map2[i])
   
df_new = df.assign(vec_com_1 = vectors1,  vec_com_2 = vectors2)#增加在原本後面
print(df_new,len(df_new))
pickle.dump( df_new, open( "./vector/ans/w2v_wiki_word_Vcom.p", "wb" ) )
#================




#%%
#向量檔合併
file = open( "./vector/vector_w2v_pubmed_t_1.p", "rb")
v1 = pickle.load(file)
file.close()
file = open( "./vector/vector_w2v_pubmed_t_2.p", "rb")
v2 = pickle.load(file)
file.close()
file = open( "./vector/vector_w2v_pubmed_t_3.p", "rb")
v3 = pickle.load(file)
file.close()
file = open( "./vector/vector_w2v_pubmed_t_4.p", "rb")
v4 = pickle.load(file)
file.close()

df = pd.concat([v1, v2,v3,v4], ignore_index = True, axis = 0)
pickle.dump( df, open( "./vector/vec_w2v_pubmed_word_t.p", "wb" ) )

#%%
#組成標準集對數
def LoadVector(file):
    file = open( "./vector/"+file+".p", "rb")
    backup_list = pickle.load(file)
    file.close()
    return backup_list

df= pd.read_csv('pair_t2d_fin.csv',encoding='ANSI')#pair_t2d_fin
# pair_d = df['word_s_pubmed'].tolist()
# pair_t = df['word_t'].tolist() #word_d_wiki
pair_d = df['cui_d_wiki'].tolist()
pair_t = df['cui_t_wiki'].tolist()

#d_vec = LoadVector('vec_w2v_drugs_s')
#t_vec = LoadVector('vec_w2v_drugs_t')
d_vec = LoadVector('vec_w2v_wiki_cui_d')
t_vec = LoadVector('vec_w2v_wiki_cui_t')

doc_d=[]
map_d=[]
vec_d=[]

doc_t=[]
map_t=[]
vec_t=[]
for i in range(df.shape[0]):


        
    match_d = d_vec.loc[ (pair_d[i]==d_vec['CUI']) ]#gram CUI
    if match_d.empty != True:
        if len(match_d.index) == 1 :
            mat_id=match_d.index[0]
            doc_d.append(df['doctor_d'][i])
            #doc_d.append(df['doctor_s'][i])
            map_d.append(d_vec['CUI'][mat_id])#gram
            vec_d.append(d_vec['vector'][mat_id])           
        else:
            print("匹配到大於1個",match_d)
    else:
        print("dNO",pair_d[i])
        
        
    match_t = t_vec.loc[ (pair_t[i]==t_vec['CUI']) ]#gram
    if match_t.empty != True:
        if len(match_t.index) == 1 :
            mat_id=match_t.index[0]
            doc_t.append(df['doctor_t'][i])
            map_t.append(t_vec['CUI'][mat_id])#gram
            vec_t.append(t_vec['vector'][mat_id])
        else:
            print("匹配到大於1個",match_t)
    else:
        print("tNO",pair_t[i])



print(len(doc_d),len(map_d),len(vec_d))
print(len(doc_t),len(map_t),len(vec_t))


dict = {'doc_t':doc_t,'map_t':map_t,'vec_t':vec_t, 'doc_d':doc_d,'map_d':map_d,'vec_d':vec_d} 
#dict = {'doc_t':doc_t,'map_t':map_t,'vec_t':vec_t, 'doc_s':doc_d,'map_s':map_d,'vec_s':vec_d} 
df_pair = pd.DataFrame(dict) 
pickle.dump( df_pair, open( "./vector/w2v_wiki_cui_t2d.p", "wb" ) )
    
'''
#%% 
#================
#bio
#1~4-gram向量合併
#================
#取標準集的 t d s
#分長度

import numpy as np

def isNaN(num):
    return num != num


map_w1=[]
map_w2=[]
map_w3=[]
map_w4=[]


df1= pd.read_csv('pair_t2d_fin.csv',encoding='ANSI')#pair_t2d_fin
word = df1['doctor_d'].tolist()#word_t
print(len(word))
word = list(set(word))
print(len(word))
cnt=0
for i in range(len(word)):
    if(isNaN(word[i]) == False):#col每行不同(去重複後)
        lst_strings = word[i].strip().split(' ')
        if len(lst_strings) == 1:
            string = ' '.join(lst_strings)
            map_w1.append(string)
        elif len(lst_strings) == 2:
            string = ' '.join(lst_strings)
            map_w2.append(string)
        elif len(lst_strings) == 3:
            string = ' '.join(lst_strings)
            map_w3.append(string)
        elif len(lst_strings) == 4:
            string = ' '.join(lst_strings)
            map_w4.append(string)
        else:
            print(lst_strings)
print(map_w1,len(map_w1))
print(map_w2,len(map_w2))
print(map_w3,len(map_w3))
print(map_w4,len(map_w4))

#%%

def LoadVector(file):
    file = open( "./vector/ans/"+file+".p", "rb")
    backup_list = pickle.load(file)
    file.close()
    return backup_list


lst_map=[]
lst_vec=[]

df_bio1 = LoadVector('bio_wiki_word_1')
for i in map_w1:
    for j in range(df_bio1.shape[0]):
        if i == df_bio1['doc_2'][j]:#doc_1
            lst_map.append(i)
            lst_vec.append(df_bio1['vec_2'][j])#vec_1
            print(i,"Y")
            break
print(len(lst_vec))
df_bio1 = LoadVector('bio_wiki_word_2')
for i in map_w2:
    for j in range(df_bio1.shape[0]):
        if i == df_bio1['doc_2'][j]:
            lst_map.append(i)
            lst_vec.append(df_bio1['vec_2'][j])
            print(i,"Y")
            break
print(len(lst_vec))        
df_bio1 = LoadVector('bio_wiki_word_3')
for i in map_w3:
    for j in range(df_bio1.shape[0]):
        if i == df_bio1['doc_2'][j]:
            lst_map.append(i)
            lst_vec.append(df_bio1['vec_2'][j])
            print(i,"Y")
            break
print(len(lst_vec))
df_bio1 = LoadVector('bio_wiki_word_4')
for i in map_w4:
    for j in range(df_bio1.shape[0]):
        if i == df_bio1['doc_2'][j]:
            lst_map.append(i)
            lst_vec.append(df_bio1['vec_2'][j])
            print(i,"Y")
            break
print(len(lst_vec))
dict = {'doc_1':lst_map,'vec_1':lst_vec} 
df_pair = pd.DataFrame(dict) 
pickle.dump( df_pair, open( "./vector/bio_wiki_d.p", "wb" ) )




'''





































#%% 
'''

#%% 
file = open( "./vector/w2v/w2v_all_word_t2s.p", "rb")

#file = open( "./vector/SBERT/sbert_drugs_word_t2d.p", "rb")
#file = open( "C://Users//YC//OneDrive - 國立中正大學//桌面//BioWordVec-master//bio//vector//bio_paper_t2s.p", "rb")
df_new = pickle.load(file)
file.close()

lst_cos=[]

for i in range(df_new.shape[0]):
    #result = 1 - spatial.distance.cosine(df_new['vec_1'][i], df_new['vec_2'][i])
    result = 1 - spatial.distance.cosine(df_new['vec_t'][i], df_new['vec_s'][i])
    lst_cos.append(result)

df1= pd.read_csv('ts_ans.csv')
y = df1['mean'].tolist()

correlation, p = spearmanr(lst_cos, y)#cosine
print('Correlation:', correlation)


#%% 
#WORD
#檢查並計算COS


def Normalization(x):
    return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]

#file = open( "./vector/w2v/wiki_word_t2d.p", "rb")
#file = open( "./vector/w2v/wiki_word_t2s.p", "rb")
#file = open( "./vector/w2v/drugs_word_t2d.p", "rb")
#file = open( "./vector/w2v/drugs_word_t2s.p", "rb")
#file = open( "./vector/w2v/w2v_all_word_t2d.p", "rb")
file = open( "C:/Users/YC/OneDrive - 國立中正大學/桌面/BioWordVec-master/bio/vector/bio_paper_t2d.p", "rb")
df_t2d = pickle.load(file)
file.close()
print(len(df_t2d))



#檢查向量是否正確

print(df_t2d.iloc[48])
#model1 = Word2Vec.load('./result/w2v/wiki/w2v_wiki_1.model')
model1 = Word2Vec.load('./result/w2v/drugs/w2v_drugs_1.model')
print(model1.wv[df_t2d['disease'][48].lower()])#disease  test
print(model1.wv[df_t2d['test'][48].lower()])#disease  
print("***********************")
print(df_t2d['vec_d'][48])#vec_d vec_t
print(df_t2d['vec_t'][48])#vec_d 



lst_cos=[]

for i in range(df_t2d.shape[0]):
    result = 1 - spatial.distance.cosine(df_t2d['vec_1'][i], df_t2d['vec_2'][i])
    #result = 1 - spatial.distance.cosine(df_t2d['vec_d'][i], df_t2d['vec_t'][i])
    #result = 1 - spatial.distance.cosine(df_t2d['vec_s'][i], df_t2d['vec_t'][i])
    lst_cos.append(result)


df_new = df_t2d.assign(cosine = lst_cos,  cosine_Std = Normalization(lst_cos))#增加在原本後面  cos 歸一化(cos)
print(df_new,len(df_new))

#pickle.dump( df_new, open( "./vector/w2v/drugs_word_t2s"+"_cos.p", "wb" ) )



df1= pd.read_csv('temp_reD.csv')
y = df1['mean'].tolist()

correlation, p = spearmanr(df_new['cosine'], y)#cosine
print('Correlation:', correlation)

correlation, p = spearmanr(df_new['cosine_Std'], y)#cosine
print('Correlation_std:', correlation)

#%%
#CUI
#檢查並計算COS
from scipy import spatial

lst_empty=[]


def Normalization(x):
    return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]
file = open( "C:/Users/YC/OneDrive - 國立中正大學/桌面/BioWordVec-master/bio/vector/bio_all_cui_t2s.p", "rb")
#file = open( "./vector/w2v/w2v_all_cui_t2s.p", "rb")
df_t2d = pickle.load(file)
file.close()
print(len(df_t2d))

lst_empty = df_t2d.index[(df_t2d[ "vec_1" ] == "" ) | (df_t2d[ "vec_2" ] == "" )]
#lst_empty = df_t2d.index[(df_t2d[ "vec_t" ] == "" ) | (df_t2d[ "vec_s" ] == "" )]
print(list(set(lst_empty)))#去重複


#只用於CUI  WIKI DRUG
df_t2d.drop(lst_empty,axis= 0 ,inplace= True )#刪除不存在VEC的
df_t2d = df_t2d.reset_index(drop= True)#重置index
print(len(df_t2d))


lst_cos=[]

for i in range(df_t2d.shape[0]):
    result = 1 - spatial.distance.cosine(df_t2d['vec_1'][i], df_t2d['vec_2'][i])
    #result = 1 - spatial.distance.cosine(df_t2d['vec_t'][i], df_t2d['vec_s'][i])
    lst_cos.append(result)

print(len(lst_cos))
# df_new = df_t2d.assign(cosine = lst_cos,  cosine_Std = Normalization(lst_cos))#增加在原本後面  cos 歸一化(cos)
# print(df_new,len(df_new))

#pickle.dump( df_new, open( "./vector/w2v/drugs_word_t2s"+"_cos.p", "wb" ) )



df1= pd.read_csv('ts_ans.csv')
df1.drop(lst_empty,axis= 0 ,inplace= True )#刪除不存在VEC的
y = df1['mean'].tolist()


correlation, p = spearmanr(lst_cos, y)#cosine
print('Correlation:', correlation)

'''






#%%

file = open( "./vector/w2v/w2v_wiki_word_t2d.p", "rb")
df_t2d = pickle.load(file)
file.close()
print(len(df_t2d))
#df_t2d.to_csv('./vector/w2v/t.csv',index=0)

#%%
#計算spearmanr
from scipy.stats import spearmanr

file = open( "./vector/w2v/w2v_wiki_word_t2d.p", "rb")
df_t2d = pickle.load(file)
file.close()

print(df_t2d)


y = [i for i in range(50)]
correlation, p = spearmanr(df_t2d['cosine_Std'], y)#cosine
print('Correlation:', correlation)







'''
#%%
#---------------------------------
# word2vec model的fine-tune資料
# 文本
# IP:39
#---------------------------------

#取得所有術語集(標準集裡的術語)
df= pd.read_csv('term.csv')
lst_title= list(df.columns.values)
print(lst_title)
print(df.shape[0])

all_term=[]

for row in lst_title:

    col_data = df[row].tolist()
    for term in col_data:
        all_term.append(term)
print(len(all_term))
all_term = list(set(all_term))
print(len(all_term))

#%%
#語料庫資料斷句
import re
data=[]

def replaceDot(col):
    lst_new=[]
    for row in range(len(col)):
      DotRegex = re.compile(r'[a-zA-Z0-9]+\.[a-zA-Z0-9]+')#句號以外的點
      result = DotRegex.findall(col[row])
    
      String1= col[row]
      
      if result:
          #print(row)
          for rem in result:
              #print(rem)
              String1 = String1.replace(rem,rem.replace('.','**'))#句號以外的點轉換成**
              #print(String1)
      lst_new.append(String1)
    return lst_new


df1= pd.read_csv('./dataset/asc_com_wiki.csv')
col = df1['asc_data'].tolist()
lst = replaceDot(col)
for row in range(len(lst)):
  text = lst[row].split('.')#斷句
  if ' ' in text : text.remove(' ')
  for txt in text:
      data.append(txt.replace('**','.'))#句號以外的點 取代回去
print(len(data))

df1= pd.read_csv('./dataset/asc_com_drugs.csv')
col = df1['asc_data'].tolist()
lst = replaceDot(col)
for row in range(len(lst)):
  text = lst[row].split('.')#斷句
  if ' ' in text : text.remove(' ')
  for txt in text:
      data.append(txt.replace('**','.'))#句號以外的點 取代回去
print(len(data))



# Pubmed data
def loadPM(n):
    df1= pd.read_csv('./dataset/PM_new/ASCII/asc_'+n+'.csv')
    col = df1['asc_data'].tolist()
    return replaceDot(col)

df1= pd.read_csv('100.csv')
ICD10 = df1['ICD10'].tolist()
for j in range(len(ICD10)):

    lst = loadPM(ICD10[j])
    for row in range(len(lst)):
      text = lst[row].split('.')#斷句
      if ' ' in text : text.remove(' ')
      for txt in text:
          data.append(txt.replace('**','.'))#句號以外的點 取代回去


print(len(data))
#%%
#斷句後資料選出含有術語的句子
new_data=[]
for sentence in data:    
    for term in all_term:
        if term in sentence:
            new_data.append(sentence)
            break
print(len(new_data))
#%%
#斷字
data_Subj = []
for i in range(len(new_data)):
    
    d = [x for x in new_data[i].split(' ') if x] #斷字&去空格
    if len(d) > 10: #句子太短不加入
        data_Subj.append(d) 
        
print(len(data_Subj))   
#%%
#w2v平均向量->作為句子向量
import numpy as np
w2v_model_subj = Word2Vec.load('./result/w2v/wiki/w2v_wiki_1.model')

def embedding_feats_subj(list_of_lists):
    DIMENSION = 200
    zero_vector = np.zeros(DIMENSION)
    feats = []
    for tokens in list_of_lists:
        feat_for_this =  np.zeros(DIMENSION)
        count_for_this = 0 + 1e-5 # to avoid divide-by-zero 
        for token in tokens:
            if token in w2v_model_subj.wv:
                feat_for_this += w2v_model_subj.wv[token]
                count_for_this +=1
        if(count_for_this!=0):
            feats.append(feat_for_this/count_for_this) 
        else:
            print(tokens)
            feats.append(zero_vector)
    return feats


vectors = embedding_feats_subj(data_Subj)
print(len(vectors))


sentence=[]
for i in data_Subj:
    sentence.append(' '.join(i))#合併回去
print(len(sentence))

dict = {'sentence': sentence,'vector': vectors}
df_w2v = pd.DataFrame(dict)
#%%
print(df_w2v.shape[0])

import random

txt_a=[]
txt_b=[]
total=[]

cosine=[]
n=1000000#抽樣筆數100W
for ron in range(n):#跑n組pair
    pair = random.sample(range(0,df_w2v.shape[0]),2)#隨機取兩數 len(docvec_all_index)
    #print(pair)
    #print(df['vector'][pair[0]])

    result = 1 - spatial.distance.cosine(df_w2v['vector'][pair[0]], df_w2v['vector'][pair[1]])
    cosine.append(result)
    txt_a.append(df_w2v['sentence'][pair[0]])
    txt_b.append(df_w2v['sentence'][pair[1]])

df_new = pd.DataFrame( (zip(txt_a,txt_b,cosine)) , columns = ['sentence_a','sentence_b','cosine'])
print(df_new)
df_new.to_csv('./result/d2v/w2v_all_100W.csv',index=0)


'''




#%% 篩選
#看一下分布
#df_new= pd.read_csv('./dataset/fine-tune_data/w2v_all_100W.csv')
file = open( "./dataset/fine-tune_data/bio_all_100W.p", "rb")
df_new = pickle.load(file)
file.close()

# def Normalization(x):
#     return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]

# cos=df_new['cosine'].tolist()
# print(cos)
# print(len(Normalization(cos)))
# df_new2 = df_new.assign( cosine_Std = Normalization(cos))#增加在原本後面  cos 歸一化(cos)


score_veryH = df_new.loc[ df_new['cosine'] >= 0.8 ]
score_H = df_new.loc[ (df_new['cosine']  < 0.8) & (df_new['cosine'] >= 0.6) ]
score_N = df_new.loc[ (df_new['cosine']  < 0.6) & (df_new['cosine'] >= 0.4) ]
score_L = df_new.loc[ (df_new['cosine']  < 0.4) & (df_new['cosine'] >= 0.2) ]
score_veryL = df_new.loc[ (df_new['cosine']  < 0.2) & (df_new['cosine'] >= 0.0) ]
print(len(score_veryH))
print(len(score_H))
print(len(score_N))
print(len(score_L))
print(len(score_veryL))

#重設index
score_veryH.reset_index(drop=True, inplace=True)
score_H.reset_index(drop=True, inplace=True)
score_N.reset_index(drop=True, inplace=True)
score_L.reset_index(drop=True, inplace=True)
score_veryL.reset_index(drop=True, inplace=True)

#%% 分等級取樣
import random

def randomNUM(df,num):
    rdm = random.sample(range(0,len(df)),num)
    return rdm

score_veryH_n = score_veryH.loc[randomNUM(score_veryH,5000)]
score_H_n = score_H.loc[randomNUM(score_H,5000)]
score_N_n = score_N.loc[randomNUM(score_N,4859)]
#score_L_n = score_L.loc[randomNUM(score_L,5000)]
#score_veryL_n = score_veryL.loc[randomNUM(score_veryL,5000)]
#score_veryL_n = score_veryL.loc[randomNUM(score_veryL,len(score_veryH))]

df_com = pd.concat([score_veryH_n  ,score_H_n  ,score_N_n , score_L  ,score_veryL],axis=0, ignore_index=True)

#%%
df_com.to_csv('./result/d2v/bio_all_5000.csv',index=0) #doc2vec_sim_avg
#%%
import os 
import pandas, numpy
import openpyxl

score_H = df_new.loc[ (df_new['cosine_Std'] >= 0.6) ]#高度相關
score_N = df_new.loc[ (df_new['cosine_Std']  < 0.6) & (df_new['cosine_Std'] >= 0.4) ]#中度相關
score_L = df_new.loc[ (df_new['cosine_Std']  < 0.4) & (df_new['cosine_Std'] >= 0.2) ]#低度相關
score_veryL = df_new.loc[ (df_new['cosine_Std']  < 0.2) & (df_new['cosine_Std'] >= 0.0) ]#不相關
print(len(score_H))
print(len(score_N))
print(len(score_L))
print(len(score_veryL))

score_H=score_H.sort_values(by=['cosine_Std'], ascending=False)#排序高-低
score_N=score_N.sort_values(by=['cosine_Std'], ascending=False)
score_L=score_L.sort_values(by=['cosine_Std'], ascending=False)
score_veryL=score_veryL.sort_values(by=['cosine_Std'], ascending=False)

# 開一個新的excel並把多個df寫到同excel不同sheet
path = os.path.join(os.getcwd(), './vector/w2v/test2disease_class.xlsx') # 設定路徑及檔名
writer = pandas.ExcelWriter(path, engine='openpyxl') # 指定引擎openpyxl

score_H.to_excel(writer, sheet_name='strong') # 存到指定的sheet
score_N.to_excel(writer, sheet_name='moderate') # 存到指定的sheet
score_L.to_excel(writer, sheet_name='weak') # 存到指定的sheet
score_veryL.to_excel(writer, sheet_name='very weak') # 存到指定的sheet

writer.save() # 存檔生成excel檔案
#writer.close()




