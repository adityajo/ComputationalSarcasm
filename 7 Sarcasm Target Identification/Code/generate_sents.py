import xlrd
training_path='quotesA+V.xlsx'		#path to dataset
workbook_train = xlrd.open_workbook(training_path)
worksheet_train = workbook_train.sheet_by_index(0)
rows = []
for i, row in enumerate(range(worksheet_train.nrows)):

    r = []
    for j, col in enumerate(range(worksheet_train.ncols)):
        r.append(worksheet_train.cell_value(i, j))
    rows.append(r)
train_sents=[]		#all text of dataset
train_targs=[]		#all the actual targets

for l in rows:
    if len(l[1])>0:
        train_sents.append(l[0])
        train_targs.append(l[1])

N=len(train_sents)
F=N/4
test_sents=train_sents[:F]
test_targs=train_targs[:F]
print(test_sents)
print(test_targs)
f2=open('quotes_SVMHMM/run4/test_sents.txt','wb')
f2.write(repr(test_sents))
f3=open('quotes_SVMHMM/run4/test_targs.txt','wb')
f3.write(repr(test_targs))
