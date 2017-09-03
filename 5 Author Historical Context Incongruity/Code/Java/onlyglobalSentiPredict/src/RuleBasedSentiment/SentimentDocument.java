package RuleBasedSentiment;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.StringTokenizer;






import SentencePredictor.SentimentSentence;
import SentencePredictor.SentimentSentencePerWord;

public class SentimentDocument {

	SentimentSentence ss;
	SentimentSentencePerWord sspw;
	
	public SentimentDocument(String sentilist)
	{
	
			ss = new SentimentSentence(sentilist);
		
			sspw = new SentimentSentencePerWord(sentilist);
	}
	
	public int getDocSentiment(String document)
	{
		
		
		StringTokenizer st = new StringTokenizer(document,"\n");
		
		int score = 9999;
		while (st.hasMoreTokens())
		{
			String sentence = st.nextToken();
			sentence = sentence.replaceAll("#", "");
			int curr_score = ss.getSentimentOfSentence(sentence, false,false,true);
			
			
			
			if (curr_score != 0 && score == 9999)
				score = 0;
			
			score += curr_score;
		}
		
		
		return score;
	}
	
	public ArrayList<Integer> getSentimentbyLine(String document)
	{
		
		ArrayList<Integer> score = new ArrayList<Integer>();
		StringTokenizer st = new StringTokenizer(document,"\n");
		
		
		while (st.hasMoreTokens())
		{
			String sentence = st.nextToken();
			int curr_score = ss.getSentimentOfSentence(sentence, false,false,true);
			
			score.add(curr_score);
		}
		
		
		return score;
	}
	

	public String getSentimentbyLinePerWord(String document)
	{
		
		String score="";
		StringTokenizer st = new StringTokenizer(document,"\n");
		
			while (st.hasMoreTokens())
		{
			String sentence = st.nextToken();
			String curr_score = sspw.getSentimentOfSentence(sentence, false,false,true);
			
			score = score+" "+curr_score;
		}
		
		
		return score;
	}
	
	public ArrayList<String> getSentimentAndSentenceByLine(String document)
	{
		
		ArrayList<String> score = new ArrayList<String>();
		StringTokenizer st = new StringTokenizer(document,"\n");
		
		
		while (st.hasMoreTokens())
		{
			String sentence = st.nextToken();
			sentence = sentence.replaceAll("#", "");
			if (sentence.trim().equals(""))
				continue;
			int curr_score = ss.getSentimentOfSentence(sentence, false,false,true);
			
			score.add(sentence+" #"+curr_score);
		}
		
		
		return score;
	}
	
	public void annotateCorpusWithSentiment(String filename, int option) throws IOException
	{
		BufferedReader br = new BufferedReader(new FileReader(new File(filename)));
    
    
		SentimentDocument sd = new SentimentDocument(filename);
		
		String out_file = filename+".out2";
		
		File file = new File(out_file);
		 
		// if file doesnt exists, then create it
		if (!file.exists()) {
			file.createNewFile();
		}
	
		FileWriter fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		
		String line = "";
		
		while((line = br.readLine()) !=null)
			{ 
			
			
			if (line.trim().equals(""))
				continue;
			
			if (option == 0)
			{
			ArrayList<String> labeled_review = sd.getSentimentAndSentenceByLine(line);
		
			String out_review="";
			
			for (String s3: labeled_review)
			{
				out_review = out_review+s3+" . ";
			}
			
			out_review = out_review.trim();
		
			bw.write(out_review+"\n");
			}
			else if (option ==1)
			{
				String labeled_review = sd.getSentimentbyLinePerWord(line);
				bw.write(labeled_review+"\n");
			}
 
		}
		
		bw.close();
	}
	
	public static void main(String args[]) throws IOException
	{
		SentimentDocument sd = new SentimentDocument(args[0]);
	//	System.out.println(sd.getSentimentAndSentenceByLine("The world is sad.\n But I am absolutely s#ad"));
	//	System.out.println(sd.getDocSentiment("The world is sad.\n But I am absolutely sad"));
		
		/* Option 1 here means word by word annotation. Option 0 means document level annotation */
		sd.annotateCorpusWithSentiment("/data/aa1/PhD_Sem3/PoliticalTopicModels/PoliticalCorpus_IN/cleaned/allIndians",  1);
	}
}
