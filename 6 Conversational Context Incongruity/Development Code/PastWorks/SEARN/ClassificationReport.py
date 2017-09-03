import sys
from sklearn.metrics import classification_report

gold = []
pred = []

with open(sys.argv[1], 'rb') as f:
	for line in f:
		line = line.strip('\n')
		line = line.split('\t')
		gold.append(line[0])
		pred.append(line[1])

print classification_report(gold, pred)
