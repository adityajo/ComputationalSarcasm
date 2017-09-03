from ast import literal_eval
import nltk
#below function requires a run flag (runf) (1-4) for the four folds, and tf is flag for feature combination (1-17)
def getr(runf,tf):


    f1=open('tweets_weighted_partial_list.txt','r')		#weights of 9 rules for partial match
    f2=open('tweets_weighted_exact_list.txt','r')		#weights of 9 rules for exact match
    f3=open('tweets_weighted_dice_list.txt','r')		#weights of 9 rules for dice score
    fg=open('tweets_or_outside_tweets_indices_correct.txt','w') #to store the indices of correct instances of outside detection for hybrid or

    for line in f1:
        partial_targs=literal_eval(line)		#candidate targets of rule based extractor for partial match
    for line in f2:
        exact_targs=literal_eval(line)			#candidate targets of rule based extractor for exact match
    for line in f3:
        dice_targs=literal_eval(line)			#candidate targets of rule based extractor for dice score

    N=506			#224 for snippets
    F=N//4
    # print(F)
	#below collection of 4 if statements implements the division of targets according to fold runf
    if(runf==1):
        partial=partial_targs[3*F:]
        exact=exact_targs[3*F:]
        dice=dice_targs[3*F:]
    if(runf==2):
        partial=partial_targs[2*F:3*F]
        exact=exact_targs[2*F:3*F]
        dice=dice_targs[2*F:3*F]
    if(runf==3):
        partial=partial_targs[F:2*F]
        exact=exact_targs[F:2*F]
        dice=dice_targs[F:2*F]
    if(runf==4):
        partial=partial_targs[:F]
        exact=exact_targs[:F]
        dice=dice_targs[:F]

    g1=open('classification_tweets/run'+str(runf)+'/test_sents.txt','r')
    g2=open('classification_tweets/run'+str(runf)+'/test_targs.txt','r')
    for l1 in g1:
        test_sents=literal_eval(l1)

    for l2 in g2:
        test_targs=literal_eval(l2)

    #print(test_sents)
    #print(test_targs)
    #print(actual_targs[3*F:])

    g3=open('classification_tweets/run'+str(runf)+'/use_t'+str(tf)+'.txt','r')
    pred=[]
    words=[]
    for line in g3:
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
    partout,fullout,hmout=0,0,0		#count for outside cases

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
        pred_tar=[ww[z] for z in p1]		#words in predicted targets for statistical
		
		#for rule based below 3 lines
        lpart=[]		#predicted targets for partial match
        lex=[]			#predicted targets for exact match
        ldice=[]		#predicted targets for dice score

        l1=partial[i].split(',')
        l2=exact[i].split(',')
        l3=dice[i].split(',')

        for e1 in l1:
            lpart.extend(nltk.word_tokenize(e1))
        for e2 in l2:
            lex.extend(nltk.word_tokenize(e2))
        for e3 in l3:
            ldice.extend(nltk.word_tokenize(e3))

        #pred_tar=list(set(pred_tar).intersection(set(l2)))
		
		#hybrid
        #use intersection for AND ; union for OR in below 3 statements
        pred_tar_partial=list(set(pred_tar).intersection(set(lpart)))
        pred_tar_exact=list(set(pred_tar).intersection(set(lex)))
        pred_tar_dice=list(set(pred_tar).intersection(set(ldice)))

        #print(pred_tar)

        # ws=len(w)
        # wt=len(set(pred_tar))
        # partio+=(float(wt)/float(ws))

        ac_tar=[]		#actual target words
        for s in tar:
            ac_tar.extend(nltk.word_tokenize(s))
        #print(ac_tar)

        # at=ac_tar
        for xx1 in pred_tar_partial:
            if xx1=='.':
                pred_tar_partial.remove(xx1)
        for xx2 in pred_tar_exact:
            if xx2=='.':
                pred_tar_exact.remove(xx2)
        for xx3 in pred_tar_dice:
            if xx3=='.':
                pred_tar_dice.remove(xx3)


        sa=set(ac_tar)
        sp=set(pred_tar_partial)
        se=set(pred_tar_exact)
        sd=set(pred_tar_dice)

		#handling of outside case
        if 'OUTSIDE/LISTENER' in sa:
            if (len(sp)==0) or ('OUTSIDE/LISTENER' in sp):
                part+=1
                partout+=1
                fg.write(str(i)+' part')
            if (len(se)==0) or ('OUTSIDE/LISTENER' in se):
                full+=1
                fullout+=1
                fg.write(str(i)+' exact')
            if (len(sd)==0) or ('OUTSIDE/LISTENER' in sd):
                hm+=1.0
                hmout+=1
                fg.write(str(i)+' dice')
        else:
            if(sa==se):
                full+=1
            if(len(sa.intersection(sp))>0):
                part+=1
            hm+=(float((2*len(sa.intersection(sd))))/float((len(sd)+len(sa))))
        # print(part)
        # print(full)
        # print(hm)




    n=len(test_sents)
    # print(n)
    # print(part)
    partacc=float(part)/float(n)

    #percs=float(partio)/float(n)

    fullacc=float(full)/float(n)

    hmean=float(hm)/float(n)

    print(partacc)
    print(fullacc)
    print(hmean)
    f4=open('classification_quotes/run'+str(runf)+'/PARTIAL_i34res_AND_t'+str(tf)+'.txt','w') #record partial match for fold runf for feature combo tf
    f5=open('classification_quotes/run'+str(runf)+'/EXACT_i34res_AND_t'+str(tf)+'.txt','w')   #record exact match for fold runf for feature combo tf
    f6=open('classification_quotes/run'+str(runf)+'/DICE_i34res_AND_t'+str(tf)+'.txt','w')    #record dice score for fold runf for feature combo tf
    # # f4.write(str(part))
    # # f4.write('\n')
    # # f4.write(str(partacc))
    # #
    # # f4.write('\n')
    # # f4.write(str(percs))
    #
    # # f4.write('\n')
    # # f4.write(str(full))
    # # f4.write('\n')
    # # f4.write(str(fullacc))
    f4.write(str(partacc))
    f5.write(str(fullacc))
    f6.write(str(hmean))
	#results recorded for hybrid above
	#printed for only outside below
    print('tweets')
    print(partout)
    print(fullout)
    print(hmout)


#getr(1,1)