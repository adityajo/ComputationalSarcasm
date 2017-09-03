import codecs
#Files. Change the path before /CD/.../...
negvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/flips/ntweetsvalue','r',encoding= 'utf-8')#output from java program
posvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/flips/ptweetsvalue','r',encoding= 'utf-8')#output from java program
neg = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/Data/negative','r',encoding= 'utf-8')#non sarcastic test tweets
pos = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/Data/positive','r',encoding= 'utf-8')# sarcastic test tweets
result = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/flips/result','w',encoding= 'utf-8')
stats = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/flips/stats','w',encoding= 'utf-8') #precision and recall store

#variables
 	# pos = positive  , neg = negative
 	# xxx_yyy  = xxx is the predicted value and yyy is the actual value

pos_pos = 0   
neg_pos = 0
pos_neg = 0
neg_neg = 0

#all data into the format of output
negval = 0.0
posval = 0.0
posA = []
negA = [] 
# reading the the flips for actual sarcastic test tweets
for val in posvalues: 
	print val
	posA.append(int(val[0]))
	if int(val[0]) != 0:
		pos_pos +=1.0
	else :
		neg_pos +=1.0

# reading the the flips for actual non-sarcastic test tweets
for val in negvalues:
	negA.append(int(val[0]))
	if int(val[0]) != 0:
		pos_neg +=1.0
	else :
		neg_neg +=1.0			

PP = pos_pos/(pos_pos+pos_neg) #Pos Precision
NP = neg_neg/(neg_pos+neg_neg) #Neg Precision
PR = pos_pos/(pos_pos+neg_pos) #Pos Recall
NR = neg_neg/(neg_neg+pos_neg) #Neg Recall

print pos_neg , pos_pos
print PP , NP
print 'PosPrecision = %f', (PP)

i=0
for line in pos:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" SAR ")#actual value
	if posA[i]>0:
		result.write("SAR\n") # prediction
	else:
		result.write("NSAR\n") # prediction
	i+=1
i=0
for line in neg:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" NSAR ")#actual value
	if negA[i]>0:
		result.write("SAR\n") # prediction
	else:
		result.write("NSAR\n") # prediction
	i+=1


stats.write("Pos Precision = " +str(PP)+"\n")
stats.write("Neg Precision = " +str(NP)+"\n")
stats.write("Pos Recall = " +str(PR)+"\n")
stats.write("Neg Recall = " +str(NR))
