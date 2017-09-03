package caller;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Vector;

import SentencePredictor.SentimentSentence;

public class HashTagBasedPredictor {
// this is maynard's implementation, i reckon. -aditya . 28th April
	SentimentSentence ss = new SentimentSentence("/data/aa1/PhD_Sem3/SentiTranslation/sentiwordlist");
	public boolean getIndividualPredictions(String sentence)
	{
		String splitted[] = sentence.split("#");
		
		boolean sarcPrediction = true;
		int prevSentiment = 0;
		Vector<String> sarcastic_hashtags = new Vector<String>();
	//	sarcastic_hashtags.add("sarcasm");
		sarcastic_hashtags.add("sarcastic");
		sarcastic_hashtags.add("lying");
		sarcastic_hashtags.add("notreally");
		
		if (splitted.length == 1)
		{
			if(ss.getNumberOfFlips(splitted[0], true,true,true)==1) return true; else return false;
		}
		for(int i =0; i<splitted.length;i++)
		{
			int currSentiment = ss.getSentimentOfSentence(splitted[i], true,true,true);
			if (prevSentiment != 0 && ((currSentiment<0 && prevSentiment > 0)||(currSentiment>0 && prevSentiment<0)))
					return true;
			
			if(sarcastic_hashtags.contains(splitted[i]));
			prevSentiment = currSentiment;
		}
		
		
		
		return false;
	}
	public void getPredictions(String filename) throws IOException
	{
		BufferedReader s = new BufferedReader(new FileReader(new File(filename)));
		PrintStream pstream_orig = System.out;
		System.setOut(new PrintStream(new File(filename+".olabel")));
		String str = "";
		while((str=s.readLine())!=null)
		{
			boolean predict = this.getIndividualPredictions(str);
			if (predict) System.out.println(" $$SAR$$");
			else System.out.println("$$NSAR$$");
		}
			
	}
	public static void main(String[] args) throws IOException
	{
		HashTagBasedPredictor htbp = new HashTagBasedPredictor();
		
		boolean blah =htbp.getIndividualPredictions("Giants_101 Well that 's just fantastic . # sarcasm # this actually sucks");
		if (blah) System.out.println("Sarcastic hai re!");
		else
			System.out.println("naa re.. sarcastic naa");
		
		htbp.getPredictions("/data/aa1/PhD_Sem5/HashtagTokenizer/final.cs.o");
	}
}
