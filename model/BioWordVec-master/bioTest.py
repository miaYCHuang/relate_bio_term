from gensim.models import FastText
import pandas as pd
from scipy import spatial
import pickle

def checkExist(data_name,num,type1,type2):#(data_name,type)
    model = FastText.load("./bio/pubmed/bio_"+data_name+"_"+num)
    #model = FastText.load("./bio/"+data_name+"/bio_"+data_name+"_meta")
    doc_1=[]
    vec_1=[]
    doc_2=[]
    vec_2=[]
    cnt=0
    df1= pd.read_csv('D:/tmp/pair_t2d_fin.csv',encoding='ANSI')#pair_t2d_fin  pair_t2s_fin
    word1 = df1[type1].tolist()
    word2 = df1[type2].tolist()

    for i in range(df1.shape[0]):
        try:
            doc_1.append(word1[i])
            vec_1.append(model.wv[word1[i].lower()])
            doc_2.append(word2[i])
            vec_2.append(model.wv[word2[i].lower()])
        except:
            cnt+=1
            print('NO',i)

    print("找不到",cnt)
    dict = {'doc_1':doc_1,'vec_1':vec_1,'doc_2':doc_2, 'vec_2':vec_2} 
    df_pair = pd.DataFrame(dict) 
    pickle.dump( df_pair, open( "./vector/bio_"+data_name+"_cui_t2d.p", "wb" ) )
    #pickle.dump( df_pair, open( "./vector/bio_"+data_name+"_word_t2s_"+num+".p", "wb" ) )

checkExist("all","meta",'cui_t','cui_d')

# lst=['1','2','3','4']
# for i in lst:
#     checkExist("all",i,'word_t','doctor_d')

# %%
from gensim.models import FastText
import numpy as np
       
lst_id =['1','2','3','4']
for gram in lst_id:
    
    print("gram:",gram)
    fileName = 'all'
  
    file = open( "D:/tmp/bio_"+fileName+"_word_"+gram+".p", "rb")
    #file = open( "D:/tmp/bio_"+fileName+"_cui.p", "rb")
    df = pickle.load(file)
    file.close()
    
    #lst = [0,2,17,37,38,54,66,70,77,78]
    lst = [37,38,54,66]
    for n in lst:
        #print(df.iloc[n])
        print(len(df['doc_1'][n].split()),df['doc_1'][n])
        print(len(df['doc_2'][n].split()),df['doc_2'][n])

        model_1 = FastText.load('./BioWordVec-master/bio/pubmed/bio_'+fileName+'_'+gram)    
        
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



# %%
fileName = "all"
file = open( "D:/tmp/bio_"+fileName+"_cui.p", "rb")

df = pickle.load(file)
file.close()

#lst = [0,2,17,37,38,54,66,70,77,78]
lst = [0,7,16]
for n in lst:
    #print(df.iloc[n])
    #print(len(df['doc_1'][n].split()),df['doc_1'][n])
    #print(len(df['doc_2'][n].split()),df['doc_2'][n])
       
    model_1 = FastText.load('./BioWordVec-master/bio/pubmed/bio_'+fileName+'_meta')  
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














# %%
#載術語
import pickle
file = open( "D:/tmp/bio_all_word_1.p", "rb")
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


map1=splitWord(df['doc_1'].tolist())
map2=splitWord(df['doc_2'].tolist())


#%%
#取向量平均
import numpy as np
from gensim.models import FastText
w2v_model_subj = FastText.load('./BioWordVec-master/bio/pubmed/bio_all_1') 

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
pickle.dump( df_new, open( "./bio_all_word_1_Vcom.p", "wb" ) )
#================








# %%
import pandas as pd
from gensim.models import FastText
import pickle
from scipy import spatial
from scipy.stats import spearmanr
df1= pd.read_csv('D:/tmp/term_word.csv')
t = df1['t'].tolist()
d = df1['d'].tolist()
s = df1['s'].tolist()

model = FastText.load('C:/Users/DSBDA Server1/Desktop/MA/BioWordVec-master/bio/pubmed/bio_all_3') 

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

pickle.dump( df_new, open( "./bio_all_3_50.p", "wb" ) )
# %%
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
df_all.to_csv('./bio_all_word_5K.csv',index=0)

# %%
