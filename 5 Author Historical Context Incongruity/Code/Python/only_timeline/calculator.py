import codecs
#Files. Change the path before /CD/.../...
# also the paths for tweetnegvalues and tweetposvalues must me changed if you want to use sentiwordlist
neg = codecs.open('/Users/slfrawesome/Desktop/CD/Data/negative','r',encoding= 'utf-8')#output from java program
pos = codecs.open('/Users/slfrawesome/Desktop/CD/Data/positive','r',encoding= 'utf-8')#output from java program
tweetnegvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Data/ntweetsvalue_SAIF','r',encoding= 'utf-8')#non sarcastic test tweets
tweetposvalues = codecs.open('/Users/slfrawesome/Desktop/CD/Data/ptweetsvalue_SAIF','r',encoding= 'utf-8')# sarcastic test tweets
result = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/only_timeline/_only_NNP_SAIF/result','w',encoding= 'utf-8')
stats = codecs.open('/Users/slfrawesome/Desktop/CD/Codes/only_timeline/_only_NNP_SAIF/stats','w',encoding= 'utf-8')#precision and recall store


testvals = []
for line in tweetposvalues:
	vals = line.split()
	#print len(vals)
	testvals.append(int(vals[0])+int(vals[1]))
for line in tweetnegvalues:
	vals = line.split()
	#print len(vals)
	testvals.append(int(vals[0])+int(vals[1]))

#variables
 	# pos = positive  , neg = negative
 	# xxx_yyy  = xxx is the predicted value and yyy is the actual value

pos_pos = 0.0
neg_pos = 0.0
pos_neg = 0.0
neg_neg = 0.0
neu_pos = 0.0
neu_neg = 0.0
posA = []
negA = []
j=0
while j<2278: # 2278 because 2278 timeline. Should be changed when we get more timeline
	posvalues = open('/Users/slfrawesome/Downloads/Intern IITB/PY/only_timeline/_only_NNP_SAIF/tweetsvalue'+str(j)+'.txt','r')
	for line in posvalues:
		vals = line.split()
		if int(vals[2])==1 or int(vals[2])==0 or testvals[j]==0:
			posA.append(0)
		elif testvals[j]>0:
			if int(vals[0])+int(vals[1])<0:
				posA.append(1)
			else:
				posA.append(-1)
		else :
			if int(vals[0])+ int(vals[1])>0:
				posA.append(1)
			else:
				posA.append(-1)
	#print posA
	j+=1
	#print pos_neg , pos_pos
	#print PP , NP
	#print 'PosPrecision = ', (PP)
i=0
for line in pos:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" SAR ") #actual value
	if posA[i]>0:
		result.write("SAR\n") #predicted value
		pos_pos+=1
	else:
		result.write("NSAR\n")#predicted value
		neg_pos+=1
	#else:
	#	result.write("NOTRES\n")
	#	neu_pos+=1
	i+=1
	if i>505:  # only because we have got only 16 global maps
		break
print 'a'
#i=0
for line in neg:
	words = line.split()
	st =''
	for word in words[1:]:
		st = st+" " + word
	result.write(st)
	result.write(" NSAR ")#actual value
	if posA[i]>0:
		result.write("SAR\n")#predicted value
		pos_neg +=1
	else:
		result.write("NSAR\n")#predicted value
		neg_neg +=1
	#else:
	#	result.write("NOTRES\n")
	#	neu_neg +=1
	i+=1
	#if i>(1599):
	#	break
print i
print neu_neg , neu_pos
PP = pos_pos/(pos_pos+pos_neg) #Pos Precision 
NP = neg_neg/(neg_pos+neg_neg) #Neg Precision
PR = pos_pos/(pos_pos+neg_pos+neu_pos) # Pos Recall
NR = neg_neg/(neg_neg+pos_neg+neu_neg) # Neg Recall
#det_pos = (pos_pos+neg_pos+neg_neg+pos_neg)/(pos_pos+neg_pos+neu_pos +neg_neg+pos_neg+neu_neg)

#stats.write("Detection percent = " +str(det_pos)+"\n")
stats.write("Pos Precision = " +str(PP)+"\n")
stats.write("Neg Precision = " +str(NP)+"\n")
stats.write("Pos Recall = " +str(PR)+"\n")
stats.write("Neg Recall = " +str(NR))
