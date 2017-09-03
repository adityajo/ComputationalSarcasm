import nltk
from textblob import TextBlob
from nltk.parse.stanford import StanfordDependencyParser
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
import xlrd
from nltk.data import load
from nltk.stem import PorterStemmer
import codecs

import re

# def findWholeWord(w):
#     return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

bf = [0,0,1,0,0,1,0]     #to set the feature combo (1-17) #refer README2 in Results directory file for order of features

training_path='quotesA+V.xlsx'		#tweets.xlsx for tweets dataset
workbook_train = xlrd.open_workbook(training_path)
worksheet_train = workbook_train.sheet_by_index(0)
rows = []
for i, row in enumerate(range(worksheet_train.nrows)):

    r = []
    for j, col in enumerate(range(worksheet_train.ncols)):
        r.append(worksheet_train.cell_value(i, j))
    rows.append(r)
train_sents=[]		#initally has all text
train_targs=[]		#initially has all actual targets

for l in rows:
    if len(l[1])>0:
        train_sents.append(l[0])
        train_targs.append(l[1])

print(train_sents)
print(train_targs)
N=len(train_sents)
F=N/4

run_flag=1          #to decide the fold (1-4)
savepath='quotes_SVMHMM/run'+str(run_flag)+'/'
#below collection of 4 if statements implements the division of text into train and test for the 4 folds
if(run_flag==1):
    test_sents=train_sents[3*F:]
    ts=train_sents[:3*F]
    # tss=train_sents[2*F:]
    # ts.extend(tss)
    train_sents=ts

    test_targs=train_targs[3*F:]
    ts3=train_targs[:3*F]
    # tss=train_targs[2*F:]
    # ts3.extend(tss)
    train_targs=ts3

if(run_flag==2):
    test_sents=train_sents[2*F:3*F]
    ts=train_sents[:2*F]
    tss=train_sents[3*F:]
    ts.extend(tss)
    train_sents=ts

    test_targs=train_targs[2*F:3*F]
    ts3=train_targs[:2*F]
    tss=train_targs[3*F:]
    ts3.extend(tss)
    train_targs=ts3

if(run_flag==3):
    test_sents=train_sents[F:2*F]
    ts=train_sents[:F]
    tss=train_sents[2*F:]
    ts.extend(tss)
    train_sents=ts

    test_targs=train_targs[F:2*F]
    ts3=train_targs[:F]
    tss=train_targs[2*F:]
    ts3.extend(tss)
    train_targs=ts3

if(run_flag==4):
    test_sents=train_sents[:F]
    ts=train_sents[F:]
    # tss=train_sents[2*F:]
    # ts.extend(tss)
    train_sents=ts

    test_targs=train_targs[:F]
    ts3=train_targs[F:]
    # tss=train_targs[2*F:]
    # ts3.extend(tss)
    train_targs=ts3

p=open('positive_sent_words.txt','r')	#lexicon of positive sentiment words
n=open('negative_sent_words.txt','r')	#lexicon of negative sentiment words
p=list(p)
n=list(n)
p=[x[:-1] for x in p]
n=[q[:-1] for q in n]

#produce dictionary for pos tags
tagdict = load('help/tagsets/upenn_tagset.pickle')
l=tagdict.keys()
pos_dic={}
rev_pos_dic={}
for x in range(len(l)):
    pos_dic[x+1]=l[x]
    rev_pos_dic[l[x]]=x+1


s=set()			#set of words in vocabulary
ps=PorterStemmer()

#create vocablulary-
for x in train_sents:
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
    print(l)
    for word in l:
        w2=word.lower()
        w=ps.stem(w2)
        s.add(w)
print(s)
print(len(s))

vocab={}
rev_vocab={}
i=7		#needs to start with 7 as first 6 features are defined
for q in s:
    vocab[i]= q
    rev_vocab[q]=i
    i+=1

print(vocab)
print(rev_vocab)
#vocab created at this point

#fucntion to produce pos tags for the text
def tag(sent):
    words=nltk.word_tokenize(sent)
    tagged=nltk.pos_tag(words)
    return tagged

# print(pos_dic)
# print(rev_pos_dic[pos_dic[9]])

#produce train file (1-17)
def generate_train_file():
    f1=open(savepath+'train_t17.txt','wb') #t1 to t17
    pat=r'[\U0001f600-\U0001f650]'
    for i in range(len(train_sents)):
        print(i)
        #print(train_sents[i])
        #s2=re.sub(pat,'',train_sents[i])
        #print(s2)
        sen=train_sents[i].replace('#','')
        #print(sen)
        tags=tag(sen)		#tags of the text
        words=nltk.word_tokenize(sen)		#words of the text
        print(words)
        for j in range(len(words)):
            #print(words[j])
            flag=0
            tar=train_targs[i].split(',')
            for t in tar:
                if words[j] in t:
                    flag=1
                    break
			#assign label
            if(flag):
                f1.write('2 ')
            else:
                f1.write('1 ')

            f1.write('qid:%d'%(i+1))
			
			#feature 1 - pos tag
            if(bf[0]):
                f1.write(' 1:')
                v1=rev_pos_dic[tags[j][1]]
                f1.write(str(v1))

			#feature 2 - word polarity
            if(bf[1]):
                f1.write(' 2:')
                if words[j] in p:
                    v2=1
                elif words[j] in n:
                    v2=-1
                else:
                    v2=0
                f1.write(str(v2))

			#feature 3 - #capital letters	
            if(bf[2]):
                f1.write(' 3:')
                a=sum(1 for c in words[j] if c.isupper())
                f1.write(str(a))

			#feature 4 - previous pos tag	
            if(bf[3]):
                f1.write(' 4:')
                if j==0:
                    h1=0
                else:
                    h1=rev_pos_dic[tags[j-1][1]]
                f1.write(str(h1))

			#feature 5 - next pos tag	
            if(bf[4]):
                f1.write(' 5:')
                if j==(len(words)-1):
                    h2=0
                else:
                    h2=rev_pos_dic[tags[j+1][1]]
                f1.write(str(h2))

			#feature 6 - phrase polarity	
            if bf[5]:
                f1.write(' 6:')
                if j==0:
                    st=TextBlob(' '.join(words[j:j+2]))
                    h3=st.sentiment.polarity
                elif j==(len(words)-1):
                    st=TextBlob(' '.join(words[j-1:j+1]))
                    h3=st.sentiment.polarity
                else:
                    st=TextBlob(' '.join(words[j-1:j+2]))
                    h3=st.sentiment.polarity
                f1.write(str(h3)[:5])

			#feature 7 - unigram	
            if(bf[6]):
                try:
                    ww=words[j].lower()
                    www=ps.stem(ww)
                    v3=rev_vocab[www]
                    f1.write(' '+str(v3)+':1')
                except:
                    pass

            f1.write(' #'+words[j].encode('utf-8'))
            f1.write('\n')

#produce test file
def generate_test_file():
    f2=open(savepath+'test_t17.txt','wb')  #t1 to t17
    for i in range(len(test_sents)):
        print(i)
        #s2=re.sub(pat,'',test_sents[i])
        sen=test_sents[i].replace('#','')
        tags=tag(sen)
        words=nltk.word_tokenize(sen)
        print(words)
        for j in range(len(words)):
            #print(words[j])
            flag=0
            tar=test_targs[i].split(',')
            for t in tar:
                if words[j] in t:
                    flag=1
                    break
            if(flag):
                f2.write('2 ')
            else:
                f2.write('1 ')

            f2.write('qid:%d'%(i+1))


            if(bf[0]):
                f2.write(' 1:')
                v1=rev_pos_dic[tags[j][1]]
                f2.write(str(v1))

            if(bf[1]):
                f2.write(' 2:')
                if words[j] in p:
                    v2=1
                elif words[j] in n:
                    v2=-1
                else:
                    v2=0
                f2.write(str(v2))

            if(bf[2]):
                f2.write(' 3:')
                a=sum(1 for c in words[j] if c.isupper())
                f2.write(str(a))

            if(bf[3]):
                f2.write(' 4:')
                if j==0:
                    h1=0
                else:
                    h1=rev_pos_dic[tags[j-1][1]]
                f2.write(str(h1))

            if(bf[4]):
                f2.write(' 5:')
                if j==(len(words)-1):
                    h2=0
                else:
                    h2=rev_pos_dic[tags[j+1][1]]
                f2.write(str(h2))

            if bf[5]:
                f2.write(' 6:')
                if j==0:
                    st=TextBlob(' '.join(words[j:j+2]))
                    h3=st.sentiment.polarity
                elif j==(len(words)-1):
                    st=TextBlob(' '.join(words[j-1:j+1]))
                    h3=st.sentiment.polarity
                else:
                    st=TextBlob(' '.join(words[j-1:j+2]))
                    h3=st.sentiment.polarity
                f2.write(str(h3)[:5])

            if(bf[6]):
                try:
                    ww=words[j].lower()
                    www=ps.stem(ww)
                    v3=rev_vocab[www]
                    f2.write(' '+str(v3)+':1')
                except:
                    pass


            f2.write(' #'+words[j].encode('utf-8'))
            f2.write('\n')


generate_train_file()
generate_test_file()