import xlrd
import nltk
path='quotesA+V.xlsx'		#set path to dataset
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

rows = []
for i, row in enumerate(range(worksheet.nrows)):

    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

sents=[]		#all text in dataset
actual_targs=[]	#actual targets 

for l in rows:
    if len(l[1])>0:
        sents.append(l[0])
        actual_targs.append(l[1])
print(actual_targs)

c=0		#count of outside cases
for x in actual_targs:
    l=x.split(',')
    if 'OUTSIDE/LISTENER' in l:
        c+=1
        print(c)

print('outside in quotes : ',c)