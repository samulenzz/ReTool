# -*- coding: utf-8 -*-
# @Time : 2020/1/6 20:46
# @Author : ZacharyZhao
# @FileName: ReSuggRelate.py
# @Software: PyCharm

import jieba
from gensim import corpora, models
from gensim.similarities import Similarity

class getrequirement(object):
    def __init__(self, docData, suggestionData):
        self.docData = docData
        self.suggestionData = suggestionData

    def GetKeyword(self,sen,sugg_keywords):
        result = []
        for i in sugg_keywords:
            for j in i:
                if j in sen:
                    if sugg_keywords.index(i) == 0 and "添加" not in result:
                        result.append("添加")
                    elif sugg_keywords.index(i) == 1 and "删除" not in result:
                        result.append("删除")
                    elif sugg_keywords.index(i) == 2 and "修改" not in result:
                        result.append("修改")
                    elif sugg_keywords.index(i) == 3 and "合并" not in result:
                        result.append("合并")
                    elif sugg_keywords.index(i) == 4 and "分解" not in result:
                        result.append("分解")
        return result

    def GetRelatedRE_Sugg(self):
        Result = []
        corpora_documents = []
        for item_text in self.docData:
            item_str = jieba.lcut(item_text)
            corpora_documents.append(item_str)
        dictionary = corpora.Dictionary(corpora_documents)
        #  通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量）stopwords
        corpus = [dictionary.doc2bow(text) for text in corpora_documents]
        # 向量的每一个元素代表了一个word在这篇文档中出现的次数
        # 转化成tf-idf向量
        # corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
        tfidf_model = models.TfidfModel(corpus)
        corpus_tfidf = [tfidf_model[doc] for doc in corpus]
        print('语料的TFIDF向量', corpus_tfidf)
        ''''' 
        #查看model中的内容 
        for item in corpus_tfidf: 
            print(item) 
        # tfidf.save("data.tfidf") 
        # tfidf = models.TfidfModel.load("data.tfidf") 
        # print(tfidf_model.dfs) 
        '''
        # 转化成lsi向量
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
        corpus_lsi = [lsi[doc] for doc in corpus]
        print("语料的LSI：" + str(corpus_lsi))
        similarity_lsi = Similarity('Similarity-Lsi-index', corpus_lsi, num_features=400, num_best=5)
        #  1.测试数据
        # test_data_1 = '你好，我想问一下我想离婚他不想离，孩子他说不要，是六个月就自动生效离婚'
        for test_data_1 in self.suggestionData:
            test_cut_raw_1 = jieba.lcut(test_data_1)
            # 2.转换成bow向量 # [(51, 1), (59, 1)]，即在字典的52和60的地方出现重复的字段，这个值可能会变化
            test_corpus_3 = dictionary.doc2bow(test_cut_raw_1)
            # 3.计算tfidf值  # 根据之前训练生成的model，生成query的TFIDF值，然后进行相似度计算
            test_corpus_tfidf_3 = tfidf_model[test_corpus_3]
            #  4.计算lsi值
            test_corpus_lsi_3 = lsi[test_corpus_tfidf_3]
            #  返回最相似的样本材料,(index_of_document, similarity) tuples
            for i in similarity_lsi[test_corpus_lsi_3]:
                if i[1] >0.5:
                    # print(similarity_lsi[test_corpus_lsi_3].index(i))
                    Result.append([self.docData[i[0]],test_data_1])
                if similarity_lsi[test_corpus_lsi_3].index(i) > 4:
                    break
            # for i, item in enumerate(similarity_lsi[test_corpus_lsi_3]):
            #     if item[1] > 0.5:
            #         print(i)
            #         Result.append([self.docData[item[0]],test_data_1])
            #     if i > 4:
            #         break

            sugg_keywords = []
            sugg_keywords_file = open('core/Sugg_Keywords', 'r', encoding='utf-8').readlines()
            for i in sugg_keywords_file:
                temList = i.split(' ')
                sugg_keywords.append(temList)
            for i in range(len(Result)):
                Result[i].append(self.GetKeyword(Result[i][1], sugg_keywords))

        return Result