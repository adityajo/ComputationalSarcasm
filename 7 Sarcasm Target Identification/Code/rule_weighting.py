import nltk
import rules_implement as ri
import xlrd

path='tweets.xlsx'		#path to dataset
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]		#text instances of dataset
targs=[]		#all actual targets

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        targs.append(l[1])

#use files for normal or conditional performance of rules accordingly
		
# f1=open('weighting_results_tweets_normal_partial.txt','a')
# f2=open('weighting_results_tweets_normal_exact.txt','a')
# f3=open('weighting_results_tweets_normal_dice.txt','a')
f4=open('weighting_results_tweets_conditional_partial.txt','a')
f5=open('weighting_results_tweets_conditional_exact.txt','a')
f6=open('weighting_results_tweets_conditional_dice.txt','a')

# print sents[0]
# print targs[0]

#one rule at a time, change below

# f1.write('R9: ')
# f2.write('R9: ')
# f3.write('R9: ')
f4.write('R9: ')
f5.write('R9: ')
f6.write('R9: ')


part=0		#partial match
full=0		#exact match
hm=0.0		#dice score
denom=0		#denominator for conditional

for i in range(len(sents)):
    print(i)
    tar=targs[i].split(',')
    print(tar)
    flag=0
    pt=ri.R9(sents[i])		#change rule number accordingly
    print(pt)

    ac_tar=[]		#list of words in actual targets
    pred_tar=[]		#list of words in candidate targets for the rule stores in pt above
    for s1 in tar:
        ac_tar.extend(nltk.word_tokenize(s1))
    for s2 in pt:
        pred_tar.extend(nltk.word_tokenize(s2))

    sa=set(ac_tar)
    sp=set(pred_tar)
    flag=0
    if(len(pred_tar)>0):
        denom+=1
        flag=1
	#handle outside cases first
    if 'OUTSIDE/LISTENER' in sa:
        if (len(sp)==0) or ('OUTSIDE/LISTENER' in sp):
            part+=1
            full+=1
            hm+=1.0
            if(flag==0):
                denom+=1
    else:
        if(sp==sa):
            part+=1
            full+=1
            hm+=1.0
        elif(len(sp.intersection(sa))>0):
            part+=1
            hm+=(float((2*len(sp.intersection(sa))))/float((len(sp)+len(sa))))




    # for x in targ:
    #     for y in a:
    #         if x in y:
    #             flag=1
    #             break
    #     if(flag):
    #         break
    # if(flag):
    #     c1+=1
    print(part)
    print(full)
    print(hm)
    print(denom)
   

n=len(sents)

# acc1=float(part)/float(n)		#partial match for normal
# acc2=float(full)/float(n)		#exact match for normal
# acc3=float(hm)/float(n)		#dice score for normal
acc4=float(part)/float(denom)	#partial match for conditional
acc5=float(full)/float(denom)	#exact match for conditional
acc6=float(hm)/float(denom)		#dice score for conditional

print('\n')

# print(acc1)
# print(acc2)
# print(acc3)
print(acc4)
print(acc5)
print(acc6)

# f1.write(str(acc1)+'\n')
# f2.write(str(acc2)+'\n')
# f3.write(str(acc3)+'\n')
f4.write(str(acc4)+'\n')
f5.write(str(acc5)+'\n')
f6.write(str(acc6)+'\n')

#print(acc1)