import os
import jieba
import numpy as np
import operator
from functools import reduce
import re
from gensim.models import Word2Vec
from gensim import corpora, models

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname), mode='r', encoding='utf-8'):
                line = line.strip()
                yield line

class MySentences4Word2Vec(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname),encoding='utf-8'):
                temList =  []
                for word in jieba.cut(line):
                    temList.append(word)
                yield temList


class getrequirement(object):
    def __init__(self, docData, suggestionData):
        self.docData = docData
        self.suggestionData = suggestionData

    def is_number(self, s):
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def splitSen(selfs,senDoc):
        docFile = str(senDoc).split('\n')
        sentences = docFile
        return sentences

    def splitSen4Word2Vec(self,senDoc):
        docFile = str(senDoc).split('\n')
        sentences = []
        for line in docFile:
            temList = []
            for word in jieba.cut(line):
                temList.append(word)
            if len(temList):
                sentences.append(temList)
        return sentences

    def requirementItemized(self):
        """
        将需求文档进行条目化
        :param docFile: 需求文档
        :return: result: 需求条目（list类型）
        """
        docFile = self.splitSen(self.docData)
        print(docFile)

        allItemList = []
        result = []
        for i in docFile:
            if len(i) != 0:
                pattern = re.compile('[0-9]+\.')
                match = pattern.findall(i)
                # if (")" in i or ";" in i or "；"in i or is_number(i[0])) and '()' not in i:
                if (")" in i or "）" in i or ";" in i or "；" in i or match) and '()' not in i and i not in allItemList:
                    allItemList.append(i)
        for i in allItemList:
            # if "a)" in i[:3] or "(a)" in i[:3] or "(1)" in i[:3] or "1)" in i[:3]:
            startNum = allItemList.index(i)
            if "a)" in i[:3] or "(a)" in i[:3]:
                temList1 = []
                startWord = 'a'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    startWord = chr(ord(startWord) + 1) + ")"
                    if startNum < len(allItemList) - 1:
                        startNum = startNum + 1
                        if startWord in allItemList[startNum]:
                            temList1.append(allItemList[startNum])
                    else:
                        if len(temList1) > 1:
                            result.append(temList1)
                        break
            elif "(1)" in i[:3] or "1)" in i[:3]:
                temList1 = []
                startWord = '1'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    startWord = str(int(startWord) + 1) + ")"
                    if startNum < len(allItemList) - 1:
                        startNum = startNum + 1
                        if startWord in allItemList[startNum]:
                            temList1.append(allItemList[startNum])
                    else:
                        if len(temList1) > 1:
                            result.append(temList1)
                        break
            elif "1." in i:
                temList1 = []
                startWord = '1'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    startWord = str(int(startWord) + 1) + "."
                    if startNum < len(allItemList)-1:
                        startNum = startNum + 1
                        if startWord in allItemList[startNum]:
                            temList1.append(allItemList[startNum])
                    else:
                        if len(temList1) > 1:
                            result.append(temList1)
                        break
        print(result)
        if len(result) == 0:
            return []
        temList2 = reduce(operator.add, result)
        ret_list = list(set(allItemList).difference(set(temList2)))
        for i in ret_list:
            temList = re.split('[;；]', i.strip())
            if len(temList) > 1 and len(temList[1]) and temList not in result:
                result.append(temList)
        return result


    def cos_sim(self, vector_a, vector_b):
        """
        计算两个向量之间的余弦相似度
        :param vector_a: 向量 a
        :param vector_b: 向量 b
        :return: sim
        """
        dist1 = float(np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))
        return dist1


    def check_contain_chinese(self,check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def list_dict(self,list_data):
        list_data = list(map(lambda x: {str(x[0]): x[1]}, list_data))
        dict_data = {}
        for i in list_data:
            key, = i
            value, = i.values()
            dict_data[key] = value
        return dict_data

    # ===============word2vec词向量+tfidf==================
    def sentenceByW2VTfidf(self,corpus_tfidf, token2id, sentenceList, model, embeddingSize):
        sentenceSet = []
        for i in range(len(sentenceList)):
            # 将所有词向量的woed2vec向量相加到句向量
            sentenceVector = np.zeros(embeddingSize)
            # 计算每个词向量的权重，并将词向量加到句向量
            sentence = sentenceList[i]
            sentence_tfidf = corpus_tfidf[i]
            dict_tfidf = self.list_dict(sentence_tfidf)
            for word in sentence:
                if word in model:
                    tifidf_weigth = dict_tfidf.get(str(token2id[word]))
                    if tifidf_weigth == None:
                        tifidf_weigth = 0.0
                    sentenceVector = np.add(sentenceVector, tifidf_weigth * model[word])
            sentenceVector = np.divide(sentenceVector, len(sentence))
            # 存储句向量
            sentenceSet.append(sentenceVector)
        return sentenceSet

    # ==============词向量求平均===================
    def sentenceByWordVectAvg(self, sentenceList, model, embeddingSize):
        sentenceSet = []
        for sentence in sentenceList:
            # 将所有词向量的woed2vec向量相加到句向量
            sentenceVector = np.zeros(embeddingSize)
            # 计算每个词向量的权重，并将词向量加到句向量
            for word in sentence:
                sentenceVector = np.add(sentenceVector, model[word])
            sentenceVector = np.divide(sentenceVector, len(sentence))
            # 存储句向量
            sentenceSet.append(sentenceVector)
        return sentenceSet

    # ==============词向量求平均SIF===================
    def sentenceByWVSIF(self, sentenceList, wordFreDict, model, embeddingSize):
        sentenceSet = []
        for sentence in sentenceList:
            # 将所有词向量的woed2vec向量相加到句向量
            sentenceVector = np.zeros(embeddingSize)
            # 计算每个词向量的权重，并将词向量加到句向量
            for word in sentence:
                sentenceVector = np.add(sentenceVector, 0.01 / (0.01 + wordFreDict[word]) *model[word])
            sentenceVector = np.divide(sentenceVector, len(sentence))
            # 存储句向量
            sentenceSet.append(sentenceVector)
        return sentenceSet

    def wordFrequency(self, sen4Word2vec):
        word_list = []
        for i in sen4Word2vec:
            temList = []
            for word in jieba.cut(i):
                isCh = self.check_contain_chinese(word)
                if isCh:
                    temList.append(word)
            word_list.append(temList)
        dictionary = corpora.Dictionary(word_list)
        corpus  = [dictionary.doc2bow(text) for text in word_list]
        token2id = dictionary.token2id
        return word_list,dictionary,corpus ,token2id

    def senVec(self, itemizeResult):
        """
        将需求条目向量化
        :param itemizeResult: 需求条目（list）
        :return: senDict: 需求条目向量（dict{需求条目：向量值}）
        """
        r = '[’!"#$%&\'()*+,-./:;；<=>?@[\\]^_`{|}~，→《》：]+'
        sen4Word2vec = []
        for i in itemizeResult:
            for j in i:
                sen4Word2vec.append(re.sub(r, ' ', j.replace("\t", "")))

        sentences = self.splitSen4Word2Vec(self.docData)
        for i in sentences:
            print(i)
        model = Word2Vec(sentences, size=300, window=10, min_count=1, workers=2)
        senDict = {}
        traindata,dictionary, corpus, token2id = self.wordFrequency(sen4Word2vec)
        print(token2id)
        tfidf = models.TfidfModel(corpus=corpus, dictionary=dictionary)
        corpus_tfidf = tfidf[corpus]
        # 词向量tfidf加权得到句向量
        sentence_vecs = self.sentenceByW2VTfidf(corpus_tfidf, token2id, traindata, model, 300)

        for i in range(len(sen4Word2vec)):
            senDict[sen4Word2vec[i]] = sentence_vecs[i]
        return senDict

    def suggestionVec(self):
        suggestionFile = str(self.suggestionData).split('\n')
        print(suggestionFile)
        sentences = self.splitSen4Word2Vec(self.docData)
        model = Word2Vec(sentences, size=300, window=10, min_count=1, workers=2)
        senDict = {}
        traindata,dictionary, corpus, token2id = self.wordFrequency(suggestionFile)
        tfidf = models.TfidfModel(corpus=corpus, dictionary=dictionary)
        corpus_tfidf = tfidf[corpus]
        # 词向量tfidf加权得到句向量
        sentence_vecs = self.sentenceByW2VTfidf(corpus_tfidf, token2id, traindata, model, 300)

        for i in range(len(suggestionFile)):
            senDict[suggestionFile[i]] = sentence_vecs[i]
        return senDict

    def GetRelatedRE_Sugg(self):
        result = self.requirementItemized()
        sentence_vecs = self.senVec(result)
        suggVecDic = self.suggestionVec()
        Result = []
        for (k, v) in sentence_vecs.items():
            for (k1, v1) in suggVecDic.items():
                if self.cos_sim(v, v1) > 0.999995 and (k != k1):
                    Result.append([k,k1])
        return Result
