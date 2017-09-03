package SentencePredictor;

import java.util.HashSet;
import java.util.StringTokenizer;
import java.io.*;
import java.nio.charset.Charset;

//class to save positive sentiment and negative sentiment and flips 
class g {
    public static int pos;
    public static int neg;
    public static int flips;
    
}

public class SentimentSentence {

	public static SentimentWord sw;
	public static HashSet<String> negators;
	public static HashSet<String> intensifiers;


	private HashSet<String> getNegators() {

		HashSet<String> negators = new HashSet<String>();

		String[] listnegators = {"not","no","never","neither","nor"};
		for (String s: listnegators) negators .add(s);

		return negators;

	}


	private HashSet<String> getIntensifiers() {

		HashSet<String> intensifiers = new HashSet<String>();

		String[] fromOpinionFinder = {"absolute","abundant","acute","ample","all-consuming","all-embracing","ardent","big","bottomless","boundless","burning","categorical","certain","clear","close","colossal","complete","consuming","consummate","considerable","damned","decided","deep","definite","definitive","downright","drastic","emphatic","enormous","endless","entire","excessive","extensive","extravagant","extreme","fanatical","fervent","fervid","fierce","firm","forceful","gigantic","great","greatest","grievous","heightened","high","highest","huge","humongous","illimitable","immense","incalculable","incontestable","incontrovertible","indisputable","infinite","inordinate","intense","intensified","intensive","keen","mammoth","marked","maximal","maximum","mighty","more","most","mungo","numerous","out-and-out","outright","perfect","plain","powerful","prodigious","profound","pronounced","pure","real","resounding","severe","sharp","sheer","simple","strict","strong","stupendous","supreme","sure","terrible","thorough","titanic","top","total","towering","tremendous","true","ultimate","unambiguous","unconditional","uncontestable","undeniable","undesputable","unending","unequivocal","unfathomable","unlimited","unmistakable","unqualified","unquestionable","utmost","utter","uttermost","vast","vehement","vigorous","violent","vivid","zealous","absolutely","absurdly","abundantly","acutely","all","altogether","amazingly","amply","ardently","astonishingly","awfully","categorically","certainly","clearly","completely","considerably","dearly","decidedly","deeply","definitely","definitively","downright","drastically","eminently","emphatically","endlessly","entirely","even","exaggeratedly","exceedingly","excessively","explicitly","expressly","extensively","extraordinarily","extravagantly","extremely","fanatically","fervently","fervidly","fiercely","firmly","forcefully","frankly","fully","greatly","highly","hugely","immensely","incredibly","indeed","indispensably","indisuptably","indubitably","infinitely","inordinately","intensely","irretrievably","just","keenly","largely","maximally","mightily","more","most","much","notably","noticeably","outright","outrightly","particularly","perfectly","plainly","positively","powerfully","pressingly","pretty","prodigiously","profoundly","purely","quite","really","remarkably","severely","sharply","simply","strikingly","strongly","stupendously","substantially","super","superlatively","supremely","surely","surpassingly","surprisingly","terribly","thoroughly","too","totally","tremendously","truely","ultimately","unambiguously","uncommonly","unconditionally","unbelievably","undeniably","undisputably","unequivocally","unnaturally","unquestionably","unusually","utterly","vastly","vehemently","vigorously","violently","vividly","very","wholly","wonderfully","zealously"};

		for (String s: fromOpinionFinder) intensifiers.add(s);

		return intensifiers;

	}
	private static boolean isNegator(String word)
	{
		return (negators.contains(word));
		
		
	}
	private static boolean isIntensifier(String word)
	{
		return (intensifiers.contains(word)); 
		
		
	}
	
	public int getNumberOfFlips(String sentence, boolean stem, boolean stop, boolean removePunctuation)
	{
	
	Tokenizer t = new Tokenizer(true,false,true);

	String temp_sentence = sentence;

	temp_sentence = t.tokenizeAndReturnString(temp_sentence, stem, stop, removePunctuation);

	temp_sentence = temp_sentence.trim();
	StringTokenizer st = new StringTokenizer(temp_sentence," ");
	int num_flips = 0;
	int multiplier = 1;
	int prev_score = 0;
	while(st.hasMoreTokens())
	{
		String word = st.nextToken();
		
		int curr_score = sw.getSentimentOfWord(word);

		if (word.equals("but") || word.equals("although") || word.equals("though")||word.equals("unless")|| word.equals("until") || word.equals("till"))
            curr_score = 0;
		
		if (multiplier != 1 && curr_score != 0)
		{
			curr_score = curr_score * multiplier;
			multiplier = 1;
		}
		
		
		if (isIntensifier(word))
			multiplier = 2;
		
		if (isNegator(word))
			multiplier *= -1;
		
		if (curr_score < 0 && prev_score > 0) num_flips++;
		if (curr_score > 0 && prev_score < 0) num_flips++;

		
		if (curr_score != 0)
			prev_score = curr_score;
	}

		g.flips = num_flips;
		return num_flips;


}
	public int getSentimentOfSentence(String sentence, boolean stem,boolean stop, boolean removePunctuation)
	{
		
		Tokenizer t = new Tokenizer(true,false,true);

		String temp_sentence = sentence;

		temp_sentence = t.tokenizeAndReturnString(temp_sentence, stem, stop, removePunctuation);

		temp_sentence = temp_sentence.trim();
		StringTokenizer st = new StringTokenizer(temp_sentence," ");
		int pos_score = 0, neg_score = 0, word_count = 0;
		int multiplier = 1;
		g.pos=0 ; g.neg=0; 
		while(st.hasMoreTokens())
		{
			String word = st.nextToken();
			
			int curr_score = sw.getSentimentOfWord(word);

			if (multiplier != 1 && curr_score != 0)
			{
				
				curr_score = curr_score * multiplier;
				multiplier = 1;
			}
			
			
			if (isIntensifier(word))
				multiplier = 2;
			
			if (isNegator(word))
				multiplier *= -1;
			
			if (curr_score < 0) neg_score += curr_score;
			if (curr_score > 0) pos_score += curr_score;

			word_count++;
		}
		g.pos=pos_score;
		g.neg=neg_score;
		if (pos_score != 0 || neg_score != 0)
		{
			if (pos_score > Math.abs(neg_score))
				return pos_score;
			else
				return neg_score;
		}
		
		return 0;
		
	}
	public static void load(String[] args)
	{
		for (String arg: args) {
			String[] s = arg.split("=");
			String param = s[0];
			String val = s[1];

			if (param.equals("sentilist")) sw.hm_filepath = val; 


		}

	}

	public SentimentSentence(String sentilist)
	{
		
		negators = getNegators();
		intensifiers = getIntensifiers();
		
		if (this.sw.hm_filepath.equals(""))
			this.sw.hm_filepath = sentilist; 
		
		sw = new SentimentWord();
	}
	public SentimentSentence()
	{
		
		negators = getNegators();
		intensifiers = getIntensifiers();
			
		sw = new SentimentWord();
	}
	public static void main(String[] args){

		load(args);

		SentimentSentence ss = new SentimentSentence("");
		
			String patht="/Users/slfrawesome/Downloads/Intern IITB/PY/DataSet/positivetext"; // path of sarcastic test tweets
		int flip=0; // saves the value return by calling getNumberOfFlips
        try{ BufferedReader br = new BufferedReader(new FileReader(patht)); 
    		String line;
    		
    		while ((line = br.readLine()) != null) {
    			FileWriter fw=new FileWriter("/Users/slfrawesome/Downloads/Intern IITB/PY/flips/ptweetsvalue",true); // path to save number of flips in sarcastic test tweets
        		BufferedWriter bw= new BufferedWriter(fw);
        		flip = ss.getNumberOfFlips(line,true,true,false);// function for flips
        		System.out.println(flip);
    			bw.write(flip+"\n");
    			bw.close();
    		}
        }
        catch (Exception e)
        {
    		System.err.println(e.getMessage()); // handle exception
    	}   

		String pathtn="/Users/slfrawesome/Downloads/Intern IITB/PY/DataSet/negativetext"; // path of non-sarcastic test tweets
        try{ BufferedReader br = new BufferedReader(new FileReader(pathtn)); 
    		String line;
    		while ((line = br.readLine()) != null) {
    			FileWriter fw=new FileWriter("/Users/slfrawesome/Downloads/Intern IITB/PY/flips/ntweetsvalue",true); // path to save number of flips in sarcastic test tweets
        		BufferedWriter bw= new BufferedWriter(fw);
        		flip = ss.getNumberOfFlips(line,true,true,false);// function for flips
        		System.out.println(flip);
    			bw.write(flip+"\n");
    			bw.close();
    		}		
        }
        catch (Exception e)
        {
    		System.err.println(e.getMessage()); // handle exception
    	}   
	}
}
