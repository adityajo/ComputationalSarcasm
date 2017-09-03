import sys

o = open(sys.argv[2],'w')
with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip('\n')
		if len(line) > 0:
			o.write(line+'\n')
o.close()
