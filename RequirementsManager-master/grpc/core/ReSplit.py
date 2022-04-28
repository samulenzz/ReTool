# _*_coding:utf-8_*_
import os
import operator
from functools import reduce
import re


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname), mode='r', encoding='utf-8'):
                line = line.strip()
                yield line


class getItemizedRequirement(object):
    def __init__(self, docData,keyword):
        self.docData = docData
        self.keyword = keyword

    def splitSen(selfs,senDoc):
        docFile = str(senDoc).split('\n')
        sentences = docFile
        return sentences

    def replace_all_blank(self,value):
        comp = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5^\n^(^\[^\]^）^（^)^.^,^。^;^；^:^：^，]')
        return comp.sub('', value)

    def getLineList(self):
        # docFile = self.replace_all_blank(self.docData)
        docFile = self.splitSen(self.docData)
        allItemList = []
        for i in docFile:
            if len(i) != 0:
                allItemList.append(i)
        return allItemList

    def splitRequirement(self):
        allItemList = []
        result = []
        content = self.getLineList()
        for i in content:
            if len(i) != 0:
                pattern = re.compile('[0-9]+\.')
                match = pattern.findall(i)
                if (")" in i or "）" in i or match) and '()' not in i and i not in allItemList:
                    allItemList.append(i)
        for i in allItemList:
            startNum = allItemList.index(i)
            if "a)" in i or "(a)" in i or "a）" in i or "（a）" in i:
                temList1 = []
                startWord = 'a'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    if "a)" in i or "(a)" in i:
                        startWord = chr(ord(startWord) + 1) + ")"
                    elif "a）" in i or "（a）" in i:
                        startWord = chr(ord(startWord) + 1) + "）"
                    if startNum < len(allItemList) - 1:
                        startNum = startNum + 1
                        if startWord in allItemList[startNum]:
                            temList1.append(allItemList[startNum])
                    else:
                        if len(temList1) > 1:
                            result.append(temList1)
                        break
            elif "A)" in i or "(A)" in i or "A）" in i or "（A）" in i:
                temList1 = []
                startWord = 'A'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    if "A)" in i or "(A)" in i:
                        startWord = chr(ord(startWord) + 1) + ")"
                    elif "A）" in i or "（A）" in i:
                        startWord = chr(ord(startWord) + 1) + "）"
                    if startNum < len(allItemList) - 1:
                        startNum = startNum + 1
                        if startWord in allItemList[startNum]:
                            temList1.append(allItemList[startNum])
                    else:
                        if len(temList1) > 1:
                            result.append(temList1)
                        break
            elif "(1)" in i or "1)" in i or "（1）" in i or "1）" in i:
                temList1 = []
                startWord = '1'
                temList1.append(allItemList[startNum])
                while (1):
                    if len(startWord) > 1:
                        startWord = startWord[:-1]
                    if "1)" in i or "(1)" in i:
                        startWord = str(int(startWord) + 1) + ")"
                    elif "（1）" in i or "1）" in i:
                        startWord = str(int(startWord) + 1) + "）"
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
        if len(result):
            temList2 = reduce(operator.add, result)
            ret_list = list(set(content).difference(set(temList2)))
        else:
            ret_list = list(set(content))

        for i in ret_list:
            if (i.count(';') > 0 or i.count('；') > 0):
                temList = re.split('[;；]', i.strip())
                if len(temList) > 1 and len(temList[1]) and temList not in result:
                    result.append(temList)
            elif len(self.keyword) > 0:
                flag = 0
                for j in self.keyword:
                    if i.count(j) > 1:
                        flag = 1
                        temList = re.split(j, i.strip())
                        if len(temList) > 1 and len(temList[1]) and temList not in result:
                            for m in temList:
                                if temList.index(m) != 0:
                                    result.append([str(temList[0])+str(j)+str(m)])
                            break
                if flag == 0:
                    result.append([i])
            # elif i not in result:
            #     result.append([i])
        for i in result:
            temlist = []
            for j in i:
                if ")" in j[:5]:
                    temlist.append(j[j.index(")") + 1:])
                elif "）" in j[:5]:
                    temlist.append(j[j.index("）") + 1:])
                elif "." in j[:5]:
                    temlist.append(j[j.index(".") + 1:])
                else:
                    temlist.append(j.strip())
            result[result.index(i)] = temlist
        return result