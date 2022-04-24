import os
from filemanager.api.file.uncertaindetect.UncertaintyDetectInText import config
import stanza

def aftergenia():
    res = []
    res2 = []
    res21 = []
    res22 = []
    res23 = []
    nlp = stanza.Pipeline(lang='en', tokenize_pretokenized=True)
    fin=open(config.geniaed,"r",encoding='UTF-8')
    fout=open(config.fortest,"w",encoding='UTF-8')
    while 1:
        line = fin.readline()
        if not line:
            break
        if line == '\n':
            res.append(res2)
            res2 = []
        else:
            res2.append(line.split('\t', 4)[0])
            res21.append(line.split('\t', 4)[1])
            res22.append(line.split('\t', 4)[2])
            res23.append(line.split('\t', 4)[3])
    doc = nlp(res)
    index = 0
    for sentence in doc.sentences:
        for word in sentence.words:
            fout.write("%s\t%s\t%s\t%s\t" % (word.text, res21[index], res22[index], res23[index]))
            index += 1
            if word.head == 0:
                fout.write("ROOT\tO\troot\tO\n")
            else:
                fout.write("%s\t%s\t%s\tO\n" % (
                sentence.words[(word.head) - 1].lemma, sentence.words[(word.head) - 1].xpos, word.deprel))
        fout.write("\n")
    fout.close()

def readcues():
    fin=open(config.res,"r",encoding='UTF-8')
    flag = True
    hascue = False
    cue = ""
    start = -1
    i = 0
    sentence = []
    cues = []
    allcue=[]
    while 1:
        line = fin.readline()
        if not line:
            break
        elif line == "\n":
            if hascue:
                allcue.append([sentence,cues])
            else:
                allcue.append([sentence, None])
            flag = True
            hascue = False
            i = 0
            sentence = []
            cues = []
            continue
        else:
            content = line.split("\t")[-1]
            content = content.strip("\n")
            if content == "wzd256":
                id = line.split("\t")[0]
                continue
            else:
                word = line.split("\t")[0]
                if flag:
                    sentence.append(word)
                    flag = False
                else:
                    sentence.append(word)

                if content == "B":
                    if start != -1:
                        # 暂时取第一个单词的位置，需要讨论
                        cues.append([start, cue])
                        hascue = True
                        start = i
                        cue = word
                    else:
                        hascue = True
                        start = i
                        cue += word
                elif content == "I":
                    # 由于机器学习不准确，有可能直接I开始
                    hascue = True
                    if start == -1:
                        start = i
                        cue += word
                    else:
                        cue += " " + word
                else:
                    if start != -1:
                        # 暂时取第一个单词的位置，需要讨论
                        cues.append([start, cue])
                        start = -1
                        cue = ""
                i += 1
    return allcue

def getCues_single(sentence):
    text=""
    fout1 = open(config.forgenia, "w", encoding='UTF-8')
    nlp = stanza.Pipeline('en', use_gpu=True, processors='tokenize', tokenize_no_ssplit=True)
    doc=nlp(sentence)
    for sentence in doc.sentences:
        iword = 0
        for word in sentence.words:
            if iword == 0:
                fout1.write("%s" % (word.text))
                text+=word.text
                iword = 1
            else:
                fout1.write(" %s" % (word.text))
                text += " "+word.text
        fout1.write("\n")
    fout1.close()
    #倒是可以添加到环境变量 也可以找到 但是运行出错 必须切换到那个文件夹里才能成功运行tagger
    code1=r"cd C:\Users\wang9\Desktop\gradesign\use\mygeniatagger"
    code2=r"geniatagger.exe -nt "+config.forgenia+" > "+config.geniaed
    os.system(code1+r"&&"+code2)
    aftergenia()
    os.system(r"crf_test -m ./files/mymodel9 ./files/fortest.txt > ./files/res.txt")
    cues=readcues()
    return cues,text

def getCues(sentence):
    fout1 = open(config.forgenia, "w", encoding='UTF-8')
    nlp = stanza.Pipeline('en', use_gpu=True, processors='tokenize', tokenize_no_ssplit=True)
    doc=nlp(sentence)
    for sentence in doc.sentences:
        iword = 0
        for word in sentence.words:
            if iword == 0:
                fout1.write("%s" % (word.text))
                iword = 1
            else:
                fout1.write(" %s" % (word.text))
        fout1.write("\n")
    fout1.close()
    #倒是可以添加到环境变量 也可以找到 但是运行出错 必须切换到那个文件夹里才能成功运行tagger
    code1=r"cd C:\Users\wang9\Desktop\gradesign\use\mygeniatagger"
    code2=r"geniatagger.exe -nt "+config.forgenia+" > "+config.geniaed
    os.system(code1+r"&&"+code2)
    aftergenia()
    print(os.system("dir"))
    os.system(r"crf_test -m .\api\file\uncertaindetect\UncertaintyDetectInText\files\mymodel9 .\api\file\uncertaindetect\UncertaintyDetectInText\files\fortest.txt > .\api\file\uncertaindetect\UncertaintyDetectInText\files\res.txt")
    allcue=readcues()
    return allcue

if __name__=="__main__":
    pass