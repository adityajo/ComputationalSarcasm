import codecs

neg = codecs.open('/Users/slfrawesome/Desktop/CD/Data/negative','r',encoding= 'utf-8')
pos = codecs.open('/Users/slfrawesome/Desktop/CD/Data/positive','r',encoding= 'utf-8')
tweetnegvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Data/ntweetsvalue_SAIF','r',encoding= 'utf-8')
tweetposvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Data/ptweetsvalue_SAIF','r',encoding= 'utf-8')
flips_file = codecs.open('/Users/slfrawesome/Desktop/CD/Data/result_NewPhrases_28June_SAIF.txt','r',encoding= 'utf-8')
result = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/Integrator/result_SAIFOR','w',encoding= 'utf-8')
stats = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/Python/Integrator/stats_SAIFOR','w',encoding= 'utf-8')

testvals = []
flips = []
i=0
for line in tweetposvalues:
	vals = line.split()
	testvals.append(int(vals[0])+int(vals[1])) # int(vals[0]) - Total postive sentiment and int(vals[1]) - Total negative sentiment
for line in tweetnegvalues:
	vals = line.split()
	testvals.append(int(vals[0])+int(vals[1]))

for line in flips_file:
	vals = line.split()
	if vals[0]=='SAR':
		flips.append(2)
	else :
		flips.append(-1)
	i+=1
#variables
pos_pos = 0.0
neg_pos = 0.0
pos_neg = 0.0
neg_neg = 0.0
neu_pos = 0.0
neu_neg = 0.0
posA = []
negA = []
j=0
while j<2278: # 16 because 16 global maps. Should be changed when we get more global maps
	posvalues = open('/Users/slfrawesome/Desktop/CD/only_timeline/tweetsvalue'+str(j)+'.txt','r')
	for line in posvalues:
		vals = line.split()
		if int(vals[2])==0:
			posA.append(0)
		elif testvals[j]>0:
			if int(vals[0])+int(vals[1])<0:
				posA.append(2)
			else:
				posA.append(-1)
		elif testvals[j]<0 :
			if int(vals[0])+int(vals[1])>0:
				posA.append(2)
			else:
				posA.append(-1)
		else:
			posA.append(-1)
	#print posA
	j+=1
	
################################################################################################
i=0
for line in pos:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" SAR ")
	if posA[i]+flips[i]>0: # >0 for OR , >2 for AND, >=2 for Relaxed AND
		result.write("SAR\n")
		pos_pos+=1
	else:
		result.write("NSAR\n")
		neg_pos+=1
#	else:
#		result.write("NOTRES\n")
#		neu_pos+=1
	i+=1
	if i>505: 
		break
print 'a'
#i=0
for line in neg:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" NSAR ")
	if posA[i]+flips[i]>0: # >0 for OR , >2 for AND, >=2 for Relaxed AND
		result.write("SAR\n")
		pos_neg+=1
	else:
		result.write("NSAR\n")
		neg_neg+=1
#	else:
#		result.write("NOTRES\n")
	i+=1
	#if i>(1599):
	#	break
print i
PP = pos_pos/(pos_pos+pos_neg)
NP = neg_neg/(neg_pos+neg_neg)
PR = pos_pos/(pos_pos+neg_pos)
NR = neg_neg/(neg_neg+pos_neg)
#det_pos = (pos_pos+neg_pos)/(pos_pos+neg_pos+neu_pos)
#stats.write("Detection percent = " +str(det_pos)+"\n")
stats.write("Pos Precision = " +str(PP)+"\n")
stats.write("Neg Precision = " +str(NP)+"\n")
stats.write("Pos Recall = " +str(PR)+"\n")
stats.write("Neg Recall = " +str(NR))
