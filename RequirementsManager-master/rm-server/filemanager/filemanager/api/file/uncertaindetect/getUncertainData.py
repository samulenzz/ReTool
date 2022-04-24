# 其实还是有挺多问题的
# 首先找scope的index范围用的是遍历而不是kmp
# 其次对于所有返回的scope的index没有做一个合并，即1,3+2,4=1,4
from docx import Document
from typing import List
from interval import Interval,IntervalSet
from filemanager.api.file.uncertaindetect.UncertaintyDetectInText.getSpeculativeWord import getCues
from filemanager.api.file.uncertaindetect.UncertaintyDetectInText.getscope import anno_sentence

def findindex(sentence:List,scope:List):
    l=len(scope)
    for i in range(0,len(sentence)):
        if sentence[i]==scope[0]:
            flag=True
            for j in range(1,l):
                if sentence[i+j]!=scope[j]:
                    flag=False
                    break
            if flag:
                return i,i+l
    return -1,-1

def gethtmltext(text:List,cueindex:List,scopeindex:List):
    def getone(indexs:List):
        intervals=[]
        for index in indexs:
            # 遍历，一次加一个
            pass

    htmltext=""
    if len(cueindex)==0:
        return " ".join(text)
    # intervals=getone(scopeindex)


    # for scope in intervals:
    #     scope_s.add(scope.lower_bound)
    #     scope_e.add(scope.upper_bound)
    scope_s=[]
    scope_e=[]
    cue_s=[]
    cue_e=[]

    for _ in scopeindex:
        scope_s.append(_[0])
        scope_e.append(_[1])
    for _ in cueindex:
        cue_s.append(_[0])
        cue_e.append(_[1])

    i=0
    for word in text:
        if i in scope_s:
            htmltext+=r'''<span style="color:blue">'''
        elif i in scope_e:
            htmltext += r'''</span>'''

        if i in cue_s:
            htmltext += r'''<span style="color:red">'''
        elif i in cue_e:
            htmltext += r'''</span>'''

        if i==0:
            htmltext+=word
        else:
            htmltext+=" "+word
        i+=1

    return htmltext

# 调用工具 找出模糊性 组织成html格式 返回
# 工具需要相应的更改 比如模糊范围返回index而不是具体的子句
def getUncertainData(docx_path:str):
    htmltextall=""
    text=""
    docx = Document(docx_path)
    for para in docx.paragraphs:
        text+=para.text
        text+="\n\n\n"

    allcue=getCues(text)
    i=0
    for cueinfo in allcue:
        cueindex=[]
        scopeindex=[]
        text=cueinfo[0]
        cues=cueinfo[1]
        if cues:
            for cue in cues:
                scope = anno_sentence(" ".join(text), cue)
                s,e=findindex(text,scope)
                cueindex.append([cue[0],cue[0]+cue[1].count(" ")+1])
                scopeindex.append([s,e])
        htmltext=gethtmltext(text,cueindex,scopeindex)
        htmltextall+=r"<p>"+htmltext+r"</p>"
    return htmltextall

if __name__=='__main__':
    testpath=r"C:\Users\wang9\Desktop\test2.docx"
    fout=open(r"C:\Users\wang9\Desktop\html.html","w",encoding='UTF-8')
    print(getUncertainData(testpath),file=fout)
