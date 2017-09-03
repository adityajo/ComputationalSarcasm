from ast import literal_eval
# outfile=open('test.txt','wb')
# outfile.write(repr(['You,I','Calvin',"We're"]))
# outfile.write('\n')
# outfile.write(repr(['I','bag']))
#
# outfile.close()
# f=open('test.txt','rb')
# for line in f:
#     print(literal_eval(line))

import rules_implement as ri
import xlrd
import nltk
path='tweets.xlsx'	#path to dataset
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]		#list of texts in dataset
actual_targs=[]	#list of actual targets

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        actual_targs.append(l[1])

weight_part=[]		#list of 9 weights for partial match
weight_ex=[]		#list of 9 weights for exact match
weight_dice=[]		#list of 9 weights for dice score
f1=open('weighting_results_tweets_normal_partial.txt','rb')
f2=open('weighting_results_tweets_normal_exact.txt','rb')
f3=open('weighting_results_tweets_normal_dice.txt','rb')
for line in f1:
    weight_part.append(line.split(':')[1][1:6])
weight_part=list(map(float,weight_part))
print(weight_part)
for line in f2:
    weight_ex.append(line.split(':')[1][1:6])
weight_ex=list(map(float,weight_ex))
print(weight_ex)
for line in f3:
    weight_dice.append(line.split(':')[1][1:6])
weight_dice=list(map(float,weight_dice))
print(weight_dice)

# N=len(sents)
# F=N/4
# sents=sents[3*F:]
# actual_targs=actual_targs[3*F:]

majority_targs=[]		#majority approach predicted targets for rule based
wm_part_targs=[]		#rule based extractor predicted targets for partial match
wm_ex_targs=[]			#rule based extractor predicted targets for exact match
wm_dice_targs=[]		#rule based extractor predicted targets for dice score

for i in range(len(sents)):
    scoresmaj=[]		#score for the instance in majority approach
    scoreswp=[]			#score for instance for partial match for weighted rule based
    scoreswe=[]			#score for instance for exact match for weighted rule based
    scoreswd=[]			#score for instance for dice score for weighted rule based

    w=nltk.word_tokenize(sents[i])
    print(i)
	#nine lists of predicted targets (for each rule)
    t1=ri.R1(sents[i])
    t2=ri.R2(sents[i])
    t3=ri.R3(sents[i])
    t4=ri.R4(sents[i])
    t5=ri.R5(sents[i])
    t6=ri.R6(sents[i])
    t7=ri.R7(sents[i])
    t8=ri.R8(sents[i])
    t9=ri.R9(sents[i])
    l1,l2,l3,l4,l5,l6,l7,l8,l9=[],[],[],[],[],[],[],[],[]		#these will contain the words in predicted targets

    for x1 in t1:
        l1.extend(nltk.word_tokenize(x1))
    for x2 in t2:
        l2.extend(nltk.word_tokenize(x2))
    for x3 in t3:
        l3.extend(nltk.word_tokenize(x3))
    for x4 in t4:
        l4.extend(nltk.word_tokenize(x4))
    for x5 in t5:
        l5.extend(nltk.word_tokenize(x5))
    for x6 in t6:
        l6.extend(nltk.word_tokenize(x6))
    for x7 in t7:
        l7.extend(nltk.word_tokenize(x7))
    for x8 in t8:
        l8.extend(nltk.word_tokenize(x8))
    for x9 in t9:
        l9.extend(nltk.word_tokenize(x9))


    for j in range(len(w)):
        maj=0		#count for majority approach
        wmaj_part=0.0	#count for partial match for rule based extractor (weighted)
        wmaj_ex=0.0		#count for exact match for rule based extractor (weighted)
        wmaj_dice=0.0	#count for dice score for rule based extractor (weighted)

        if w[j] in l1:
            maj+=1
            wmaj_part+=weight_part[0]
            wmaj_ex+=weight_ex[0]
            wmaj_dice+=weight_dice[0]
        if w[j] in l2:
            maj+=1
            wmaj_part+=weight_part[1]
            wmaj_ex+=weight_ex[1]
            wmaj_dice+=weight_dice[1]
        if w[j] in l3:
            maj+=1
            wmaj_part+=weight_part[2]
            wmaj_ex+=weight_ex[2]
            wmaj_dice+=weight_dice[2]
        if w[j] in l4:
            maj+=1
            wmaj_part+=weight_part[3]
            wmaj_ex+=weight_ex[3]
            wmaj_dice+=weight_dice[3]
        if w[j] in l5:
            maj+=1
            wmaj_part+=weight_part[4]
            wmaj_ex+=weight_ex[4]
            wmaj_dice+=weight_dice[4]
        if w[j] in l6:
            maj+=1
            wmaj_part+=weight_part[5]
            wmaj_ex+=weight_ex[5]
            wmaj_dice+=weight_dice[5]
        if w[j] in l7:
            maj+=1
            wmaj_part+=weight_part[6]
            wmaj_ex+=weight_ex[6]
            wmaj_dice+=weight_dice[6]
        if w[j] in l8:
            maj+=1
            wmaj_part+=weight_part[7]
            wmaj_ex+=weight_ex[7]
            wmaj_dice+=weight_dice[7]
        if w[j] in l9:
            maj+=1
            wmaj_part+=weight_part[8]
            wmaj_ex+=weight_ex[8]
            wmaj_dice+=weight_dice[8]

        scoresmaj.append(maj)
        scoreswp.append(wmaj_part)
        scoreswe.append(wmaj_ex)
        scoreswd.append(wmaj_dice)

    # print(len(w))
    # print(len(scoresm))
    # print(len(scoreswm))

    maxm=max(scoresmaj)
    maxwp=max(scoreswp)
    maxwe=max(scoreswe)
    maxwd=max(scoreswd)
    m=[]		#final words in predicted target for majority approach
    wp=[]		#final words in predicted target for partial match for rule based (weighted)
    we=[]		#final words in predicted target for exact match for rule based (weighted)
    wd=[]		#final words in predicted target for dice score for rule based (weighted)
    for k in range(len(scoresmaj)):
        if(scoresmaj[k]==maxm and scoresmaj[k]!=0):
            m.append(w[k])
        if(scoreswp[k]==maxwp and scoreswp[k]!=0):
            wp.append(w[k])
        if(scoreswe[k]==maxwe and scoreswe[k]!=0):
            we.append(w[k])
        if(scoreswd[k]==maxwd and scoreswd[k]!=0):
            wd.append(w[k])

    if 'OUTSIDE/LISTENER' in l3 or 'OUTSIDE/LISTENER' in l8:
        m.append('OUTSIDE/LISTENER')
        wp.append('OUTSIDE/LISTENER')
        we.append('OUTSIDE/LISTENER')
        wd.append('OUTSIDE/LISTENER')
    print(actual_targs[i])
    print(m)
    print(wp)
    print(we)
    print(wd)
	#comma separated lists of predicted targets; stored and used for evaluation in rule_based_app_evaluation.py
    majority_targs.append(','.join(m))
    wm_part_targs.append(','.join(wp))
    wm_ex_targs.append(','.join(we))
    wm_dice_targs.append(','.join(wd))

    print('\n')

print(actual_targs)
print(majority_targs)
print(wm_part_targs)
print(wm_ex_targs)
print(wm_dice_targs)


f4=open('tweets_maj_list.txt','w')
f5=open('tweets_weighted_partial_list.txt','w')
f6=open('tweets_weighted_exact_list.txt','w')
f7=open('tweets_weighted_dice_list.txt','w')
f4.write(repr(majority_targs))
f5.write(repr(wm_part_targs))
f6.write(repr(wm_ex_targs))
f7.write(repr(wm_dice_targs))