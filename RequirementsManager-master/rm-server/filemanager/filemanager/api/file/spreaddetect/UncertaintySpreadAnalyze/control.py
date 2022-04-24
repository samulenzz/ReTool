#-*-coding:gb2312-*-
import data
import stanza
from UncertaintyDetectInText import getSpeculativeWord
from UncertaintyDetectInText import getscope
import demo
import re
import pprint
import json
import demjson
from typing import List

class myRE:
    def __init__(self,FRDL):
        # 六元组
        self.FRDL=FRDL
        # 自身有没有模糊性
        self.isUncertain=False
        # 如果有，模糊的范围，是一个子句
        self.scope=""
        # 0代表没有传播，1代表前提依传播过来，2代表交互传播过来
        self.spread=0
        # 传播源头的id
        self.sourceid=-1

    def getF(self):
        return self.FRDL

    def getID(self):
        return int(self.FRDL['id'])

def tokenizeSen(text):
    nlp = stanza.Pipeline('en', use_gpu=True, processors='tokenize', tokenize_no_ssplit=True)
    words=[]
    sen=nlp(text).sentences[0]
    for word in sen.words:
        words.append(word.text)
    return " ".join(words)

def getREs_single():
    global  myREs
    for s in data.testF:
        tRE=myRE(s)
        id=s['id']
        text = s['description']
        cues,text = getSpeculativeWord.getCues_single(text)
        if len(cues)>0:
            tRE.isUncertain=True
            for cue in cues:
                scope = getscope.anno_sentence(text,cue)
                tRE.scope+=" ".join(scope)+" "
        myREs[id]=tRE

def getREs(testF:List):
    global myREs
    allre=""
    for s in testF:
        text = s['description']
        allre+=text
        allre+="\n\n\n"
    allcue=getSpeculativeWord.getCues(allre)
    i=0
    for cueinfo in allcue:
        text=cueinfo[0]
        cues=cueinfo[1]
        s=testF[i]
        tRE = myRE(s)
        id = s['id']
        i+=1
        if cues:
            tRE.isUncertain=True
            for cue in cues:
                scope = getscope.anno_sentence(text, cue)
                tRE.scope += " ".join(scope) + " "
        myREs[id] = tRE

def analyzeSpread(rela_result):
    def checkinscope(s,scope:str,type:str):
        def rim(s:str):
            return s.replace("[","").replace("]","").replace(" ","").lower()
        scope=scope.lower().replace(" ","")
        l1=[]
        s1=set()
        if type=="output" or type=="input":
            l1=s.split(", ")
        elif type=="event":
            # event虽然实际是五元组 但是是字符串 不好处理 所以不如直接手动改成子句
            # l1.append(s['agent'])
            # l1.append(s['operation'])
            # l1.append(s['input'])
            # l1.append(s['output'])
            # l1.append(s['restriction'])
            if s=="":
                return False
            if not isinstance(s,dict):
                print("can't decode this event %s" %(s))
                return False
            l1.append(s['agent'])
            l1.append(s['operation'])
            l1.append(s['input'])
            l1.append(s['output'])
            l1.append(s['restriction'])
        elif type=="operation":
            l1.append(s)
        else:
            print("there is no such element")
            return False
        for s in l1:
            s1.add(rim(s))
        for s in s1:
            if s in scope:
                return True
        return False


    for r in rela_result:
        sourceRE=myREs[r['id1']]
        targetRE=myREs[r['id2']]
        if not (sourceRE.isUncertain or targetRE.isUncertain):
            continue

        # if r['relationType'] == '0':
        #     if tokenizeSen(sourceRE.getF()['operation']) in sourceRE.scope:
        #         targetRE.spread=1
        #         targetRE.sourceid=sourceRE.getID()
        # elif r['relationType'] == '4':
        #     if tokenizeSen(sourceRE.getF()['output']) in sourceRE.scope:
        #         targetRE.spread=2
        #         targetRE.sourceid=sourceRE.getID()
        # else:
        #     pass

        if r['relationType'] == '0':
            if sourceRE.isUncertain:
                if checkinscope(sourceRE.getF()['operation'],sourceRE.scope,"operaion"):
                    targetRE.spread=1
                    targetRE.sourceid=sourceRE.getID()
            if targetRE.isUncertain:
                if checkinscope(targetRE.getF()['event'],targetRE.scope,"event"):
                    sourceRE.spread=2
                    sourceRE.sourceid=targetRE.getID()

        elif r['relationType'] == '4':
            if sourceRE.isUncertain:
                if checkinscope(sourceRE.getF()['output'], sourceRE.scope, "output"):
                    targetRE.spread = 3
                    targetRE.sourceid = sourceRE.getID()
            if targetRE.isUncertain:
                if checkinscope(targetRE.getF()['input'], targetRE.scope, "input"):
                    sourceRE.spread = 4
                    sourceRE.sourceid = targetRE.getID()
        else:
            pass
    for re in myREs.values():
        print(re.getID(),re.isUncertain,re.spread,re.sourceid)

def readStructedRes():
    fin=open(SReFile,"r",encoding='UTF-8')
    lines=fin.readlines()
    fin.close()
    for line in lines:
        if line=="" or line=="\n":
            continue
        line=line.strip()
        if line[-1]==',':
            line=line[0:-1]
        # data=json.loads(line)
        try:
            data=demjson.decode(line)
        except Exception as e:
            print(line)
            exit(0)
        testF.append(data)

def readStructedRes0():
    with open(SReFile,"r",encoding='UTF-8') as fin:
        testF=json.load(fin)

def myreadRelations():
    fin = open(RelationFile, "r", encoding='UTF-8')
    lines = fin.readlines()
    fin.close()
    for line in lines:
        content=re.search(r"\{.*\}",line)
        if content == None:
            continue
        content=content.group()
        content=content[1:-1]
        contents=content.split(", ")
        id1=contents[0].split(": ")[1][1:-1]
        id2=contents[1].split(": ")[1][1:-1]
        relationType=contents[2].split(": ")[1][1:-1]
        rela={}
        rela['id1']=id1
        rela['id2']=id2
        rela['relationType']=relationType
        result.append(rela)

def readRelations():
    global result
    with open(RelationFile,"r",encoding='UTF-8') as fin:
        result=json.load(fin)

testF=[]
result=[]
myREs = {}
folder=r"C:\Users\wang9\Desktop\2\\"
SReFile=folder + "sre.json"
RelationFile=folder + "rela.json"
def wordonFile():
    readStructedRes()
    readRelations()
    getREs(testF)
    analyzeSpread(result)


getREs(data.testF)
readRelations()
# demo.get_relationship_014(data.testF)
# demo.get_relationship_4(data.testF)
analyzeSpread(result)


