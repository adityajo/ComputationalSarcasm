import sys
from ast import literal_eval
import nltk
#below function requires a run flag (runf) (1-4) for the four folds, and tf is flag for feature combination (1-17)
def getr(runf,tf):

    f1=open('classification_tweets/run'+str(runf)+'/test_sents.txt','r')
    f2=open('classification_tweets/run'+str(runf)+'/test_targs.txt','r')
    for l1 in f1:
        test_sents=literal_eval(l1)

    for l2 in f2:
        test_targs=literal_eval(l2)

    #print(test_sents)
    #print(test_targs)

    f3=open('classification_tweets/run'+str(runf)+'/use_t'+str(tf)+'.txt','r')
    pred=[]		#list of predicted label
    words=[]	#list of word corresponding to above label
    for line in f3:
        #line.strip('\n')
        l1=line.split('\t')
        pred.append(l1[0])
        s=l1[1]
        l=s.split(' ')
        words.append(l[-1][1:-1])
    pred=list(map(float,pred))
    #print(pred)
    #print(words)

    x,y=0,0		#markers for beginning and end of that sentence, to break the collection of words sentence wise
    part,full=0,0 #cound of partial and exact match

    partio=0.0		#% of words in sentence also in predicted target for partial match

    hm=0.0			#count for dice score

    for i in range(len(test_sents)):
        sen=test_sents[i].replace('#','')
        w=nltk.word_tokenize(sen)
        x=y
        y=x+len(w)

        p=pred[x:y]		#list of predictions for the particular text instance
        p1=[]
        tar=test_targs[i].split(',')	#actual targets
        ww=words[x:y]
        #print(ww)
        p1=[k for k in range(len(p)) if p[k]>0]
        pred_tar=[ww[z] for z in p1]		#words in predicted targets

        ws=len(w)
        wt=len(set(pred_tar))
        partio+=(float(wt)/float(ws))

        #print(pred_tar)
        ac_tar=[]		#words in actual targets
        for s in tar:
            ac_tar.extend(nltk.word_tokenize(s))
        #print(ac_tar)
        pt=pred_tar
        at=ac_tar
        for xx in pt:
            if xx=='.':
                pt.remove(xx)
        sp=set(pt)
        sa=set(at)
		#outside case handled first only for dice score, then for partial and exact match
        if 'OUTSIDE/LISTENER' in sa:
            if (len(sp)==0) or ('OUTSIDE/LISTENER' in sp):
                hm+=1.0
        else:
            hm+=(float((2*len(sp.intersection(sa))))/float((len(sp)+len(sa))))
        print(hm)


        if 'OUTSIDE/LISTENER' in tar:
            if len(pred_tar)==0:
                part+=1
                full+=1
            else:
                if len(ac_tar)>1:
                    for h in pred_tar:
                        if (h in ac_tar) and (h!='a') and (h!='.'):
                            part+=1
                            break
        else:
            if set(ac_tar)==set(pred_tar):
                full+=1
                part+=1

            else:
                #print(1)
                flag=0
                for v in pred_tar:
                    #print(v)
                    if (v in ac_tar) and (v!='a') and (v!='.'):
                        flag=1
                        break
                if(flag):
                    part+=1

    n=len(test_sents)
    partacc=float(part)/float(n) #partial match 

    percs=float(partio)/float(n)	#% of partial score not requirede in final draft

    fullacc=float(full)/float(n)		#exact match 

    hmean=float(hm)/float(n)		#dice score
    f4=open('classification_tweets/run'+str(runf)+'/harmonic_res_t'+str(tf)+'.txt','w') #only res for partial and exact match
    # f4.write(str(part))
    # f4.write('\n')
    # f4.write(str(partacc))
    # f4.write('\n')
    # f4.write(str(full))
    # f4.write('\n')
    # f4.write(str(fullacc))
    # f4.write('\n')
    # f4.write(str(percs))
    f4.write(str(hmean))

#getr(1,1)
#getr(sys.argv[0],sys.argv[1])
