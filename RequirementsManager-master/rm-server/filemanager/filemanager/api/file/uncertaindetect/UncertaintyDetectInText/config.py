import collections
tokenfile="C:\\Users\\wang9\\Desktop\\gradesign\\use\\docs\\out2\\3_final\\cuesright.txt"
cuesinfo=[]

auxiliaries = ["may","might","can","would","should","could"]
nraising_verbs = ["imply","implies","suppose","supposes","supposed","indicate",\
                  "indicating","indicates","suspected","expect","expected",\
                  "suggest","suggests","suggested",\
                  "proposed","presumed",
                  "assume","assumes","assumed","assuming",\
                  "believe","consider","considered"]
#verb不太好处理，因为要考虑各种时态，还要分提升非提升
raising_verbs=["seem","seems","appear","appears"]
verbs=raising_verbs+nraising_verbs
verbtypes=["VB","VBD","VBG","VBN","VBP","VBZ"]
adjectives=["possible","likely",
            "probable","unlikely","unsure","unclear","clear","potential"]
adverbs=["possibly",
         "probably","presumably", "perhaps", "potentially"]
nouns=["assumption","possibility",
       "probability", "hypothesis", "suggestion","indication"]
conjs=["either","whether","or","if"]
allcues=auxiliaries+verbs+adjectives+adverbs+nouns+conjs

stopword = ["whereas", "but", "although", "nevertheless", "until",".",";"]

dir=r"C:\Users\wang9\Desktop\gradesign\liuchang\liuchang\RequirementsManager-master\rm-server\filemanager\filemanager\api\file\uncertaindetect\UncertaintyDetectInText\files\\"
forgenia=dir+"forgenia.txt"
geniaed=dir+"geniaed.txt"
fortest=dir+"fortest.txt"
res=dir+"res.txt"
