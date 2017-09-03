import os

testdirectory = './'

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if current_file.replace('./','') == 'test_t24.q':
    	seq_no = 1
    	op = open(current_file.replace('.q','.feat'),'w')
    	with open(current_file, 'r') as f:
    		for line in f:
    			line = line.strip('\n')
    			if line[0] != '#':
    				line = line.split('#')[0]
    				feat = []
    				for val in line.split():
    					if 'qid' in val:
    						sno = int(val.split(':')[1])
    						if sno != seq_no:
    							seq_no = sno
    							op.write('\n')
    					else:
    						feat.append(val)
    				op.write(' '.join(feat))			
    				op.write('\n')
    	op.close()		

