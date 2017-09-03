package hello  ;
import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.concurrent.Semaphore;

public class mymodel {
	
	public Double[] iterationvals ;

	public static int Z; // number of topics
	public int W; // vocabulary
	public static int D; // number of documents
	private static long N; // total word occurrences
	private static int L ; // labels
	private static int S ; // number of sentiment

	private  long[][] Nd_z_l ; // Count document level topic and label
	private  long[] Nd_l ; // Count document level label
	private  long[][][] Nws_s_zl ; //Count word level sentiment topic and label
	private  long[][] Nws_zl ; // Count word level topic and label
	private  long[][][] Nws_w_zs; //count word wi with sentiment s topic z
	private long[][]  Nws_zs ; //count words with topic z sentiment s
	private long[][] Nws_s_l ; // count words with sentiment s and label l 
	private long[] Nws_l ; // count words with label l (sentiment words only)
	private long[][] Nws_w_s; //Count times word w occurs as sentiment with sentiment s
	private long[] Nws_s ; // count times sentiment s occurs
	private long[][] Nwt_w_z ; //count word w with topic z 
	private long[] Nwt_z ; //count words with topic z
	private String[] map_id_word ; //mapping between id and word
	
	public Output[] outputs ; // to store output of each file
	
	
	private int[][] is_di; // Switch for dth document ith word
	private int[][] sentiment ; //Sentiment of dth document ith word
	
	private double[] is_w ; //switch distro for each word
	
	public int[] label ; // label of dth document
	public int[] topic ; //topic of dth document

	public HashMap<Integer, Integer> senti_prior ; // Hardcoding positive and negative words
	
	public double[][] P_z_l ; //P(z/l)
	public double[][][] P_s_zl ;//P(s/zl)
	public double[][] P_w_z ; //P(w/z)
	public double[][][] P_w_zs ;//P(w/zs)
	public double[][] P_s_l ; //P(s/l)
	public double[][] P_w_s ; //P(w/s)
	
	
	public int[] positive_words,negative_words ; //harcoded positive and negative words
	public double[] P_l , P_z ; // P(l) , P(z)
	
	String path_result_prefix = "/home/development/prayas/topic-model-data/results/result-" ; 
	String path_result ;
	WriteFile writer ;
	
	public int[][] w_di; // w_di[d][i] = i'th word in the d'th document

	public int num_samples; 
	
	private double alpha_num , //priors 
				alpha_den , 
				
				beta_2_num,
				beta_2_den , 
				gamma_num , 
				gamma_den , 
				delta_1_num , 
				delta_1_den , 
				delta_2_num ,
				delta_2_den ;

	
	private double[][] beta_1_num ; 
	private double[] beta_1_den ;
	
	public int[][] test_data ;
	public int[] test_label ;
	
	
	//loads the hardcoded words, and test data
	public mymodel(HashMap<String, Integer> hm,int[][] test_data,int[] test_label){
		
		this.test_data = test_data ;
		this.test_label = test_label ;
		System.out.println("Size"+String.valueOf(test_data.length));
		String path_words="/home/development/prayas/topic-model-data/support/" ;
		senti_prior = new HashMap<Integer, Integer>(); 
		positive_words=loadpriors(path_words+"positive-prior",hm) ;
		negative_words=loadpriors(path_words+"negative-prior",hm) ;
		System.out.println("loaded") ;
		for(int i=0;i<positive_words.length;i++){
		//	System.out.println(String.valueOf(i)+" "+String.valueOf(positive_words[i])) ;
			senti_prior.put(positive_words[i], 0) ; 
		}
		for(int i=0;i<negative_words.length;i++){
			//	System.out.println(String.valueOf(i)+" "+String.valueOf(positive_words[i])) ;
				senti_prior.put(negative_words[i], 1) ; 
			} 
		/*for (Integer name: senti_prior.keySet()){

            String key =name.toString();
            String value = senti_prior.get(name).toString();  
            System.out.println(key + " " + value);  

		} */
		
	}
	//loads the harcoded words, in an array
	int[] loadpriors( String fpath,HashMap<String, Integer> hm){
		ReadFile file = new ReadFile(fpath) ;
		int[] words=null ;
		try {
			String[] swords= file.OpenFile();
			words = new int[swords.length] ;
			for(int i=0;i<swords.length;i++){
				if(hm.containsKey(swords[i])) {
					words[i] = hm.get(swords[i]) ;
					//System.out.println(swords[i]+String.valueOf(words[i])); 
				}else{
					//System.out.println("--"+swords[i]+"--") ;
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			
		}
		return words ;
	}
	//loads the data in an svm format, with its features
	public void createdata_svm(int[][] w_di ,int[] label,int[] topic , double[][] P_l_z, double[][][] P_s_zl , int[] positive , int [] negative,
			String suffix, int type){
		WriteFile writeme = null ;
		if(type==0)
			writeme = new WriteFile("/home/development/prayas/topic-model-data/svmdata/traindata-"+suffix) ;
		else if(type==1)
			writeme = new WriteFile("/home/development/prayas/topic-model-data/svmdata/testdata-"+suffix) ;
		
		for(int d=0;d<w_di.length;d++){
			String w="" ;
			for(int i=0;i<w_di[d].length;i++){
				w=w+map_id_word[w_di[d][i]]+" " ;
			}
			w=w+"z:"+String.valueOf(topic[d])+" " ;
			w=w+"lz0:"+String.valueOf(P_l_z[0][topic[d]])+" lz1:"+String.valueOf(P_l_z[1][topic[d]])+
					" lz2:"+String.valueOf(P_l_z[2][topic[d]])+" ";
			w=w+"szl00:"+String.valueOf(P_s_zl[0][topic[d]][0])+ 
				" szl01:"+String.valueOf(P_s_zl[0][topic[d]][1])+
				" szl02:"+String.valueOf(P_s_zl[0][topic[d]][2])+
				" szl10:"+String.valueOf(P_s_zl[1][topic[d]][0])+
				" szl11:"+String.valueOf(P_s_zl[1][topic[d]][1])+
				" szl12:"+String.valueOf(P_s_zl[1][topic[d]][2])+" " ;
			w=w+"S:"+String.valueOf(positive[d]+negative[d])+" " ;
			if((positive[d]+negative[d])==0){
				w=w+"s0:"+String.valueOf(0)+
					" s1:"+String.valueOf(0) ;							
			}else {
				w=w+"s0:"+String.valueOf((double)positive[d]/(double)(positive[d]+negative[d]))+
						" s1:"+String.valueOf((double)negative[d]/(double)(positive[d]+negative[d])) ;
			}
			if(label!=null){
				w=w+"\t"+String.valueOf(label[d]) ;
			}
			try {
				writeme.write(w) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
				
		}
		
	}
	
	//prediction using sampling method
	public int[] predict_sampleL(int[][] w_di,int[] test_label, double[][] P_z_l, double[][][] P_s_zl , double[][][] P_w_zs,
			double[][] P_w_z,double[][] P_l_z, String suffix){
		

		WriteFile writef = new WriteFile("/home/development/prayas/topic-model-data/results/fscore2/fscore2-"+suffix) ;
		WriteFile writell = new WriteFile("/home/development/prayas/topic-model-data/results/logtest/log-"+suffix) ;
		int iterations =20 ;
		int[] output  = new int[w_di.length] ;
		int[] topicz = new int[w_di.length] ;
		int[] NdL = new int[L] ; 
		int Nd = w_di.length ;
		
		int[][] s_di = new int[w_di.length][]  ;
		int[][] is_di =new int[w_di.length][] ;
		
		double lpriornum = 10 ;
		double lpriorden = 10*L ;
		
		for(int i=0;i<output.length;i++){
			output[i]= (int) Math.random()*L ;
			topicz[i] =(int) Math.random()*Z ;
			NdL[output[i]]++ ; 
		}
		
		for(int d=0;d<w_di.length;d++){
			s_di[d]  = new int[w_di[d].length] ;
			is_di[d]  = new int[w_di[d].length] ;
			for(int i=0;i<w_di[d].length;i++){
				int word = w_di[d][i] ;
				double val = Math.random();
				if(is_w[word]>val)
					is_di[d][i] =0 ;
				else
					is_di[d][i] =1 ;
				if(senti_prior.containsKey(w_di[d][i]))
				{	
					if(senti_prior.get(w_di[d][i])==1)
							s_di[d][i]=1 ;
					else
							s_di[d][i]= 0;
				}
				else
					s_di[d][i]= (int) (Math.random()*S) ;
			
			}
		}
		
		//beginsampling
		for(int iter =0;iter<iterations ;iter++){
			double ll = 0.0d ;
			for(int d=0;d<w_di.length;d++){
				NdL[output[d]]-- ;
				double[][] plz = new double[L][Z] ;
				double total = 0 ;
				for(int l=0;l<L;l++){
					for(int z=0;z<Z;z++){
						plz[l][z]= (NdL[l]+lpriornum)/(Nd+lpriorden) ;
						plz[l][z] = plz[l][z]*P_z_l[z][l] ;
						for(int i = 0 ;i<w_di[d].length;i++){
							if(is_di[d][i]==1){
								plz[l][z]*=P_s_zl[s_di[d][i]][z][l] ;
								plz[l][z]*=P_w_zs[w_di[d][i]][z][s_di[d][i]] ;
							}else{
								plz[l][z]*=P_w_z[w_di[d][i]][z] ;
							}
						}
						total +=plz[l][z] ;
					}
				}
				int l=0,z=0 ;
				double val = Math.random()*total ;
				while((val-=plz[l][z])>0){
					if(z==Z-1){
						l++ ;
						z=0;
					}else{
						z++ ;
					}
				}
				NdL[l]++ ;
				output[d] = l ;
				topicz[d]= z ;
				ll+=Math.log(plz[l][z]) ;
				
				for(int i=0;i<w_di[d].length;i++){
					val = Math.random() ;
					if(val<is_w[w_di[d][i]])
					{
						is_di[d][i]=0 ;
						s_di[d][i]=-1 ;
						ll+=Math.log(P_w_z[w_di[d][i]][topicz[d]]) ;
					}
					else
						{
							is_di[d][i]=1; 
							val = Math.random() ;
							s_di[d][i]= 0 ;
							while((val-=P_s_zl[s_di[d][i]][topicz[d]][output[d]] )>0) s_di[d][i]++ ;
						
							ll+=Math.log(P_s_zl[s_di[d][i]][topicz[d]][output[d]]) ;
							ll+=Math.log(P_w_zs[w_di[d][i]][topicz[d]][s_di[d][i]]) ;
						}
				}
			}
			
			int tp=0,tn=0,fp=0,fn=0 ;
			double precision =0.0d , recall = 0.0d , fscore=0.0d , nprecision = 0.0d ,nrecall=0.0d;
			
			for(int i=0;i<w_di.length;i++){
				int op = output[i];
				if(op==test_label[i]&&op==2)
					tp++;
				else if(op==test_label[i]&&op!=2)
					tn++;
				else if(op!=test_label[i]&&op==2)
					fp++;
				else
					fn++;
			}
			precision = (double)tp/(double)(tp+fp) ;
			
			recall=(double)tp/(double)(tp+fn);
			fscore = (2*precision*recall)/(precision+recall) ;
			nprecision = (double)tn/(double)(tn+fn) ;
			nrecall = (double)tn/(double)(tn+fp) ;
			
			writef.open();
			writell.open() ;
			try { 
				writef.write(String.valueOf(fscore)+" "+String.valueOf(precision)+" "+String.valueOf(recall)+" "
						+String.valueOf(nprecision)+" "+String.valueOf(nrecall));
				writef.close();
				writell.write(String.valueOf(ll));
				writell.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}
		
		
		int[] positive = new int[w_di.length] ;
		int[] negative = new int[w_di.length] ;
		for(int d=0;d<w_di.length;d++){
			int pos =0 ;
			int neg =0 ;
			for(int i=0;i<w_di[d].length;i++){
				if(s_di[d][i]==0)
					pos++ ;
				else if(s_di[d][i]==1)
					neg++ ;
				
			}
			positive[d]=pos ;
			negative[d] = neg ;
		
		}
		createdata_svm(w_di, test_label, topicz, P_l_z, P_s_zl, positive, negative, suffix,1);
		return  output ;
	}
	//to predict on a single tweet, ll based
	public int predict(int[] w_i){
		double[] ll = new double[L] ;
		int iterationcount =10 ;
		for(int l=0;l<L;l++){
			
			for(int iteration =0 ;iteration<iterationcount;iteration++){
					int z;
					double val = Math.random() ;
					double llt = 0.0d ;
					z=0;while ((val -= P_z_l[z][l]) > 0) z++;
					
					llt+= Math.log(P_z_l[z][l]) ;
					for(int i=0;i<w_i.length;i++){
						int w= w_i[i] ;
						int is,s ;
						val=Math.random();
						if(val<is_w[w]){
							is=0 ;
							s=-1 ;
							llt+=Math.log(is_w[w]) ;
							llt+= Math.log(P_w_z[w][z]) ;
						}else {
							is=1 ;
							llt+=Math.log(1.0d-is_w[w]) ;
							val = Math.random() ;
							s=0 ;while((val-=P_s_zl[s][z][l])>0)s++ ;
							//	P_s_zl
							llt+=Math.log(P_s_zl[s][z][l]) ;
							llt+=Math.log(P_w_zs[w][z][s]) ;
						}
						
					}
					
					//System.out.println(llt) ;
					if(iteration==0){
						ll[l]=llt ;
					}else{
						ll[l]=Math.max(ll[l],llt) ;
					}
					
			}
			//System.out.println("-NEXT-") ;
		}
		//System.out.println(Arrays.toString(ll)) ;
		int ans=0;
		double valans=ll[0] ;
		for(int l=1;l<L;l++){
			if(ll[l]>valans){
				valans=ll[l]; 
				ans=l ;
			}
		}
		return ans ;
	}
	
	//Predict entire test data, ll based
	public int predict2(int[] w_i,double[][]P_z_l,double[][] P_w_z,double[][][] P_s_zl,
			double[][][] P_w_zs){
		double[] ll = new double[L] ;
		int iterationcount =10 ;
		for(int l=0;l<L;l++){
			
			for(int iteration =0 ;iteration<iterationcount;iteration++){
					int z;
					double val = Math.random() ;
					double llt = 0.0d ;
					z=0;while ((val -= P_z_l[z][l]) > 0) z++;
					
					llt+= Math.log(P_z_l[z][l]) ;
					for(int i=0;i<w_i.length;i++){
						int w= w_i[i] ;
						int is,s ;
						val=Math.random();
						if(val<is_w[w]){
							is=0 ;
							s=-1 ;
							llt+=Math.log(is_w[w]) ;
							llt+= Math.log(P_w_z[w][z]) ;
						}else {
							is=1 ;
							llt+=Math.log(1.0d-is_w[w]) ;
							val = Math.random() ;
							s=0 ;while((val-=P_s_zl[s][z][l])>0)s++ ;
							//	P_s_zl
							llt+=Math.log(P_s_zl[s][z][l]) ;
							llt+=Math.log(P_w_zs[w][z][s]) ;
						}
						
					}
					
					//System.out.println(llt) ;
					if(iteration==0){
						ll[l]=llt ;
					}else{
						ll[l]=Math.max(ll[l],llt) ;
					}
					
			}
			//System.out.println("-NEXT-") ;
		}	
		//System.out.println(Arrays.toString(ll)) ;
		int ans=0;
		double valans=ll[0] ;
		for(int l=1;l<L;l++){
			if(ll[l]>valans){
				valans=ll[l]; 
				ans=l ;
			}
		}
		return ans ;
	}
	
	//print top topic words
	public void print_topicwords(int count, int z){
		double[] p = new double[W] ;
		for(int w=0;w<W;w++){
			p[w]= (double)(Nwt_w_z[w][z]+gamma_num)/
					(Nwt_z[z]+gamma_den) ;
			
		}
		
		ArrayIndexComparator3 compare = new ArrayIndexComparator3(p) ;
		Integer[] indexes = compare.createIndexArray() ;
		Arrays.sort(indexes,compare) ;
		//for(int i=0;i<indexes.length;i++){
			//indexes[i]=indexes[i]+1 ;
	//	}
		String ww="" ;
		for(int i=0;i<count;i++){
			ww+=map_id_word[indexes[i]]+" ";
		}
		System.out.println(ww);
		
		
	}
	
	//estimation and training of the model
	public void estimate(int[] label, int[][] w_di,double[] is_w, String[] map_id_word, int W, int D, int Z, int L, int S ,  int burnIn, int samples, int step,int result_path_suffix,int count,
			
			double an, double ad, double[][] b1n, double[] b1d,double b2n, double b2d, double gn, double gd, 
			
			double d1n, double d1d,double d2n, double d2d	) {
		System.out.println("Estimation started!");
		
		outputs = new Output[burnIn+samples*step] ;
		
		WriteFile fscorewrite = new WriteFile("/home/development/prayas/topic-model-data/results/fscore/fscore-"+String.valueOf(result_path_suffix));

		path_result = path_result_prefix + String.valueOf(result_path_suffix) + ".txt" ;
		writer = new WriteFile(path_result) ;
		
		this.w_di = w_di;
		this.label= label ;
		this.Z = Z;
		this.L = L ;
		this.S = S ;
		this.W = W;
		this.D = D;
		this.is_w = is_w ;
		this.map_id_word = map_id_word ;
		
		iterationvals = new Double[samples] ;

		alpha_num = an ;
		alpha_den = ad;
		beta_1_num = b1n ;
		beta_1_den = b1d ;
		beta_2_num = b2n;
		beta_2_den = b2d ;
		gamma_num = gn ;
		gamma_den = gd ;
		delta_1_num = d1n ;
		delta_1_den = d1d ;
		delta_2_num = d2n; 
		delta_2_den = d2d; 

		P_z_l = new double[Z][L] ;
		P_s_zl = new double[S][Z][L] ;
		P_w_z = new double[W][Z] ;
		P_w_s = new double[W][S] ;
		P_w_zs = new double[W][Z][S] ;
		P_s_l = new double[S][L] ;
		
		P_l = new double[L] ;
		P_z = new double[Z] ;
		
		
		
//		b_wz = loadbetapriors(lr, beta_prior);
//		a_z = loadalphapriors(alpha_prior);

		num_samples=0 ;
		Nd_z_l= new long[Z][L] ;
		Nd_l = new long[L] ;
		
		Nws_s_zl = new long[S][Z][L];
		Nws_zl = new long[Z][L] ;
		
		is_di = new int[D][] ;
		sentiment = new int[D][] ;
		topic = new int[D] ;
		
		Nws_w_zs = new long[W][Z][S] ;
		Nws_zs = new long[Z][S] ;
		
		Nws_s_l = new long[S][L];
		Nws_l = new long[L] ;
		
		Nws_w_s = new long[W][S] ;
		Nws_s = new long[S] ;
		
		Nwt_w_z = new long[W][Z] ;
		Nwt_z = new long[Z] ;

		for(int d=0;d<D;d++){
			topic[d]= (int) (Math.random()*Z) ;
		}
		
		for(int d=0;d<w_di.length;d++){
			is_di[d] = new int[w_di[d].length] ;
			sentiment[d] = new int[w_di[d].length] ;
			
			for(int i=0;i<w_di[d].length;i++){
				int w =w_di[d][i] ;
				double isp= is_w[w] ;
				double sam = Math.random() ;
				if(sam<isp)
					is_di[d][i]=0;
				else
					is_di[d][i]=1 ;
				//is_di[d][i] = (int) (Math.random()*2) ;
				
				
				if(is_di[d][i]==1){
					if(senti_prior.containsKey(w_di[d][i]))
						{	
							if(senti_prior.get(w_di[d][i])==1)
									sentiment[d][i]=1 ;
							else
									sentiment[d][i]= 0;
						}
					else
						sentiment[d][i]= (int) (Math.random()*S) ;
				}else
					sentiment[d][i] =-1 ;
			}
		}
		
		for(int d=0;d<w_di.length;d++){
			for(int i=0;i<w_di[d].length;i++){
				if(is_di[d][i]==1&&senti_prior.containsKey(w_di[d][i])){
				//	if(senti_prior.get(w_di[d][i])==0)
				//	System.out.println(String.valueOf(sentiment[d][i])+" "+String.valueOf(senti_prior.get(w_di[d][i]))) ;
				
				}
			}
		}
	

		for(int d=0;d<D;d++){
			Nd_z_l[topic[d]][label[d]]++ ;
			Nd_l[label[d]]++ ; 
		}

		for(int d=0;d<D;d++){
			int z =topic[d] ;
			int l =label[d] ;
			for(int i=0;i<w_di[d].length;i++){
				long w = w_di[d][i];				
				int is = is_di[d][i];				
				int s = sentiment[d][i];
				
				if(is==1){
					Nws_s_zl[s][z][l]++ ;
					Nws_w_zs[(int) w][z][s]++ ;
					Nws_zs[z][s]++  ;
					Nws_zl[z][l]++; 
					Nws_s_l[s][l]++ ;
					Nws_l[l]++ ;
					Nws_w_s[(int)w][s]++ ;
					Nws_s[s]++ ;
				}
				else {
					Nwt_z[z]++  ;
					Nwt_w_z[(int)w][z]++ ;
				}

			}		

		}




		// perform Gibbs sampling
		for (int iteration=0; iteration<burnIn+samples*step; iteration++) {
			
			
			for (int d=0; d<D; d++) { // document d
				
				if (w_di[d] == null){
					System.out.println("*");
					continue;
				}
				int l=label[d];
				int z=topic[d] ;
				
				//Estimate probability of z/l
				double[] p = new double[Z] ;
				Nd_z_l[z][l]--;
				Nd_l[l]-- ;
				//System.out.println(Nd_z_l[z][l]);
			//	System.out.println(Nd_l[l]);
				//System.out.println(w_di[d].length);
				
				for(int i=0;i<w_di[d].length;i++){
					
					int w = w_di[d][i] ;
					int s = sentiment[d][i] ;
					if(s==-1 && is_di[d][i]==1){
						System.out.println(String.valueOf(i)+" "+String.valueOf(d));
						System.out.println("Shit! Screwed");
						return ;
					}
					if(is_di[d][i]==1){
						Nws_s_zl[s][z][l]-- ;
						Nws_zl[z][l]-- ;
						Nws_w_zs[w][z][s]-- ;
						Nws_zs[z][s]-- ;
						Nws_s_l[s][l] -- ;
						Nws_l[l]-- ;
						Nws_w_s[(int)w][s]-- ;
						Nws_s[s]-- ;
					}else{
						Nwt_w_z[w][z]-- ;
						Nwt_z[z]-- ;
						
					}
				}

				// Sample z  ~ P(z/l) * for all words of doc d with is=1 P(s/z,l,is=1) * P(w/s,z,is=1) 
					// * for all with is=0 P(w/z,is=0)
				
				for(z=0;z<Z;z++){
					
					p[z] = (double)(Nd_z_l[z][l]+alpha_num)/
							(Nd_l[l]+alpha_den) ;
					
					//assert
					if(p[z]==0){
						System.out.println("--------------Shit! Screwed"+
								"-------------------------------------") ;
					}
					double as1,as2,as3,as4,as5 ;
					as1=p[z] ;
					
					for(int i=0;i<w_di[d].length;i++){
						int s=sentiment[d][i] ;
						int w= w_di[d][i] ;
						as3=p[z] ;
						if(is_di[d][i]==1){
							
							double p_s_l = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
										(Nws_l[l] + beta_1_den[l]) ;
							p[z]=p[z]* (double)(Nws_s_zl[s][z][l]+beta_2_num*p_s_l)/
									(Nws_zl[z][l]+beta_2_den);
							as2=p[z] ;
							double p_w_s = (double)(Nws_w_s[w][s]+delta_1_num)/
										(Nws_s[s]+ delta_1_den) ;
							p[z] = p[z]*(double)(Nws_w_zs[w][z][s] + p_w_s*delta_2_num)/
										(Nws_zs[z][s]+ delta_2_den)  ;
										
							if(p_s_l==0 || p[z]==0 || p_w_s==0 ){
								System.out.println("Why meeee") ;
								//System.out.println(p_s_l) ;
								/*System.out.println("p[z]") ;
								System.out.println(as1) ;
								System.out.println(as3) ;
								System.out.println("num") ;
								System.out.println(Nws_s_zl[s][z][l]) ;
								System.out.println("den") ;
								System.out.println(Nws_zl[z][l]) ;
								System.out.println("p[z]*some bakvass") ;
								System.out.println(as2) ; */
								System.out.println(p_w_s) ;
								System.out.println(Nws_w_s[w][s]) ;
								System.out.println(Nws_w_s[w][s]+delta_1_num);
								System.out.println(Nws_s[s]) ;
								System.out.println(Nws_s[s]+delta_1_den);
								/*
								System.out.println("p[z]*some bakvass * more bakwass") ;
								System.out.println(Nws_w_zs[w][z][s]) ;
								System.out.println(Nws_zs[z][s]) ;
								
								System.out.println(p[z]) ;
								*/
								System.out.println("Why meeee") ;
								return ;
									
							}
						
						}
						else if(is_di[d][i]==0){
							p[z]=p[z]* (double)(Nwt_w_z[w][z]+gamma_num)/
										(Nwt_z[z]+gamma_den) ;
												
							if(p[z]==0){
								System.out.println("--No please! no-- " ) ;
								System.out.println(p[z]) ;
								System.out.println("--No please! no-- " ) ;
								return ;
							}
							
							
						}
						
					}
					//System.out.println(Arrays.toString(p));
				
				}
				double totalsum =0 ;
				for( z=0;z<Z;z++){
					totalsum+=p[z] ;
				}
				
				for( z=0;z<Z;z++){
					p[z]/=totalsum ;
						
				}
				
				
				double val = Math.random() ;
				
				z = 0; while ((val -= p[z]) > 0) z++;  // select a new topic
				
				Nd_z_l[z][l]++;
				Nd_l[l]++ ;
				topic[d]=z ;
				
				
				for(int i=0;i<w_di[d].length;i++){
					int s= sentiment[d][i] ;
					int w =w_di[d][i] ;
					if(is_di[d][i]==1){
						Nws_s_zl[s][z][l]++ ;
						Nws_zl[z][l]++ ;
						Nws_w_zs[w][z][s]++ ;
						Nws_zs[z][s]++ ;
						Nws_s_l[s][l]++ ;
						Nws_l[l]++ ;
						Nws_w_s[(int)w][s]++ ;
						Nws_s[s]++ ;
					}else {
						Nwt_w_z[w][z]++ ;
						Nwt_z[z]++ ;
					}
				}
				
				for (int i=0; i<w_di[d].length; i++) { // position i
					// Aadi: Go over each word of all documents
					
					int w = w_di[d][i];				// Aadi: Which word is this?
					int is = is_di[d][i];				//whether it is a topic word or sentiment word
					int s = sentiment[d][i] ; 							//sentiment of word
					if(is==0){
						Nwt_w_z[w][z]-- ;
						Nwt_z[z]-- ;
					}else if(is==1){
						Nws_s_zl[s][z][l]-- ;
						Nws_zl[z][l]-- ;
						Nws_w_zs[w][z][s]-- ;
						Nws_zs[z][s]-- ;
						Nws_s_l[s][l]-- ;
						Nws_l[l]-- ;
						Nws_w_s[(int)w][s]-- ;
						Nws_s[s]-- ;
					}
					val = Math.random() ;
					if(val<is_w[w])
	//hack 101
					//if(is_w[w]>0.98)
						is_di[d][i]=0 ;
					else
						is_di[d][i]=1 ;
					is= is_di[d][i] ;
					
					if(is==0){
						Nwt_w_z[w][z]++ ;
						Nwt_z[z]++ ;
						sentiment[d][i]=-1 ;
					}else if(is==1){
						
						// Sample s ~ P(s|z,l,is=1). P(w|s,z,is=1)
						
						p = new double[S];

						double p_w_zs; 
						double p_s_zl; 
						double p_s_l ;
						double p_w_s ;
						
						double total =0 ;
						for( s=0;s<S;s++){
							p_s_l = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
								(Nws_l[l] + beta_1_den[l]) ;
							p_w_s = (double)(Nws_w_s[w][s]+delta_1_num)/ 
									(Nws_s[s]+ delta_1_den) ;	
							p_w_zs=(double)(Nws_w_zs[w][z][s]+delta_2_num*p_w_s)/
									(Nws_zs[z][s]+delta_2_den) ;
							p_s_zl = (double)(Nws_s_zl[s][z][l]+beta_2_num*p_s_l)/
									(Nws_zl[z][l]+beta_2_den) ;
							p[s] = (double)p_w_zs*p_s_zl ;
							if(p_s_l==0 || p_w_zs==0 || p_s_zl==0 ||p_s_zl>1 || p_w_zs>1 || p_s_zl>1 )
								System.out.println("error is here bro" ) ;
							total+=p[s] ;
						}
						for( s=0;s<S;s++)
							p[s]/=total ;
						val = Math.random();
					
 						s=0;while ((val -= p[s]) > 0) s++;
 						sentiment[d][i]=s ;
 						if(senti_prior.containsKey(w_di[d][i])){
 							sentiment[d][i]= senti_prior.get(w_di[d][i]);
 							s=sentiment[d][i] ;
 						}
 						if(s>1)
 							System.out.println("Ohhhh" ) ;
 							 
 						Nws_s_zl[s][z][l]++ ;
						Nws_zl[z][l]++ ;
						Nws_w_zs[w][z][s]++ ;
						Nws_zs[z][s]++ ;
						Nws_s_l[s][l]++ ;
						Nws_l[l]++ ;
						Nws_w_s[w][s]++ ;
						Nws_s[s]++ ;
					}

				
				}	
			}
			
			if(false) {
			
				// These probabilities are for assertion of the model
				double[][] aP_z_l =  new double[Z][L] ;
				double[][][] aP_s_zl  =  new double[S][Z][L] ;
				double[][] aP_s_l  =  new double[S][L] ; 
				double[][] aP_w_z =  new double[W][Z] ; 
				double[][] aP_w_s = new double [W][S] ;
				double[][][] aP_w_zs= new double [W][Z][S] ;
			
				// P(z|l)
					for(int z=0;z<Z;z++){
						
						for(int l=0;l<L;l++){
							aP_z_l[z][l] = (double)(Nd_z_l[z][l]+alpha_num)/
										(Nd_l[l]+alpha_den) ;
						}
					}
					//P(s/l,is=1)
					
					for(int l=0;l<L ;l++){
						for(int s=0;s<S;s++){
							aP_s_l[s][l] = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
										(Nws_l[l] + beta_1_den[l]) ;
							
						}
					}
					//P(s|z,l,is=1)
					for(int z=0;z<Z;z++){
						for(int l=0;l<L;l++){
							double total=0   ;
							for(int s=0;s<S;s++){
								
								aP_s_zl[s][z][l]= (double)(Nws_s_zl[s][z][l]+ beta_2_num*aP_s_l[s][l])/
											(Nws_zl[z][l]+beta_2_den) ;
								
							}
						}
					}
					//P(w|z,is=0)
					for(int z =0;z<Z;z++){
						for(int w=0;w<W;w++){
							aP_w_z[w][z]= (double)(Nwt_w_z[w][z]+gamma_num)/
										(Nwt_z[z]+gamma_den) ;
						}
					}
					//P(w/s, is=1)
					double[][] p_w_s = new double[W][S] ;
					for(int s=0;s<S;s++){
						for(int w=0;w<W;w++){
							aP_w_s[w][s] = (double)(Nws_w_s[w][s]+delta_1_num)/
										(Nws_s[s]+ delta_1_den) ;
							
						}
					}
					
					
					//P(w|s,z,is=1)
					for(int s=0;s<S;s++){
						for(int z=0;z<Z;z++){
							for(int w=0;w<W;w++){
								aP_w_zs[w][z][s]= (double)(Nws_w_zs[w][z][s] + aP_w_s[w][s]*delta_2_num)/
											(Nws_zs[z][s]+ delta_2_den) ; 
							}
						}
					}
					//assert_model_separate(aP_z_l,aP_s_zl,aP_s_l,aP_w_z,aP_w_s,aP_w_zs) ;
			
			}	

			// update parameter estimates
			if (iteration >= burnIn && (iteration-burnIn)%step==0) {	

					//P_l
					int sm=0 ;
					for(int l=0;l<L;l++){
						
						sm+=Nd_l[l] ;
					}
					for(int l=0;l<L;l++){
						P_l[l]+=(double)Nd_l[l]/sm ;
					}
					for(int z=0;z<Z;z++){
						int usum=0 ;
						for(int l=0;l<L;l++){
							usum+=Nd_z_l[z][l] ;
						}
						P_z[z]+=(double)usum/sm  ;
					}
					
				
					// P(z|l)
					for(int z=0;z<Z;z++){
						for(int l=0;l<L;l++){
							P_z_l[z][l] += (double)(Nd_z_l[z][l]+alpha_num)/
										(Nd_l[l]+alpha_den) ;
						}
					}
					//P(s/l,is=1)
					double p_s_l[][] = new double[S][L] ;
					for(int l=0;l<L ;l++){
						for(int s=0;s<S;s++){
							p_s_l[s][l] = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
										(Nws_l[l] + beta_1_den[l]) ;
							P_s_l[s][l]+= (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
										(Nws_l[l] + beta_1_den[l]) ;
						}
					}
					//P(s|z,l,is=1)
					for(int z=0;z<Z;z++){
						for(int l=0;l<L;l++){
							for(int s=0;s<S;s++){
								P_s_zl[s][z][l]+= (double)(Nws_s_zl[s][z][l]+ beta_2_num*p_s_l[s][l])/
											(Nws_zl[z][l]+beta_2_den) ;
							}
						}
					}
					//P(w|z,is=0)
					for(int z =0;z<Z;z++){
						for(int w=0;w<W;w++){
							P_w_z[w][z]+= (double)(Nwt_w_z[w][z]+gamma_num)/
										(Nwt_z[z]+gamma_den) ;
						}
					}
					//P(w/s, is=1)
					double[][] p_w_s = new double[W][S] ;
					for(int s=0;s<S;s++){
						for(int w=0;w<W;w++){
							p_w_s[w][s] = (double)(Nws_w_s[w][s]+delta_1_num)/
										(Nws_s[s]+ delta_1_den) ;
							P_w_s[w][s] += (double)(Nws_w_s[w][s]+delta_1_num)/
										(Nws_s[s]+ delta_1_den) ;
						}
					}
					
					
					//P(w|s,z,is=1)
					for(int s=0;s<S;s++){
						for(int z=0;z<Z;z++){
							for(int w=0;w<W;w++){
								P_w_zs[w][z][s]+= (double)(Nws_w_zs[w][z][s] + p_w_s[w][s]*delta_2_num)/
											(Nws_zs[z][s]+ delta_2_den) ; 
							}
						}
					}
					
					
					
					
					
			}
			double ll = log_likelihood() ;
			if (iteration >= burnIn && (iteration-burnIn)%step==0) {
				iterationvals[num_samples++] = ll ;
			}
			if (iteration >= burnIn && (iteration-burnIn)%step==0) {
				System.out.print("Sample No:"+ String.valueOf(num_samples)+" ") ;
			}else{
				System.out.print("Burned: ") ;
			}
			System.out.println(ll);

			
		/*	System.out.println("--") ; 
			
			for(int l=0;l<L;l++){
				double[] p = new double[Z] ;
				for(int z=0;z<Z;z++){
					p[z] = (double)(Nd_z_l[z][l]+alpha_num)/
						(Nd_l[l]+alpha_den) ;
				}
				int ind=0,ind2=1;
				double val=p[0],val2=p[1] ;
				if(val<val2){
					val=p[1] ;
					val2=p[0] ;
					ind=1 ;
					ind2=0 ;
				}
					
				for(int z=0;z<p.length;z++){
					if(val<p[z]){
						val2=val ;
						ind2=ind ;
						val=p[z]; 
						ind=z ;
					}else if(val2<p[z]){
						val2=p[z] ;
						ind2=z ;
					}
				}
				//Print top 15 words for topic ind
				
				print_topicwords(15,ind) ;
				System.out.println(String.valueOf(iteration)+" "+String.valueOf(l)+" "+String.valueOf(ind)+" "+String.valueOf(val)) ;
				print_topicwords(15,ind2) ;
				System.out.println(String.valueOf(iteration)+" "+String.valueOf(l)+" "+String.valueOf(ind2)+" "+String.valueOf(val2)) ;
				
			}
			System.out.println("--") ;
			*/
			
			double[][] p_w_z = new double[W][Z] ;
			for(int w=0;w<W;w++){
				for(int z=0;z<Z;z++){
					p_w_z[w][z] = (double)(Nwt_w_z[w][z]+gamma_num)/
							(Nwt_z[z]+gamma_den) ;
				}
			}
			double[][][] p_w_zs = new double[W][Z][S] ;
			//P(w/s, is=1)
			double[][] p_w_s = new double[W][S] ;
			for(int s=0;s<S;s++){
				for(int w=0;w<W;w++){
					p_w_s[w][s] = (double)(Nws_w_s[w][s]+delta_1_num)/
								(Nws_s[s]+ delta_1_den) ;
				}
			}
			
			
			//P(w|s,z,is=1)
			for(int s=0;s<S;s++){
				for(int z=0;z<Z;z++){
					for(int w=0;w<W;w++){
						p_w_zs[w][z][s]= (double)(Nws_w_zs[w][z][s] + p_w_s[w][s]*delta_2_num)/
									(Nws_zs[z][s]+ delta_2_den) ; 
					}
				}
			}
			
			double[][] p_z_l =new double[Z][L] ;
			// P(z|l)
			for(int z=0;z<Z;z++){
				for(int l=0;l<L;l++){
					p_z_l[z][l] = (double)(Nd_z_l[z][l]+alpha_num)/
								(Nd_l[l]+alpha_den) ;
				}
			}
			double[] p_l = new double[L] ;
			double[] p_z =new double[Z] ;
			
			int sm=0 ;
			for(int l=0;l<L;l++){
				
				sm+=Nd_l[l] ;
			}
			for(int l=0;l<L;l++){
				p_l[l]=(double)Nd_l[l]/sm ;
			}
			for(int z=0;z<Z;z++){
				int usum=0 ;
				for(int l=0;l<L;l++){
					usum+=Nd_z_l[z][l] ;
				}
				p_z[z]=(double)usum/sm  ;
			}
			int tp=0,tn=0,fp=0,fn=0 ;
			double[][][] p_s_zl = new double[S][Z][L];
			double p_s_l[][] = new double[S][L] ;
			for(int l=0;l<L ;l++){
				for(int s=0;s<S;s++){
					p_s_l[s][l] = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/
								(Nws_l[l] + beta_1_den[l]) ;
				}
			}
			for(int z=0;z<Z;z++){
				for(int l=0;l<L;l++){
					for(int s=0;s<S;s++){
						p_s_zl[s][z][l]= (double)(Nws_s_zl[s][z][l]+ beta_2_num*p_s_l[s][l])/
									(Nws_zl[z][l]+beta_2_den) ;
					}
				}
			}
			
			double[][] p_l_z = new double[L][Z] ;
			for(int l=0;l<L;l++){
				for(int z=0;z<Z;z++){
					p_l_z[l][z] = (p_l[l]*p_z_l[z][l])/p_z[z];
				}
			}
			
			int[] predict_label = new int[test_label.length] ;
			
			for(int i=0;i<test_data.length;i++){
				int op=predict2(test_data[i],p_z_l,p_w_z,p_s_zl,p_w_zs) ;
				predict_label[i]= op ;
				if(op==test_label[i]&&op==2)
					tp++;
				else if(op==test_label[i]&&op!=2)
					tn++;
				else if(op!=test_label[i]&&op==2)
					fp++;
				else
					fn++;
			}
			double precision=0.0d ;
			precision = (double)tp/(double)(tp+fp) ;
			double recall = 0;
			recall=(double)tp/(double)(tp+fn);
			double fscore = (2*precision*recall)/(precision+recall) ;
			double nprecision = (double)tn/(double)(tn+fn) ;
			double nrecall = (double)tn/(double)(tn+fp) ;
			
			predict_sampleL(test_data, test_label, p_z_l, p_s_zl, p_w_zs, p_w_z,p_l_z, String.valueOf(result_path_suffix)+String.valueOf(iteration)) ;
			
			fscorewrite.open();
			try {
				fscorewrite.write(String.valueOf(fscore)+" "+String.valueOf(precision)+" "+String.valueOf(recall)+" "
						+String.valueOf(nprecision)+" "+String.valueOf(nrecall));
				fscorewrite.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			System.out.println(tp);
			System.out.println(precision);
			System.out.println(recall);
			System.out.println(nprecision);
			System.out.println(nrecall);
			
			
			outputs[iteration] = new Output(w_di,label,sentiment,iteration,W, D, L, S, Z, map_id_word, p_w_z, p_w_zs, p_z_l, p_z, p_l,p_s_l,p_s_zl, precision,recall,nprecision,nrecall,result_path_suffix);
			String path_towrite="" ;
			path_towrite= "/home/development/prayas/topic-model-data/results/prediction/predict-"+String.valueOf(result_path_suffix)+String.valueOf(iteration) ;
			writesentencepredictions(path_towrite,test_data,test_label,predict_label);
			
			int[] positive = new int[w_di.length] ;
			int[] negative = new int[w_di.length] ;
			for(int d=0;d<w_di.length;d++){
				int pos =0 ;
				int neg =0 ;
				for(int i=0;i<w_di[d].length;i++){
					if(sentiment[d][i]==0)
						pos++ ;
					else if(sentiment[d][i]==1)
						neg++ ;
					
				}
				positive[d]=pos ;
				negative[d] = neg ;
			
			}
			
			if(iteration==10 || iteration==59){
				createdata_svm(w_di,label, topic,p_l_z, p_s_zl, positive, negative, String.valueOf(result_path_suffix)+String.valueOf(iteration),0);
			}
			
			
			//Write distributions to a file 
			String distropath = "/home/development/prayas/topic-model-data/results/distros/distro-"+String.valueOf(result_path_suffix)+String.valueOf(iteration) ;
			
			WriteFile writedistro = new WriteFile(distropath) ;
			try {
				writedistro.write("P_z_l") ;
				for(int l=0;l<L;l++){
					String as = "" ;
					for(int z=0;z<Z;z++){
						as+=String.valueOf(p_z_l[z][l])+" " ;
					}
					writedistro.write(as) ;
					
				}
				writedistro.write("P_l") ;
				writedistro.write(Arrays.toString(p_l)) ;
				writedistro.write("P_z") ;
				writedistro.write(Arrays.toString(p_z)) ;
				writedistro.write("P_s_l") ;
				
				for(int l=0;l<L ;l++){
					String as = "" ;
					for(int s=0;s<S;s++){
						as+=String.valueOf(p_s_l[s][l])+" " ;
					}
					writedistro.write(as) ;
				}
				writedistro.write("P_s_zl") ;
				for(int l=0;l<L;l++){
					for(int s=0;s<S;s++){
						String as ="" ;
						for(int z=0;z<Z;z++){
							as+=String.valueOf(p_s_zl[s][z][l])+" " ;
							
						}
						writedistro.write(as) ;
					}
				}
				writedistro.close() ;
				
				
				
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			
			if(iteration==burnIn+samples*step-1){
				//Scatter Plot
				WriteFile scatter = new WriteFile("/home/development/prayas/topic-model-data/results/scatter/scatter-"+String.valueOf(result_path_suffix)) ;
				for(int d=0;d<w_di.length;d++){
					String res=String.valueOf(label[d]) ;
					int s0=0,s1=0;
					for(int i=0;i<w_di[d].length;i++){
						if(sentiment[d][i]==1)
							s1++;
						else
							s0++ ;
					}
					res=res+" "+String.valueOf(s0)+" "+String.valueOf(s1)+" "+String.valueOf(w_di[d].length) ;
					//System.out.println(res);
					try {
						scatter.write(res);
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}

		}
		double totsum = 0 ;
		for(int l=0;l<L;l++){
			totsum+=P_l[l] ;
		}
		
		for(int l=0;l<L;l++){
			P_l[l]/=totsum ;
		}
		
		totsum = 0 ;
		for(int z=0;z<Z;z++){
			totsum+=P_z[z] ;
		}
		
		for(int z=0;z<Z;z++){
			P_z[z]/=totsum ;
		}
		
		//Normalize P(z|l)
		for(int l=0;l<L;l++){
			double totalsum =0 ;
			for(int z=0;z<Z;z++){
				totalsum+=P_z_l[z][l] ;
			}
			for(int z=0;z<Z;z++){
				P_z_l[z][l]/=totalsum ;
				if(P_z_l[z][l]==0)
					System.out.println("I am tired now") ;
			}
			
		}
		//Normalize P(s/l ,is= 1)
		for(int l=0;l<L;l++){
			double totalsum = 0 ;
			for(int s=0;s<S;s++){
				totalsum+= P_s_l[s][l] ;
				
			}
			for(int s=0;s<S;s++){
				 P_s_l[s][l]/=totalsum ;
				 if(P_s_l[s][l]==0)
					System.out.println("I am tired now!!!!!!!!") ;
			}	
		}
		
		
		
		//Normalize P(s/z,l,is=1)
		for(int z=0;z<Z;z++){
			for(int l=0;l<L;l++){
				double totalsum =0 ;
				for(int s=0;s<S;s++){
					totalsum+= P_s_zl[s][z][l] ;
				}
				for(int s=0;s<S;s++){
					P_s_zl[s][z][l]/=totalsum  ;
					if(P_s_zl[s][z][l]==0)
						System.out.println("I am tired now! The hardest") ;
				}
				
			}
		}
		// Normalize P(w/z,is=0)
		for(int z=0;z<Z;z++){
			double totalsum=0 ;
			for(int w=0;w<W;w++){
				totalsum+=P_w_z[w][z] ;
			}
			for(int w=0;w<W;w++){
				P_w_z[w][z]/=totalsum ;
			}
		}
		// Normalize P(w/s, is= 1)
		for(int s=0;s<S;s++){
			double total = 0;
			for(int w=0;w<W;w++){
				total+=P_w_s[w][s] ;
			}
			for(int w=0;w<W;w++){
				P_w_s[w][s]/=total ;
			}
		}
		
		// Normalize P(w/s,z,is=1)
		for(int z=0;z<Z;z++){
			for(int s=0;s<S;s++){
				double total= 0;
				for(int w=0;w<W;w++){
					total+=P_w_zs[w][z][s] ;
				}
				for(int w=0;w<W;w++){
					P_w_zs[w][z][s]/=total ;
				}
				
				
			}
		}
		
		
		
		writer.close() ;
		get_words(count, result_path_suffix); 
		getSentimentWords(5,result_path_suffix) ;
		getPz_l(result_path_suffix);
		
		for(int s=0;s<S;s++)
			System.out.println(Arrays.toString(P_s_l[s])) ;
		
		//assert_model() ;
		
		
	}


	//obselete, used to assert the model

	private void assert_model_separate(double[][] P_z_l, double[][][] P_s_zl,
			double[][] P_s_l, double[][] P_w_z, double[][] P_w_s,
			double[][][] P_w_zs) {
		// TODO Auto-generated method stub
		
		//Assert P_z_l
		System.out.println("Assert p_z_l") ;
		for(int l=0;l<L;l++){
			double total = 0 ;
			for(int z=0;z<Z;z++){
				total+= P_z_l[z][l] ;
				System.out.print(String.valueOf(P_z_l[z][l])+" " ) ;
			
			}
			System.out.println(total) ;
			
		} 

		//Assert P_s_zl
		System.out.println("Assert p_s_zl") ;
		for(int z = 0 ;z<Z;z++){
			
			
			for(int l=0; l<L;l++){
				double total = 0 ;
				for(int s=0;s<S;s++){
					total+=P_s_zl[s][z][l] ;
					System.out.print(String.valueOf(P_s_zl[s][z][l])+" " ) ;
					
				}	
				System.out.println(total) ;
				
			}
			
			
			
			
		} 
		
		
		// Assert P_s_l 
		System.out.println("Assert p_s_l") ;
		for (int l=0;l<L;l++){
			double total = 0 ; 
			for(int s=0;s<S; s++){
				System.out.print(String.valueOf(P_s_l[s][l])+" ") ;
				total+= P_s_l[s][l] ;
				
			}
			System.out.println(total) ;
		} 
		//Assert word probabilites now 
		
		System.out.println("Assert p_w_z") ;
		for(int z=0;z<Z;z++){
			double total = 0 ;
			for(int w=0;w<W;w++){
				total+=P_w_z[w][z] ;
				if(w<2) 
					System.out.print(String.valueOf(P_w_z[w][z])+" ") ;
				if(P_w_z[w][z]>1 || P_w_z[w][z]<=0){
					System.out.print("doomed") ;
				}
			}
			System.out.println(total) ;
		}
		
		
		System.out.println("Assert p_w_s") ;
		for(int s=0;s<S;s++){
			double total = 0 ;
			for(int w=0;w<W;w++){
				total+=P_w_s[w][s] ;
				if(w<2) 
					System.out.print(String.valueOf(P_w_s[w][s])+" ") ;
				if(P_w_s[w][s]>1 || P_w_s[w][s]<=0){
					System.out.print("doomed") ;
					return ;
				}
			}
			System.out.println(total) ;
		}
		
		System.out.println("Assert p_w_zs") ;
		for(int z=0;z<Z;z++){
		for(int s=0;s<S;s++){
			double total = 0 ;
			for(int w=0;w<W;w++){
				total+=P_w_zs[w][z][s] ;
				if(w<2) 
					System.out.print(String.valueOf(P_w_zs[w][z][s])+" ") ;
				if(P_w_zs[w][z][s]>1 || P_w_zs[w][z][s]<=0){
					System.out.print("doomed") ;
					return ;
				}
			}
			System.out.println(total) ;
		}}
		
		
		
		
	}


	//obselete, used to assert the model

	private void assert_model(){
		//Assert P_z_l
		/*System.out.println("Assert p_z_l") ;
		for(int l=0;l<L;l++){
			double total = 0 ;
			for(int z=0;z<Z;z++){
				total+= P_z_l[z][l] ;
				System.out.print(String.valueOf(P_z_l[z][l])+" " ) ;
			
			}
			System.out.println(total) ;
			
		} */

		//Assert P_s_zl
		/*System.out.println("Assert p_s_zl") ;
		for(int z = 0 ;z<Z;z++){
			
			
			for(int l=0; l<L;l++){
				double total = 0 ;
				for(int s=0;s<S;s++){
					total+=P_s_zl[s][z][l] ;
					System.out.print(String.valueOf(P_s_zl[s][z][l])+" " ) ;
					
				}	
				System.out.println(total) ;
				
			}
			
			
			
			
		} 
		*/
		
		// Assert P_s_l 
		/*System.out.println("Assert p_s_l") ;
		for (int l=0;l<L;l++){
			double total = 0 ; 
			for(int s=0;s<S; s++){
				System.out.print(String.valueOf(P_s_l[s][l])+" ") ;
				total+= P_s_l[s][l] ;
				
			}
			System.out.println(total) ;
		} */
		//Assert word probabilites now 
		
		System.out.println("Assert p_w_z") ;
		for(int z=0;z<Z;z++){
			double total = 0 ;
			for(int w=0;w<W;w++){
				total+=P_w_z[w][z] ;
				if(w<2) 
					System.out.print(String.valueOf(P_w_z[w][z])+" ") ;
				if(P_w_z[w][z]>1 || P_w_z[w][z]<=0){
					System.out.print("doomed") ;
				}
			}
			System.out.println(total) ;
		}
		
		
		System.out.println("Assert p_w_s") ;
		for(int s=0;s<S;s++){
			double total = 0 ;
			for(int w=0;w<W;w++){
				total+=P_w_s[w][s] ;
				if(w<2) 
					System.out.print(String.valueOf(P_w_s[w][s])+" ") ;
				if(P_w_s[w][s]>1 || P_w_s[w][s]<=0){
					System.out.print("doomed") ;
				}
			}
			System.out.println(total) ;
		}
		
		//System.out.println("Assert p_w_zs") ;
		//for(int z=0;z<Z;z++){
		//for(int s=0;s<S;s++){
		//	double total = 0 ;
		//	for(int w=0;w<W;w++){
		//		total+=P_w_zs[w][z][s] ;
		//		if(w<2) 
		///			System.out.print(String.valueOf(P_w_zs[w][z][s])+" ") ;
		//		if(P_w_zs[w][z][s]>1 || P_w_zs[w][z][s]<=0){
		//			System.out.print("doomed") ;
		///		}
		//	}
		///	System.out.println(total) ;
	///	}}
		
		
		
	
	}
	
	
	//Compute the log likelihood of the model

	private double log_likelihood() {
		// TODO Auto-generated method stub
		double ll = 0.0d ;
		for(int d=0;d<D;d++){
			int z = topic[d] ;
			int l = label[d] ;
			double p_z_l =(double)(Nd_z_l[z][l]+alpha_num)/(Nd_l[l]+alpha_den) ;
			ll+= Math.log(p_z_l) ;
			//if(Double.isNaN(ll))
			//	System.out.println("1 is the bitch") ;
			for(int i=0;i<w_di[d].length;i++){
				int w = w_di[d][i] ;
				int is= is_di[d][i];
				if(is==0)
					ll+= Math.log(is_w[w]) ;
				else
					ll+= Math.log(1.0d-is_w[w]) ;
			//	if(Double.isNaN(ll))
			//		System.out.println("2 is the bitch") ;	
					
				if(is==1){
					int s= sentiment[d][i] ;
					
					double p_s_l = (double)(Nws_s_l[s][l] + beta_1_num[s][l])/(Nws_l[l] + beta_1_den[l]) ;
					//double p_w_zs=(double)(Nws_w_zs[w][z][s]+1)/(Nws_zs[z][s]+S) ;
					double p_s_zl = (double)(Nws_s_zl[s][z][l]+beta_2_num*p_s_l)/(Nws_zl[z][l]+beta_2_den) ;
					ll+= Math.log(p_s_zl) ;
				//	if(Double.isNaN(ll))
				//		System.out.println("3 is the bitch") ;
					
				}
				if(is==0){
					double p_w_z = (double)(Nwt_w_z[w][z]+gamma_num)/(Nwt_z[z]+gamma_den) ;
					ll+=Math.log(p_w_z) ;
				//	if(Double.isNaN(ll))
				//		System.out.println("4 is the bitch") ;
				}
				if(is==1){
					int s = sentiment[d][i] ;
					double p_w_s = (double)(Nws_w_s[w][s]+delta_1_num)/
											(Nws_s[s]+ delta_1_den) ;
					
					double p_w_sz = (double)(Nws_w_zs[w][z][s] + p_w_s*delta_2_num)/
											(Nws_zs[z][s]+ delta_2_den) ; 
					
					ll+=Math.log(p_w_sz) ;
				//	if(Double.isNaN(ll))
				//		System.out.println("5 is the bitch") ;
				}
				
			}
		}
		
		try {
			writer.write(String.valueOf(ll)) ;
			writer.close() ;
			writer.open() ;
			return ll ;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return 11838*1.0d ;
		}
		
		
	}








	public static long getN() {
		return N;
	}

	public static void setN(long n) {
		N = n;
	}
	//print top sentiment words for each topic
	public void getSentimentWords(int count,int fsuffix){
	
		//P_w_zs
		
		String wordpath="/home/development/prayas/topic-model-data/results/words/words-"+String.valueOf(fsuffix) ;
		WriteFile wordwrite = new WriteFile(wordpath) ;
		
		
		for(int z=0;z<Z;z++){
			for(int s=0;s<S;s++){
				ArrayIndexComparator2 compare = new ArrayIndexComparator2(P_w_zs,z,s,W) ;
				Integer[] indexes = compare.createIndexArray() ;
				Arrays.sort(indexes,compare) ;
				String w =String.valueOf(z+1)+" " ;
				String pw = String.valueOf(z+1)+ " " ;
				for(int c=0;c<count;c++){
					 w+= map_id_word[indexes[c]] ;
					 w+=" " ;
					 pw+= String.valueOf(P_w_zs[indexes[c]][z][s])+" " ;
				}
				try {
					wordwrite.write(w) ;
			//		wordwrite.write(pw) ;
					//wordwrite.write("\n") ;
				} catch (IOException e) {
				// TODO Auto-generated catch block
					e.printStackTrace();
				}
			
			}
			
			try {
					
					wordwrite.write("\n") ;
				} catch (IOException e) {
				// TODO Auto-generated catch block
					e.printStackTrace();
				}
			
			
		}
		
		try {
			wordwrite.write("\n---Sentiment words for each topic----\n") ;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		wordwrite.close() ;

	}
	//print P(z/l)
	public void getPz_l(int fsuffix){
	
		String wordpath="/home/development/prayas/topic-model-data/results/words/words-"+String.valueOf(fsuffix) ;
		WriteFile wordwrite = new WriteFile(wordpath) ;
		for(int z=0;z<Z;z++){
				String w=" " ;	
				w= String.valueOf(z+1)+ " Happy= " ;
				w+= String.valueOf(P_z_l[z][0]) ;
				w+= " Sad= " ;
				w+= String.valueOf(P_z_l[z][1]) ;
				w+= " Sarcasm= " ;
				w+= String.valueOf(P_z_l[z][2]) ;
				try {
					wordwrite.write(w) ;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
	
		}
		
		try {
			wordwrite.write("\n") ;
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		for(int l= 0 ;l<L;l++){
			double[] prob = new double[Z] ;
			for(int z=0;z<Z;z++){
				prob[z]=P_z_l[z][l]; 
			}
			
			ArrayIndexComparator3 compare = new ArrayIndexComparator3(prob) ;
			Integer[] indexes = compare.createIndexArray() ;
			Arrays.sort(indexes,compare) ;
			for(int i=0;i<indexes.length;i++){
				indexes[i]=indexes[i]+1 ;
			}
			
			try {
			
				
			if(l==0)
				
					wordwrite.write("Happy: "+Arrays.toString(indexes)) ;
				
			if(l==1)
				wordwrite.write("Sad: "+Arrays.toString(indexes)) ;
			if(l==2)
				wordwrite.write("Sarcasm: "+Arrays.toString(indexes)) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}	
		
		}
		
		//P_l_z
		double[][] p_l_z = new double[L][Z];
		
		
		for(int z=0;z<Z;z++){
			for(int l=0;l<L;l++){
				p_l_z[l][z] = (P_z_l[z][l]*P_l[l])/P_z[z] ;
			
			}
			try {
				wordwrite.write(String.valueOf(z+1)+ " " + "Happy "+ String.valueOf(p_l_z[0][z])+" "+"Sad "
								+ String.valueOf(p_l_z[1][z])+" Sarcasm "+String.valueOf(p_l_z[2][z])) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		for(int l= 0 ;l<L;l++){
			double[] prob = new double[Z] ;
			for(int z=0;z<Z;z++){
				prob[z]=p_l_z[l][z]; 
			}
			
			ArrayIndexComparator3 compare = new ArrayIndexComparator3(prob) ;
			Integer[] indexes = compare.createIndexArray() ;
			Arrays.sort(indexes,compare) ;
			for(int i=0;i<indexes.length;i++){
				indexes[i]=indexes[i]+1 ;
			}
			
			try {
			
				
			if(l==0)
				
					wordwrite.write("Happy: "+Arrays.toString(indexes)) ;
				
			if(l==1)
				wordwrite.write("Sad: "+Arrays.toString(indexes)) ;
			if(l==2)
				wordwrite.write("Sarcasm: "+Arrays.toString(indexes)) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}	
		
		}
		
		
		
		
		
		
		try {
			wordwrite.write("\n---Probabilities topic----\n") ;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		wordwrite.close() ;
	
	
	}
	//helper classes used by other methods
	
	public class ArrayIndexComparator2 implements Comparator<Integer>
	{	
    		private final double[][][] array;
		private final int z,s  ;
    		public ArrayIndexComparator2(double[][][] array,int z,int s,int W)
    		{
    			this.z = z; 
    			this.s= s ;
        		this.array = array;
    		}		

    		public Integer[] createIndexArray()
    		{
        		Integer[] indexes = new Integer[W];
        		for (int i = 0; i < W; i++)
        		{
            			indexes[i] = i; // Autoboxing
        		}
        		return indexes;
    		}

    		@Override
    		public int compare(Integer index1, Integer index2)
    		{
         // Autounbox from Integer to int to use as array indexes
        //reversed them -prayas to get reverse sorted
    			return Double.compare(array[index2][z][s], array[index1][z][s]) ;
        		
    		}
	}
	
	
	public class ArrayIndexComparator3 implements Comparator<Integer>
	{	
    		private final double[] array;
		
    		public ArrayIndexComparator3(double[] array)
    		{
    			
        		this.array = array;
    		}		

    		public Integer[] createIndexArray()
    		{
        		Integer[] indexes = new Integer[array.length];
        		for (int i = 0; i < array.length; i++)
        		{
            			indexes[i] = i; // Autoboxing
        		}
        		return indexes;
    		}

    		@Override
    		public int compare(Integer index1, Integer index2)
    		{
         // Autounbox from Integer to int to use as array indexes
        //reversed them -prayas to get reverse sorted
    			return Double.compare(array[index2], array[index1]) ;
        		
    		}
	}
	
	
	
	
	
	
	public class ArrayIndexComparator implements Comparator<Integer>
	{	
    		private final double[][] array;
		private final int z  ;
    		public ArrayIndexComparator(double[][] array,int z,int W)
    		{
    			this.z = z; 
        		this.array = array;
    		}		

    		public Integer[] createIndexArray()
    		{
        		Integer[] indexes = new Integer[W];
        		for (int i = 0; i < W; i++)
        		{
            			indexes[i] = i; // Autoboxing
        		}
        		return indexes;
    		}

    		@Override
    		public int compare(Integer index1, Integer index2)
    		{
         // Autounbox from Integer to int to use as array indexes
        //reversed them -prayas to get reverse sorted
    			return Double.compare(array[index2][z], array[index1][z]) ;
        		
    		}
	}	

	public void get_words(int count,int fsuffix){
		String wordpath="/home/development/prayas/topic-model-data/results/words/words-"+String.valueOf(fsuffix) ;
		WriteFile wordwrite = new WriteFile(wordpath) ;
		for(int z=0;z<Z;z++){
			ArrayIndexComparator compare = new ArrayIndexComparator(P_w_z,z,W) ;
			Integer[] indexes = compare.createIndexArray() ;
			Arrays.sort(indexes,compare) ;
			String w =String.valueOf(z+1)+" " ;
			for(int c=0;c<count;c++){
				 w+= map_id_word[indexes[c]] ;
				 w+=" " ;
			}
			try {
				wordwrite.write(w) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		try {
			wordwrite.write("\n---------\n") ;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		wordwrite.close() ;
	}	
	public void writesentencepredictions(String path,int[][] test_data,int[] test_label, int[] predict_label){
		WriteFile writesentence = new WriteFile(path) ;
		for(int d=0;d<test_data.length;d++){
			String sentence ="" ;
			sentence=sentence+test_label[d]+"\t"+predict_label[d]+"\t";
			
			int w ;
			String word ;
			for(int i=0;i<test_data[d].length;i++){
				w=test_data[d][i] ;
				word = map_id_word[w] ;
				sentence=sentence+word+" " ;
				
			}
			try {
				writesentence.write(sentence) ;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
}





