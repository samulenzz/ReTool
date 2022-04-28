import jieba
import re
import jieba.posseg as pseg
from gensim.models import Word2Vec
import os
import math
import synonyms

class MySentencesNotCut(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname),encoding='utf-8'):
                line = line.strip()
                yield line

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    # 清洗文本
    def cleanTxt(self,line):
        # 去标点
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~，→《》：]+'
        temstr = line.strip()
        temstr = re.sub(r, ' ', temstr)
        # 去数字
        r = '[abcdefghijklmnopgrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ]+'
        temstr = re.sub(r, '', temstr)
        temstr = temstr.strip()
        return temstr
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            print(fname)
            for line in open(os.path.join(self.dirname,fname),encoding='utf-8'):
                line = self.cleanTxt(line)
                if len(line):
                    yield [word for word in jieba.cut(line)]


class chSyn(object):
    def __init__(self,filePath):
        self.filePath = filePath

    # 写文件
    def write_file(self,handle, MWT):
        handle.write(MWT)

    # 清洗文本
    def cleanTxt(self,line):
        # 去标点
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~，→《》：]+'
        temstr = line.strip()
        temstr = re.sub(r, ' ', temstr)
        # 去数字
        r = '[abcdefghijklmnopgrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ]+'
        temstr = re.sub(r, '', temstr)
        temstr = temstr.strip()
        return temstr

    # 获取MWT
    def getMWT(self,lineList):
        MWTLIST = []
        for i in lineList:
            sentenceSplitList = [word for word in pseg.cut(i)]
            for j in sentenceSplitList:
                NNWordNum = sentenceSplitList.index(j)
                MWT = []
                if j.flag == 'vn' or j.flag == 'n':
                    MWT.append([j.word, j.flag])
                for m in range(1, 5):
                    if NNWordNum + m < len(sentenceSplitList):
                        if "n" in sentenceSplitList[NNWordNum + m].flag or "vn" in sentenceSplitList[
                            NNWordNum + m].flag:
                            MWT.append([sentenceSplitList[NNWordNum + m].word, sentenceSplitList[NNWordNum + m].flag])
                        else:
                            break
                for _ in MWT:
                    if len(MWT) > 0 and (MWT[-1][1] == "v" or MWT[-1][1] == "vn"):
                        pass
                    else:
                        MWTLIST.append(MWT)
        return MWTLIST

    # 计算词频
    def getMWTFrequency(self,MWTList):
        newMWTList = []
        countMWtList = []
        for i in MWTList:
            temlist = []
            for j in i:
                temlist.append(j[0])
            newMWTList.append(" ".join(temlist))
        setMWTList = set(newMWTList)
        for item in setMWTList:
            temList = [item, newMWTList.count(item)]
            countMWtList.append(temList)
        return countMWtList

    # 计算c_value
    def caCvalue(self,countMWtList):
        cVlaueList = []
        for i in countMWtList:
            nestedList = []
            nestedList.append(i)
            for j in countMWtList:
                if i[0] in j[0] and i[0] != j[0]:
                    if j in nestedList:
                        continue
                    nestedList.append(j)
            if len(nestedList) == 1:
                # log2|t|*f(t)
                c_value = math.log(len(i[0].split(" ")), 2) * nestedList[0][1]
            else:
                # log2|t|*(f(t)-1/|Ct|*freSum)
                freSum = 0
                for n in nestedList:
                    # freSum全部词的词频之和
                    freSum = freSum + n[1]
                c_value = math.log(len(i[0].split(" ")), 2) * (nestedList[0][1] - (1 / len(nestedList) * freSum))
            if c_value > 2:
                cVlaueList.append(i)
                print(i, c_value)
        return cVlaueList

    # 过滤无用MWT
    def clusterMWT(self,MWTLIST):
        new_MWTLIST = []
        for i in MWTLIST:
            flag = 0
            for j in i:
                if "用户" in j or "设置" in j or "选择" in j or "输入" in j or "到" in j or \
                        "时" in j or "解析" in j or "将" in j or "采用" in j or "选项" in j or \
                        "包括" in j or "放大" in j or "拖动" in j or "放入" in j or "缩小" in j or \
                        "菜单中选择" in j or "关闭" in j or "保存" in j or "返回" in j or "会" in j or \
                        "弹出" in j or "使用" in j or "按住" in j or "不" in j or "具有" in j or \
                        "方式" in j or "点击" in j or "作为" in j or "已" in j or "需" in j or \
                        "想" in j or "显示" in j or "地" in j or "切换" in j or "完成" in j or \
                        "编辑" in j or "分别" in j or "是" in j or "方" in j or "读取" in j or \
                        "自动" in j or "包含" in j or "需要" in j or "人员" in j or "删除" in j or \
                        "进行" in j or "是否" in j or "一旦" in j or "时刻" in j or "全部" in j or \
                        "子" in j or "双手" in j or "指" in j:
                    flag = 1
                    break
            if flag == 0:
                new_MWTLIST.append(i)
        return new_MWTLIST

    # 第一种同义词抽取方法
    def fistSynonymousMethod(self,CValueList, Sthreshold,model):
        result = []
        for i in CValueList:
            iList = i[0].split(" ")
            for j in CValueList:
                jList = j[0].split(" ")
                if len(iList) > 1 and len(jList) > 1:
                    if len(iList) == 2 and len(jList) == 2:
                        if iList[0] == jList[0] and iList[1] != jList[1] and iList[1] in model and jList[1] in model:
                            similarity = model.similarity(iList[1].strip(), jList[1].strip())
                            if similarity > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        if iList[1] == jList[1] and iList[0] != jList[0] and iList[0] in model and jList[0] in model:
                            similarity = model.similarity(iList[0].strip(), jList[0].strip())
                            if similarity > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                    # ----------------------------------------------------len=3,前两个词和后两个词相同的情况-----------------------------------------------------------#
                    if len(iList) == 3 and len(jList) == 3:
                        if iList[0] == jList[0] and iList[1] == jList[1] and iList[2] != jList[2] and iList[
                            2] in model and jList[2] in model:
                            similarity = model.similarity(iList[2].strip(), jList[2].strip())
                            if similarity > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        if iList[1] == jList[1] and iList[2] == jList[2] and iList[0] != jList[0] and iList[
                            0] in model and jList[0] in model:
                            similarity = model.similarity(iList[0].strip(), jList[0].strip())
                            if similarity > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=3，第一个词或最后一个词相同----------------------------------------------------------#
                        if iList[0] == jList[0] and iList[1] != jList[1] and iList[2] != jList[2] and iList[
                            1] in model and jList[1] in model and iList[2] in model and jList[2] in model:
                            similarity1 = model.similarity(iList[1].strip(), jList[1].strip())
                            similarity2 = model.similarity(iList[2].strip(), jList[2].strip())
                            if similarity1 > Sthreshold and similarity2 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity1, ',', similarity2)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        if iList[2] == jList[2] and iList[0] != jList[0] and iList[1] != jList[1] and iList[
                            0] in model and jList[0] in model and iList[1] in model and jList[1] in model:
                            similarity1 = model.similarity(iList[0].strip(), jList[0].strip())
                            similarity2 = model.similarity(iList[1].strip(), jList[1].strip())
                            if similarity1 > Sthreshold and similarity2 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity1, ',', similarity2)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=3，第一个词和最后一个词相同----------------------------------------------------------#
                        if iList[0] == jList[0] and iList[2] == jList[2] and iList[1] != jList[1] and iList[
                            1] in model and jList[1] in model:
                            similarity = model.similarity(iList[1].strip(), jList[1].strip())
                            if similarity > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                    # -----------------------------------------------------len=4----------------------------------------------------------#
                    if len(iList) == 4 and len(jList) == 4:
                        # -----------------------------------------------------len=4，第一个词相同----------------------------------------------------------#
                        if iList[0] == jList[0] and iList[1] != jList[1] and iList[2] != jList[2] and iList[3] != jList[
                            3] \
                                and iList[1] in model and jList[1] in model and iList[2] in model and jList[2] in model \
                                and iList[3] in model and jList[3] in model:
                            similarity1 = model.similarity(iList[1].strip(), jList[1].strip())
                            similarity2 = model.similarity(iList[2].strip(), jList[2].strip())
                            similarity3 = model.similarity(iList[3].strip(), jList[3].strip())
                            if similarity1 > Sthreshold and similarity2 > Sthreshold and similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity1, ',', similarity2, ',',
                                      similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=4，第一,二个词相同----------------------------------------------------------#
                        if iList[0] == jList[0] and iList[1] == jList[1] and iList[2] != jList[2] and iList[3] != jList[
                            3] \
                                and iList[2] in model and jList[2] in model and iList[3] in model and jList[3] in model:
                            similarity2 = model.similarity(iList[2].strip(), jList[2].strip())
                            similarity3 = model.similarity(iList[3].strip(), jList[3].strip())
                            if similarity2 > Sthreshold and similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity2, ',', similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=4，第一,二,三个词相同----------------------------------------------------------#
                        if iList[0] == jList[0] and iList[1] == jList[1] and iList[2] == jList[2] and iList[3] != jList[
                            3] \
                                and iList[3] in model and jList[3] in model:
                            similarity3 = model.similarity(iList[3].strip(), jList[3].strip())
                            if similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=4，第四个词相同----------------------------------------------------------#
                        if iList[3] == jList[3] and iList[0] != jList[0] and iList[1] != jList[1] and iList[2] != jList[
                            2] \
                                and iList[0] in model and jList[0] in model and iList[1] in model and jList[1] in model \
                                and iList[2] in model and jList[2] in model:
                            similarity1 = model.similarity(iList[0].strip(), jList[0].strip())
                            similarity2 = model.similarity(iList[1].strip(), jList[1].strip())
                            similarity3 = model.similarity(iList[2].strip(), jList[2].strip())
                            if similarity1 > Sthreshold and similarity2 > Sthreshold and similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity1, ',', similarity2, ',',
                                      similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=4，第三，四个词相同----------------------------------------------------------#
                        if iList[2] == jList[2] and iList[3] == jList[3] and iList[0] != jList[0] and iList[1] != jList[
                            1] \
                                and iList[0] in model and jList[0] in model and iList[1] in model and jList[1] in model:
                            similarity2 = model.similarity(iList[0].strip(), jList[0].strip())
                            similarity3 = model.similarity(iList[1].strip(), jList[1].strip())
                            if similarity2 > Sthreshold and similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity2, ',', similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass
                        # -----------------------------------------------------len=4，第二,三，四个词相同----------------------------------------------------------#
                        if iList[1] == jList[1] and iList[2] == jList[2] and iList[3] == jList[3] and iList[0] != jList[
                            0] \
                                and iList[0] in model and jList[0] in model:
                            similarity3 = model.similarity(iList[0].strip(), jList[0].strip())
                            if similarity3 > Sthreshold:
                                print("".join(iList), ",", "".join(jList), ",", similarity3)
                                result.append(["".join(iList), "".join(jList)])
                                pass

        return result

    # 第二种同义词抽取方法
    def secSynonymousMethod(self,CValueList):
        jieba.re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._% ]+)", re.U)
        for i in CValueList:
            jieba.add_word(i[0].replace(" ", ""))
        """
        将数据导入wrod2vec模型
        """
        model = self.word2VecFun()
        for i in CValueList:
            if i[0].replace(" ", "") in model:
                y3 = model.most_similar(i[0].replace(" ", ""), topn=3)
                print(i[0].replace(" ", ""), "::::", y3)

    def word2VecFun(self,docFilePath):
        """
        将数据导入wrod2vec模型
        """
        sentences = []
        sentencesTem = str(docFilePath).split('\n')
        for line in sentencesTem:
            temList = []
            for word in jieba.cut(line):
                temList.append(word)
            if len(temList):
                sentences.append(temList)

        model = Word2Vec(sentences, size=300, window=5, min_count=1, workers=2)
        return model

    def thridFunSynonymousMethod(self,MWTLIST,threshold):
        #哈工大词林方法
        i = 0
        result = []
        for i in MWTLIST:
            ar = i[0]
            br = i[1]
            r = synonyms.compare(ar, br, seg=True)
            if r > threshold:
                if [ar,br] in result or [br,ar] in result:
                    pass
                else:
                    result.append(i)
        return result

    def run(self):
        model = self.word2VecFun(self.filePath)
        Sthreshold = 0.99
        # 词林阈值
        Wthreshold = 0.92
        lineList = str(self.filePath).split('\n')
        MWTLIST = self.getMWT(lineList)
        new_MWTLIST = self.clusterMWT(MWTLIST)
        MWTFreList = self.getMWTFrequency(new_MWTLIST)
        CValueList = self.caCvalue(MWTFreList)
        print(CValueList)
        result = self.fistSynonymousMethod(CValueList, Sthreshold,model)
        result = self.thridFunSynonymousMethod(result,Wthreshold)
        print(result)

        return result
