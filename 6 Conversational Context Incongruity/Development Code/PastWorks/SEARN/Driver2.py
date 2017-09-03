import os
import sys
from sklearn.metrics import classification_report

testdirectory = './'
op = open('searnresults_run1.txt','w')

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if 'train_t' in current_file and '.feat' in current_file:
    	trainfile = current_file
    	testfile = current_file.replace('train','test')
    	os.system("./SearnLabel.pl 5 0.05 "+trainfile+" "+testfile)
    	os.system("cut -d' ' -f1 "+testfile+" > test.txt")
    	os.system("python removeblanks.py log.txt pred.txt")
    	os.system("python removeblanks.py test.txt actual.txt")
    	os.system("paste actual.txt pred.txt > labels")
    	gold = []
    	pred = []
    	with open('labels', 'rb') as f:
			for line in f:
				line = line.strip('\n')
				line = line.split('\t')
				gold.append(line[0])
				pred.append(line[1])
        op.write(current_file+'\n')
        op.write(classification_report(gold, pred))
op.close()