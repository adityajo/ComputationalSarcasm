import xlrd
from nltk.stem import PorterStemmer
import nltk
import re
from textblob import TextBlob
path='quotesA+V.xlsx'
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)
rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]
targs=[]

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        targs.append(l[1])

p=open('positive_sent_words.txt','r') #positive sentiment words lexicon
n=open('negative_sent_words.txt','r') #negative sentiment words lexicon
p=list(p)
n=list(n)
p=[x[:-1] for x in p]
n=[q[:-1] for q in n]



print("No.of sents - "+str(len(sents))) #nukmber of text instances of dataset
# compute average length of text - 
x=0
for s in sents:
    print(s)
    l=nltk.word_tokenize(s)
    for ww in l:
        ww.encode(encoding='utf-8')
        if (ww!=',') and (ww!='.') and (ww!='?') and (ww!='!') and (ww!='"') and (ww!="'") and (ww!=')') and (ww!='(') and (ww!=':') and (ww!=';'):
            x+=1
    #x+=len(l)
    print(len(l))
avl=float(x)/float(len(sents))
print('Average length of sentence - '+str(avl))

#construct vocabulary
s=set()		#set of vocabulary words
ps=PorterStemmer()

for x in sents:
    pat=r'[\U0001f600-\U0001f650]'
    x1=x.replace('?',' ? ')
    x2=x1.replace(',',' , ')
    x3=x2.replace('!',' ! ')
    x4=x3.replace('.',' . ')
    x5=x4.replace(';',' ; ')
    x7=x5.replace('"','')
    x8=x7.replace('(',' ( ')
    x9=x8.replace(')',' ) ')
    x10=x9.replace('-',' - ')
    x6=x10.replace(':',' : ')
    re.sub(pat,'',x6)
    #l=x6.split()
    l=nltk.word_tokenize(x6)
    #print(l)
    for word in l:
        w2=word.lower()
        w=ps.stem(w2)
        s.add(w)
#vocab creation complete
print('vocabulary length - '+str(len(s)))


targn=0		#number of words in targets
tl=0		#total length of all targets
y=0.0		#sentiment strength of target portion	
for t in targs:

    l1=t.split(',')
    targn+=len(l1)
    for e in l1:

        #tl+=len(e)
        j=nltk.word_tokenize(e)
        for q in j:
            if (q!=',') and (q!='.') and (q!='?') and (q!='!') and (q!='"') and (q!="'") and (q!=')') and (q!='(') and (q!=':') and (q!=';'):
                tl+=1
            q.encode(encoding='utf-8')
            if (q in p) or (q in n):
                y+=1
            # if q in n:
            #     y+=1
            #y+=abs(TextBlob(q).sentiment.polarity)
    print(y)

    #print(tl)
print('no of targets - '+str(targn))
a=float(tl)/float(targn)		#average length of target
print('average length of target - '+str(a))
print(y)
ts_avg=float(y)/float(len(sents)) #avergae target sentiment strength
print('average senti strength of target portion - '+str(ts_avg))


z=0.0		#sentiment strength of text portion beyond target (without target)
for i in range(len(sents)):
    tr=targs[i].split(',')

    words=nltk.word_tokenize(sents[i])
    for w4 in words:
        flag=0
        for c in tr:
            cc=nltk.word_tokenize(c)
            if w4 in cc:
                flag=1
                break
        w4.encode(encoding='utf-8')
        if(flag==0):
            if (w4 in p) or (w4 in n):
                z+=1
        # if(flag==0):
        #     z+=abs(TextBlob(w4).sentiment.polarity)
    print(z)
            # if w in n:
            #     z+=1


savg=float(z)/float(len(sents))		#average senti strength of portion of text without target
print(z)
print('avg senti strength of sentence beyond target - '+str(savg))


