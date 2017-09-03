for i in range(1,18):
	#for statistical only , use below 3 lines along with hm
    # fa=0.0		#exact match
    # pa=0.0		#partial match
    # perc=0.0		#% of words of sentence in target
	
	#use below three lines for hybrid approach
    pa=0.0		#partial match
    ea=0.0		#exact match
    hm=0.0		#dice score
    for j in range(1,5):

        f1=open('run'+str(j)+'/PARTIAL_i34res_AND_t'+str(i)+'.txt','r')
        f2=open('run'+str(j)+'/EXACT_i34res_AND_t'+str(i)+'.txt','r')
        f3=open('run'+str(j)+'/DICE_i34res_AND_t'+str(i)+'.txt','r')
		#above 3 for hybrid
		#below line for partial and exact match of statistical
		# f1=open('run'+str(j)+'/res_t'+str(i)+'.txt','r')
		#below line for dice score only for statistical
		# f1=open('run'+str(j)+'/harmonic_res_t'+str(i)+'.txt','r')
        l1=list(f1)
        l2=list(f2)
        l3=list(f3)
        pa+=float(str(l1[0][:-1]))
        ea+=float(l2[0][:-1])
        hm+=float(str(l3[0][:-1]))
		#above 3 for hybrid, below 3 for statistical (use hm in both)
		# pa+=float(str(l1[1][:-1]))
		# perc+=float(str(l[4])[:-1])
        # fa+=float(str(l[3])[:-1])

    x=float(pa)/float(4)
    # z=float(perc)/float(4)
    y=float(ea)/float(4)
	# y=float(fa)/float(4)
    v=float(hm)/float(4)
    print(x)
    print('\n')
    print(y)
    print('\n')
    # print(z)
    #print(y)
    # print('\n')
    print(v)
	#for hybrid - 
    f4=open('PARTIAL_i34_AND_results_t'+str(i)+'.txt','w')
    f5=open('EXACT_i34_AND_results_t'+str(i)+'.txt','w')
    f6=open('DICE_i34_AND_results_t'+str(i)+'.txt','w')
    f4.write(str(x))
    f5.write(str(y))
    f6.write(str(v))
	
	#for partial and exact match of statistical - 
	# f2=open('results_t'+str(i)+'.txt','w')
	# f2.write(str(x)+'\n')
    # f2.write(str(y)+'\n')
    # f2.write(str(z))
	
	#for dice score of statistical
	# f2=open('harmonic_results_t'+str(i)+'.txt','w')
	# f2.write(str(v))