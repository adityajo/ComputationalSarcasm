from ast import literal_eval
import nltk
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

sents=[]			#texts in dataset
actual_targs=[]		#actual targets

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        actual_targs.append(l[1])

f1=open('tweets_maj_list.txt','r')
f2=open('tweets_weighted_partial_list.txt','r')
f3=open('tweets_weighted_exact_list.txt','r')
f4=open('tweets_weighted_dice_list.txt','r')

# all lists of candidate targets of rule based extractor for comparison with actual targets and results
for line in f1:
    majority_targs=literal_eval(line)
for line in f2:
    wm_partial_targs=literal_eval(line)
for line in f3:
    wm_exact_targs=literal_eval(line)
for line in f4:
    wm_dice_targs=literal_eval(line)


print(actual_targs)
print(majority_targs)
print(wm_partial_targs)
print(wm_exact_targs)
print(wm_dice_targs)

# prm=0.0
# prw=0.0
#
# maj=0
# wmaj=0
#
# hm=0.0
# hw=0.0
maj_part=0
maj_exact=0
maj_dice=0.0
wmaj_part=0
wmaj_exact=0
wmaj_dice=0.0

n=len(actual_targs)

for i in range(n):
    tar=actual_targs[i].split(',')
    ac_tar=[]
    for stt in tar:
        ac_tar.extend(nltk.word_tokenize(stt))
    print(i)
    ws=len(nltk.word_tokenize(sents[i]))

    sa=set(ac_tar)
    print(sa)

    mm=majority_targs[i].split(',')
    wmp=wm_partial_targs[i].split(',')
    wme=wm_exact_targs[i].split(',')
    wmd=wm_dice_targs[i].split(',')

    maj_pred=[]		#predicted target words for majority approach
    wmaj_partial_pred=[]		#predicted target words for rule based (weighted) for partial match
    wmaj_exact_pred=[]			#predicted target words for rule based (weighted) for exact match
    wmaj_dice_pred=[]			#predicted target words for rule based (weighted) for dice score

    for m2 in mm:
        maj_pred.extend(nltk.word_tokenize(m2))
    for wp2 in wmp:
        wmaj_partial_pred.extend(nltk.word_tokenize(wp2))
    for we2 in wme:
        wmaj_exact_pred.extend(nltk.word_tokenize(we2))
    for wd2 in wmd:
        wmaj_dice_pred.extend(nltk.word_tokenize(wd2))

    smaj=set(maj_pred)
    swp=set(wmaj_partial_pred)
    swe=set(wmaj_exact_pred)
    swd=set(wmaj_dice_pred)
    print(smaj)
    print(swp)
    print(swe)
    print(swd)

    if 'OUTSIDE/LISTENER' in sa:
        if (len(smaj)==0) or ('OUTSIDE/LISTENER' in smaj):
            maj_part+=1
            maj_exact+=1
            maj_dice+=1.0
        if (len(swp)==0) or ('OUTSIDE/LISTENER' in swp):
            wmaj_part+=1
        if (len(swe)==0) or ('OUTSIDE/LISTENER' in swe):
            wmaj_exact+=1
        if (len(swd)==0) or ('OUTSIDE/LISTENER' in swd):
            wmaj_dice+=1.0
    else:
        if 'OUTSIDE/LISTENER' in smaj:
            smaj.remove('OUTSIDE/LISTENER')
        if 'OUTSIDE/LISTENER' in swp:
            swp.remove('OUTSIDE/LISTENER')
        if 'OUTSIDE/LISTENER' in swe:
            swe.remove('OUTSIDE/LISTENER')
        if 'OUTSIDE/LISTENER' in swd:
            swd.remove('OUTSIDE/LISTENER')
        if(smaj==sa):
            maj_part+=1
            maj_exact+=1
            maj_dice+=1.0
        elif(len(sa.intersection(smaj))>0):
            maj_part+=1
            maj_dice+=(float(2*(len(sa.intersection(smaj))))/float(len(sa)+len(smaj)))

        if(len(sa.intersection(swp))>0):
            wmaj_part+=1
        if(swe==sa):
            wmaj_exact+=1
        wmaj_dice+=(float(2*(len(sa.intersection(swd))))/float(len(sa)+len(swd)))

    print(maj_part)
    print(maj_exact)
    print(maj_dice)
    print(wmaj_part)
    print(wmaj_exact)
    print(wmaj_dice)

mpacc=float(maj_part)/float(n)		#partial match for majority approach
meacc=float(maj_exact)/float(n)		#exact match for majority approach
mdacc=float(maj_dice)/float(n)		#dice score for majority approach
wmpacc=float(wmaj_part)/float(n)	#partial match for weighted majority approach
wmeacc=float(wmaj_exact)/float(n)	#exact match for weighted majority approach
wmdacc=float(wmaj_dice)/float(n)	#dice score for weighted majority approach


print('\n\n')
print('TWEETS')		#change to snippets when required
print('Majority')
print('Partial match - ',mpacc)
print('Exact match - ',meacc)
print('Dice score - ',mdacc)
print('Weighted Majority')
print('Partial match - ',wmpacc)
print('Exact match - ',wmeacc)
print('Dice score - ',wmdacc)
