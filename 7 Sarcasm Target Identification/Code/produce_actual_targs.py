import xlrd
import nltk
path='tweets.xlsx'
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)
import NE_extractor as named_entity

rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]		#text in dataset
actual_targs=[]	#actual targets

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        actual_targs.append(l[1])
print(actual_targs)

l=[]		#list of target words, NE for named entity, only for production of word cloud!

for i in range(len(actual_targs)):
    print(i)
    x=actual_targs[i].split(',')
    for j in range(len(x)):
        q=named_entity.ne(x[j])
        z=[]
        for e in q:
            z.extend(e.split(' '))
        s=nltk.word_tokenize(x[j])
        for w in s:
            if w in z:
                l.append('NE')
            elif w!='I':
                l.append(w.lower())
            else:
                l.append(w)

print(l)
print(actual_targs)
y=' '.join(l)
f=open('tweets_targ_sent.txt','w')
f.write(y)
