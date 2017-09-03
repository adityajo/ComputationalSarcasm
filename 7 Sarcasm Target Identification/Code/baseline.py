import codecs
from textblob import TextBlob
import xlrd
import nltk
from nltk.corpus import stopwords
stop=stopwords.words('english')

path='tweets.xlsx'		#path to the dataset
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]			#text instances of the dataset
actual_targs=[]		#actual targets of the text in dataset

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        actual_targs.append(l[1])

p=open('positive_sent_words.txt','r')		#positive sentiment words lexicon
n=open('negative_sent_words.txt','r')		#negative sentiment words lexicon
p=list(p)
n=list(n)
p=[x[:-1] for x in p]
n=[q[:-1] for q in n]
# p=[y.encode(encoding='utf-8') for y in p]
# n=[e.encode(encoding='utf-8') for e in n]
#print(type(p[0]))
part=0		#count for partial match
partio=0.0	#count for % of words of text in the predicted target for partial match	
full=0		#count for exact match
hm=0.0		#count for dice score

for i in range(len(sents)):
    print(i)
    w=nltk.word_tokenize(sents[i])
    tag=nltk.pos_tag(w)		#pos tags of sentence

    tar=[]			#actual target in form of words only

    e=actual_targs[i].split(',')
    for q in e:
        tar.extend(nltk.word_tokenize(q))

    pred_tar=[]		#predicted target words

    for j in range(len(w)):
        #print(type(str(w[j])))
        #w[j].encode(encoding='utf-8')
        #print(type(w[j]))
        if tag[j][1]=='.' or tag[j][1]==',' or tag[j][1]==':':
            continue
        elif (w[j].lower() in p) or (w[j].lower() in n):
            continue
        # elif abs(TextBlob(w[j]).sentiment.polarity)>0.4:
        #     continue
        # elif tag[j][1]=='PRP' or tag[j][1]=='PRP$':
        #     pred_tar.append(w[j])
        elif w[j].lower() not in stop:
            pred_tar.append(w[j])

    s1=set(tar)
    s2=set(pred_tar)
    print(s1)
    print(s2)
	#bdlow handles outside case
    if 'OUTSIDE/LISTENER' in s1:
        if (len(s2)==0) or ('OUTSIDE/LISTENER' in s2):
            hm+=1.0
            part+=1
            full+=1
    else:
        hm+=(float((2*len(s2.intersection(s1))))/float((len(pred_tar)+len(tar))))
        if s1==s2:
            part+=1
            full+=1
        else:
            if len(s1.intersection(s2))>0:
                part+=1

    print(part)
    print(full)
    print(hm)

    # if s1==s2:
    #     part+=1
    #     full+=1
    # else:
    #     if len(s1.intersection(s2))>0:
    #         part+=1



    partio+=(float(len(pred_tar))/float(len(w)))
    print(partio)

print('Baseline for quotes')
N=len(sents)
partacc=float(part)/float(N)
fullacc=float(full)/float(N)
perc=float(partio)/float(N)
hmean=float(hm)/float(N)

print(partacc)
print(perc)
print(fullacc)
print(hmean)

