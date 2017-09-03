import codecs
f=codecs.open('tweets_SVMHMM/run1/train_t15.txt','r',encoding='utf-8')
w=codecs.open('classification_tweets/run1/train_t15.txt','w',encoding='utf-8')

for line in f:
    l=line.split(' ')
	#change label 2 to 1 ; 1 to -1 for svm perf
    if l[0]=='2':
        l[0]=str(1)
    elif l[0]=='1':
        l[0]=str(-1)
    l.remove(l[1])     #remove the qid field
    #print(l)
    w.write(' '.join(l))