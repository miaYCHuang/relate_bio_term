# 文件說明
 
## 前處理
#### 文字部分
-  Preprocessing_wiki.py
- Preprocessing_drugs.py
(DT:以ICD疾病(D)找到的檢驗(T)；ab:摘要；DS：以ICD疾病(D)找到的症狀(S))
-  Preprocessing_PM_web.py
因為有些pubmed.ows會出現錯誤因此從網頁下載，再進行前處理
-  Preprocessing_PM_orange.py
Orange爬到的資料進行前處理
-  Preprocessing_pubmed.py
全部再一起做一次前處理，取5K筆
-  preprocessing.py
asc_處理亂碼後；pre_asc_處理亂碼後前處理；stop_pre_asc_處理亂碼後前處理後刪停用詞


#### CUI部分
- metamap.py
CountMeta:找出症狀高頻詞；findAllMeta
- preprocessing_Meta.py 
com2data合併兩個資料



## 模型
-  w2v.py
資料分n-gram後建模

- BioWordVec.py
- bioTest.py
將模型資料存成pickle檔
- test.py
取得BioWordVec paper模型資料(與本研究比較)

- Bert_label_train.ipynb
包含Bert、SBERT、PubmedBERT模型微調後的結果


- relate.py
計算相關性、圖表
- data_fineTune.py
產生微調資料
- ans_statistics.py
醫生標註之答案截尾平均

