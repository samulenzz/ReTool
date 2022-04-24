import stanza
from stanza.server import CoreNLPClient
import re
from filemanager.api.file.uncertaindetect.UncertaintyDetectInText.config import *
import collections
class tNode:
    def __init__(self, node, pnode, isleaf):
        self.node = node
        self.pnode = pnode
        self.isleaf = isleaf
        self.value=node.value
        self.tchilds = []
        self.dpout = {}
        self.dpin = {}

    def getValue(self):
        return self.node.value

def cutscope(scope,cutters,iscutterin=True):
    l=[]
    for word in scope:
        if word in cutters:
            if iscutterin:
               l.append(word)
            return l
        l.append(word)
    return l

def findkeywithvalue(map,value):
    for k,v in map.items():
        if v.value==value:
            return k

def beginscope(scope,beginner):
    l = []
    flag=False
    for word in scope:
        if word == beginner:
            flag=True
        if flag:
            l.append(word)
    return l


def viewTree(tnode: tNode):
    print(tnode.node.value)
    tchilds = tnode.tchilds
    i = 0
    while i < len(tchilds):
        tchild = tchilds[i]
        viewTree(tchild)
        i += 1


def getstnode(cuenode: tNode, start: str):
    if cuenode.getValue() == start:
        return cuenode
    else:
        if cuenode.getValue()=="ROOT":
            return False
        return getstnode(cuenode.pnode, start)

def getstnodes(cuenode: tNode, start: list):
    if cuenode.getValue() in start:
        return cuenode
    else:
        return getstnodes(cuenode.pnode, start)

def getancestor_num(node:tNode,num:int):
    for i in range(0,num):
        node=node.pnode
    return node

def getcommonancestor(node1,node2):
    tnode1=node1.pnode
    tnode2=node2.pnode
    lp1=[tnode1]
    lp2=[tnode2]
    while tnode1.value!="ROOT":
        tnode1=tnode1.pnode
        lp1.append(tnode1)
    while tnode2.value!="ROOT":
        tnode2=tnode2.pnode
        lp2.append(tnode2)
    for n1 in lp1:
        for n2 in lp2:
            if n1 is n2:
                return n1
    print("%s and %s dont have common ancestor")
    exit(0)

def getscope(snode: tNode,add_sword:list=[]):
    global stopword
    mystopword=stopword+add_sword
    l = []
    if snode.isleaf and (snode.getValue() in mystopword):
        return [], False
    elif snode.isleaf:
        return [snode.getValue()], True
    else:
        for i in range(len(snode.tchilds)):
            tmpl, flag = getscope(snode.tchilds[i],add_sword)
            l.extend(tmpl)
            if not flag:
                return l,flag
        return l,True

def getscope_child(fnode: tNode, cnode: tNode,reachcnode:bool=False,add_sword:list=[]):
    #从fnode的cnode开始保留，前面的child不保留
    global stopword
    mystopword = stopword + add_sword
    l = []
    if fnode.isleaf and (fnode.getValue() in mystopword):
        return [], False
    elif fnode.isleaf:
        return [fnode.getValue()], True
    else:
        for i in range(len(fnode.tchilds)):
            if fnode.tchilds[i] is cnode:
                reachcnode=True
            if not reachcnode:
                continue
            tmpl, flag = getscope_child(fnode.tchilds[i],cnode,True)
            l.extend(tmpl)
            if not flag:
                return l, flag
        return l, True


def anno_sentence(text,cueinfo):
    def buildTree(tnode: tNode):
        global leafi
        if len(tnode.node.child) == 0:
            tnode.isleaf = True
            num2leafnode[leafi] = tnode
            leafi += 1
            return

        childs = tnode.node.child
        i = 0
        while i < len(childs):
            child = childs[i]
            tmptNode = tNode(child, tnode, False)
            tnode.tchilds.append(tmptNode)
            buildTree(tmptNode)
            i += 1
    def buildDependencies():
        nonlocal num2leafnode
        bds = sen.basicDependencies
        for i in range(0, len(bds.edge)):
            edge = bds.edge[i]
            s = edge.source
            t = edge.target
            dep = edge.dep
            if (dep in num2leafnode[s - 1].dpout.keys()):
                num2leafnode[s - 1].dpout[dep].append(num2leafnode[t - 1])
            else:
                num2leafnode[s - 1].dpout[dep] = [num2leafnode[t - 1]]
            if (dep in num2leafnode[t - 1].dpin.keys()):
                num2leafnode[t - 1].dpin[dep].append(num2leafnode[s - 1])
            else:
                num2leafnode[t - 1].dpin[dep] = [num2leafnode[s - 1]]

    def findCenter(index: int, cue: str):
        if cue == "either":
            '''
            for cueinfo in cues:
                indexi, cuei = cueinfo[0], cueinfo[1]
                if cuei == "or":
                    return indexi, cuei
            '''
            for i in sorted(num2leafnode):
                if i>index and num2leafnode[i].getValue().lower()=="or":
                    return i,"or"
            print("either without or means no uncertainty")
            exit(0)
        elif cue.count(" ") == 0:
            return index, cue
        if cue in ["indicating that", "indicates that", "indicate that"]:
            return index, cue.split(" ")[0]
        elif cue in ["whether or not"]:
            return index, "whether"
        elif cue in ["may or may not"]:
            return index + 2, "may"
        elif cue in ["not clear"]:
            return index + 1, "clear"
        elif cue in ["and / or"]:
            return index + 2, "or"
        else:
            print("no such multi-word-cue")
            exit(1)
    def search_leaf_value(index:int,cue:str):
        if index not in num2leafnode.keys() or\
                num2leafnode[index].getValue().lower()!=cue:
            print("index cue not match at\t%s %s %s\n" %(text,index,cue))
            exit(0)
        else:
            return num2leafnode[index]

    def toend(cuetnode):
        l=[]
        flag=False
        for i in range(0,len(num2leafnode)):
            if flag:
                l.append(num2leafnode[i].value)
            if num2leafnode[i]==cuetnode:
                l.append(cuetnode.value)
                flag=True
        return l[0:-1]

    def anno_aux():
        cuetnode = search_leaf_value(index,cue)
        if "aux" not in cuetnode.dpin.keys():
            tnodestart = getstnode(cuetnode, "VP")
            scope, flag = getscope(tnodestart)
            return scope
        verbs = cuetnode.dpin["aux"]
        if (len(verbs) != 1):
            print("wrong2 more" + text)
            exit(0)
        verbtype = verbs[0].pnode.getValue()
        verbnode=verbs[0]
        if verbtype == "VB":
            start = "VP"
        elif verbtype == "VBN":
            tnodestart = getstnode(cuetnode, "S")
            if "nsubj:pass" in verbnode.dpout.keys():
                subnode=verbnode.dpout["nsubj:pass"][0]
                tnodenp=getstnode(subnode,"NP")
                if tnodenp!=False:
                    if tnodenp.pnode == tnodestart:
                        scope, flag = getscope_child(tnodestart,tnodenp)
                        return scope
                    elif tnodenp.pnode.pnode==tnodestart and tnodenp.pnode.value=="NP":
                        scope, flag = getscope_child(tnodestart, tnodenp.pnode)
                        return scope
            scope, flag = getscope(tnodestart)
            return scope
        else:
            start="VP"
        tnodestart = getstnode(cuetnode, start)
        scope, flag = getscope(tnodestart)
        return scope

    def anno_verbs():
        cuetnode = search_leaf_value(index,cue)
        # 找出发点
        if cue in raising_verbs:
            #Insulin is only delivered in circumstances where it appears that the level is likely to go outside this range.
            tnodestart = getstnode(cuetnode, "S")
        elif cuetnode.pnode.getValue() == "VBN":
            tnodestart = getstnode(cuetnode, "S")
            if tnodestart.pnode.getValue() == "ROOT":
                #You are supposed to go there.
                if "nsubj:pass" in cuetnode.dpout.keys():
                    subnode=cuetnode.dpout["nsubj:pass"][0]
                    npnode=getstnode(subnode,"NP")
                    if npnode.pnode==tnodestart:
                        scope,flag=getscope_child(tnodestart,npnode)
                        return scope
                    elif npnode.pnode.pnode==tnodestart:
                        scope,flag=getscope_child(tnodestart,npnode.pnode)
                        return scope
                pass
            elif (tnodestart.pnode.getValue() == "SBAR") and \
                        (tnodestart.pnode.tchilds[0].getValue() == "WHNP"):
                #This determination requires figuring out what the CBS is supposed to do, i.e., the full set of features.
                tnodestart = tnodestart.pnode
            elif (tnodestart.pnode.getValue() == "SBAR") and \
                        (tnodestart.pnode.tchilds[0].getValue() == "WHADVP"):
                #The user will be directed to a special web page that provides clear message about the status of the web site and when it is expected to return to normal operation .
                tnodestart = tnodestart.pnode
            elif (tnodestart.pnode.getValue() == "SBAR") and \
                    (tnodestart.pnode.tchilds[0].getValue() == "ADVP"):
                # Diagnoses The patient 's diseases , actual as well as suspected .
                tnodestart = tnodestart.pnode
            elif (tnodestart.pnode.getValue() == "SBAR") and \
                        (tnodestart.pnode.tchilds[0].getValue() == "WHPP"):
                #The pointer to an annotated VCDU in which the end of line code ends are expected to be quiet.
                tnodestart = getstnode(cuetnode, "ROOT")
            else:
                pass
        else:
            #The multiple media requirement implies the ability to generate a seamless map background from more than one CD ROM.
            # if "ccomp" in cuetnode.dpout.keys():
            #     pass
            #     sub1=cuetnode.dpout["ccomp"][0]
            #     if "conj" in sub1.dpout.keys():
            #         sub2=sub1.dpout["conj"][0]
            #         snode=getcommonancestor(sub1,sub2)
            #         scope,flag=getscope(snode)
            #         scope=beginscope(scope,cuetnode.value)
            #         return scope
            tnodestart = getstnode(cuetnode, "VP")
        # 开始标注
        scope, flag = getscope(tnodestart)
        return scope

    def anno_adjs():
        cuetnode = search_leaf_value(index,cue)
        flag1 = "nsubj" in cuetnode.dpout.keys()
        flag2 = "amod" in cuetnode.dpin.keys()
        flag3 = "advmod" in cuetnode.dpin.keys()

        if flag1 and not flag2:
            tnodestarts = cuetnode.dpout["nsubj"]
            if (len(tnodestarts) != 1):
                tnodestart = tnodestarts[1]
            else:
                tnodestart = tnodestarts[0]
            subvalue=tnodestart.value
            tnodestarts = getstnode(tnodestart, "S")
            tnodestartnp = getstnode(tnodestart, "NP")
            while tnodestartnp not in tnodestarts.tchilds:
                if tnodestartnp==tnodestarts:
                    print("wrong66")
                    exit(0)
                tnodestartnp=tnodestartnp.pnode
            scope, flag = getscope_child(tnodestarts,tnodestartnp,False)
        elif not flag1 and flag2:
            tnodestarts = cuetnode.dpin["amod"]
            if (len(tnodestarts) != 1):
                tnodestart = tnodestarts[1]
            else:
                tnodestart = tnodestarts[0]
            scope, flag = getscope_child(getancestor_num(tnodestart, 3),
                                         getancestor_num(tnodestart, 2),
                                         False)
            if cuetnode.value in scope:
                scope=beginscope(scope,cuetnode.value)
                pass
            else:
                scope=[cuetnode.value]+scope
            #这里本来觉得比如“potential corrections to misspelled key words”这个句子应该只有potential corrections
            #后来一想好像还是全加吧
            '''
             if "acl:relcl" in tnodestart.dpout.keys():
                scope, flag = getscope_child(getancestor_num(tnodestart, 3),
                                             getancestor_num(tnodestart, 2),
                                             False)
            elif "nmod" in tnodestart.dpout.keys():
                tnodestart = getstnode(tnodestart, "NP")
                scope, flag = getscope(tnodestart)
            else:
                print("wrong3.9")
                exit(0)
            '''

        elif flag3:
            tnodestart = getstnode(cuetnode, "ROOT")
            scope, flag = getscope(tnodestart)
        else:
            tnodestart = getstnode(cuetnode, "ROOT")
            scope, flag = getscope(tnodestart)
        return scope

    def anno_advs():
        cuetnode = search_leaf_value(index,cue)
        if "advmod" not in cuetnode.dpin.keys():
            tnodestart = getstnode(cuetnode, "ROOT")
            scope, flag = getscope(tnodestart)
            return scope
        subs = cuetnode.dpin["advmod"]
        if (len(subs) != 1):
            print("wrong2 more" + text)
            exit(0)
        subnode=subs[0]
        # indexsub=findkeywithvalue(num2leafnode,subnode)
        # indexcue=findkeywithvalue(num2leafnode,cuetnode)
        # if indexsub>indexcue:
        #     tnodestart = getstnode(subnode, "ROOT")
        #     scope, flag = getscope(tnodestart)
        #     scope=beginscope(scope,cuetnode.value)
        #     scope=cutscope(scope,[")",","],False)
        #     return scope
        subtype = subnode.pnode.getValue()
        if subtype in verbtypes:
            start = "S"
            tnodestart = getstnode(subnode, start)
            if tnodestart==False:
                tnodestart = getstnode(subnode, "ROOT")
            scope, flag = getscope(tnodestart)
        else:
            if "nsubj" in subnode.dpout.keys():
                subnode=subnode.dpout["nsubj"][0]
                tnodestart = getstnode(subnode, "S")
                if not tnodestart:
                    return ["1","1"]
                scope, flag = getscope(tnodestart)
                return scope
            cnodestart = getstnodes(subnode, ["NP","S"])
            # scope, flag = getscope(cnodestart)
            # scope=beginscope(scope,cuetnode.value)
            if cnodestart.value=="NP":
                if cnodestart.pnode.value=="PP":
                    tnodestart = getstnode(cnodestart, "ROOT")
                    scope, flag = getscope(tnodestart)
                else:
                    scope, flag = getscope_child(cnodestart.pnode, cnodestart)
            else:
                scope, flag = getscope(cnodestart,[","])
        if cuetnode.value not in scope:
            scope=[cuetnode.value]+scope
        return scope

    def anno_nouns():
        cuetnode = search_leaf_value(index,cue)
        nthat = 0
        nto = 0
        nof=0
        if "ccomp" in cuetnode.dpout.keys():
            thats = cuetnode.dpout["ccomp"]
            nthat = len(thats)
        elif "dep" in cuetnode.dpout.keys():
            thats = cuetnode.dpout["dep"]
            nthat = len(thats)
        if "nsubj" in cuetnode.dpin.keys():
            tos = cuetnode.dpin["nsubj"]
            nto = len(tos)
        elif "nsubj" in cuetnode.dpin.keys():
            tos = cuetnode.dpin["nsubj"]
            nto = len(tos)
        if "nmod" in cuetnode.dpout.keys():
            ofs = cuetnode.dpout["nmod"]
            nof = len(ofs)
        if (nthat == 1 and nto == 0) or (nthat == 1 and nto == 1):
            thatnode = thats[0]
            tnodestart = getstnode(thatnode, "SBAR")
            if not tnodestart:
                tnodestart = getstnode(thatnode, "ROOT")
            scope, flag = getscope(tnodestart)
            if cuetnode.value not in scope:
                scope = [cuetnode.value] + scope
            else:
                pass
        elif nthat == 0 and nto == 1:
            tonode = tos[0]
            tnodestart = getstnode(tonode, "S")
            scope, flag = getscope(tnodestart)
            if cuetnode.value not in scope:
                scope = [cuetnode.value] + scope
            else:
                scope=beginscope(scope,cuetnode.value)
        elif nof==1:
            ofnode = ofs[0]
            tnodestart = getstnode(ofnode, "PP")
            scope, flag = getscope(tnodestart)
            if cuetnode.value not in scope:
                scope = [cuetnode.value] + scope
            else:
                scope = beginscope(scope, cuetnode.value)
        else:
            tnodestart = getstnodes(cuetnode, ["S","ROOT"])
            scope, flag = getscope(tnodestart)
            scope = beginscope(scope, cuetnode.value)
        return scope

    '''
    如果是either，同一句一定有or，按or处理，注意这里一定是分开的，所以不好找
    or的话 首先cc到第二个词 然后conj到第一个词 然后找共同祖先
    如果找不到or的话 再特殊处理
    '''
    def anno_conjs():
        if cue=="or":
            cuetnode = search_leaf_value(index, cue)
            if "cc" not in cuetnode.dpin.keys():
                print("wrong2 not" + text)
                exit(0)
            snns = cuetnode.dpin["cc"]
            if (len(snns) != 1):
                print("wrong2 more" + text)
                exit(0)
            snn=snns[0]
            if "conj" not in snn.dpin.keys():
                #cc到的一定是第二个
                tnodestart = getcommonancestor(cuetnode, snn)
                scope, flag = getscope(tnodestart)
                scope=cutscope(scope,[snn.node.value])
            else:
                fnns = snn.dpin["conj"]
                if (len(fnns) != 1):
                    print("wrong2 more" + text)
                    exit(0)
                fnn=fnns[0]
                tnodestart=getcommonancestor(fnn,snn)
                scope, flag = getscope(tnodestart)
        elif cue=="either":
            '''
            Either of these(two) words is correct.
            大概思路应该是找到either的主语 然后向上找到S
            后来发现其实并不是，这个句子并没有模糊性
            either单独使用的时候是两者任一 都行的意思
            '''
            pass
        elif cue=="whether":
            cuetnode = search_leaf_value(index,cue)
            if "nsubj" in cuetnode.dpout.keys():
                subs = cuetnode.dpout["nsubj"]
                if (len(subs) > 1):
                    print("wrong2 more" + text)
                    exit(0)
                else:
                    subnode = subs[0]
                    tnodestart = getstnode(subnode, "S")
                    scope, flag = getscope(tnodestart)
            else:
                tnodestart = getstnode(cuetnode, "SBAR")
                if tnodestart==False:
                    scope=toend(cuetnode)
                else:
                    scope, flag = getscope(tnodestart)
        elif cue=="if":
            cuetnode = search_leaf_value(index, cue)
            tnodestart = getstnode(cuetnode, "SBAR")
            if tnodestart==False:
                tnodestart = getstnode(cuetnode, "PP")
            scope, flag = getscope(tnodestart)
        return scope

    global leafi
    leafi=0
    num2leafnode = {}
    # 获取标注结果，建立数据结构
    ann = client.annotate(text)
    sen = ann.sentence[0]
    rnode=sen.parseTree
    # print(sen.parseTree)
    # exit(0)
    rtnode = tNode(rnode, None, False)
    buildTree(rtnode)
    buildDependencies()

    # 完成了相关辅助数据结构的构建之后，就开始进入真正的标注
    index=cueinfo[0]
    cue = cueinfo[1].lower()
    index,cue=findCenter(index,cue)
    if cue in auxiliaries:
        return anno_aux()
    elif cue in verbs:
        return anno_verbs()
    elif cue in adjectives:
        return anno_adjs()
    elif cue in adverbs:
        return anno_advs()
    elif cue in nouns:
        return anno_nouns()
    elif cue in conjs:
        return anno_conjs()
    else:
        print("there is no such cue")
        exit(0)

leafi=0

#stanfordcorenlpclient
# properties = {
#         'tokenize.whitespace': True,
#         'ssplit.eolonly': True
# }
# client = CoreNLPClient(
#     annotators=['tokenize','ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
#     timeout=30000, memory='8G',
#     start_server=stanza.server.StartServer.TRY_START, be_quiet=True,
#     properties=properties)
client=CoreNLPClient(timeout = 30000,memory = '8G',be_quiet = True,
start_server = stanza.server.StartServer.TRY_START,
properties='C:/Users/wang9/Desktop/gradesign/use/docs/myprop.props')
# 吐了 有好几个坑：
# 首先 timeout等信息必须直接指定
# 其次props文件路径必须全部
# 最后必须用斜杠而不是传统的反斜杠
client.start()
if __name__=="__main__":
    issingle=True
    finsentence=open(r"C:\Users\wang9\Desktop\sentence.txt","r",encoding='UTF-8')
    text=finsentence.readline()
    text=text.strip()
    cues = [[19,"could"]]
    if issingle:
        for cueinfo in cues:
            if cueinfo != []:
                scope = anno_sentence(text, cueinfo)
                print(scope)
    else:
        for t in cuesinfo:
            sentence = t[0]
            cues = t[1]
            for cue in cues:
                scope = anno_sentence(sentence, cue)
                print(scope)

    client.stop()