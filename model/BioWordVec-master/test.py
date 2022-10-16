
#%% 
import pandas as pd
import pickle

from gensim.models import fasttext
from gensim.test.utils import datapath
#https://github.com/ncbi-nlp/BioSentVec/issues/12
#在入BioWordVec模型(paper)取得paper結果之向量
#%% 
model = fasttext.load_facebook_vectors(datapath("C:/Users/DSBDA Server1/Downloads/BioWordVec_PubMed_MIMICIII_d200.bin"))
print(model['testaaaabbxws'])
#model = FastText.load_fasttext_format('C:/Users/DSBDA Server1/Downloads/BioWordVec_PubMed_MIMICIII_d200.bin')


#%% 
doc_1=[]
vec_1=[]
doc_2=[]
vec_2=[]
cnt=0
df1= pd.read_csv('D:/tmp/ans.csv',encoding='ANSI')#pair_t2d_fin  pair_t2s_fin
word1 = df1['pair1'].tolist()
word2 = df1['pair2'].tolist()

for i in range(df1.shape[0]):
    try:
        doc_1.append(word1[i])
        vec_1.append(model[word1[i].lower()])
        doc_2.append(word2[i])
        vec_2.append(model[word2[i].lower()])
    except:
        cnt+=1
        print('NO',i)

print("找不到",cnt)
dict = {'doc_1':doc_1,'vec_1':vec_1,'doc_2':doc_2, 'vec_2':vec_2} 
df_pair = pd.DataFrame(dict) 
pickle.dump( df_pair, open( "bio_paper.p", "wb" ) )
# %%
