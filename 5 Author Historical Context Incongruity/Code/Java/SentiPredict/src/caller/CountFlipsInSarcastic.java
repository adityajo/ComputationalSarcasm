package caller;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import SentencePredictor.SentimentSentence;

public class CountFlipsInSarcastic {

	public static void main(String[] args) throws IOException{
		String filename = "/data/aa1/PhD_Sem4/Vinita_CD/System/SarcasmSystem/corpus/CorpusWithUserInfo(10697tweets)";
		CountFlipsInSarcastic fi = new CountFlipsInSarcastic();
		
		fi.fileToFile(filename, true,10697); 
		
		filename= "/data/aa1/PhD_Sem4/Vinita_CD/System/SarcasmSystem/corpus/CorpusWithoutUserInfo(19930tweets)";
		fi.fileToFile(filename, true, 19932);
		
		filename = "/data/aa1/PhD_Sem3/PoliticalTopicModels/PoliticalCorpus_US/all.clean";
		fi.fileToFile(filename, false,2542927);
	}
	
	public static void fileToFile(String filename, boolean isSarcasmAnnotated, int length) throws IOException{
		BufferedReader s = new BufferedReader(new FileReader(new File(filename)));
		
		int count = length;
		String line = "", inputLine = "";
		SentimentSentence ss = new SentimentSentence("/data/aa1/PhD_Sem3/SentiTranslation/sentiwordlist");
		int explicit_flips = 0, implicit_flips = 0;
		double avg_num_flips = 0, avg_num_flipsInExplicit=0;
		int total_flips = 0;
		int curr_flips;
		int max_flips = 0, min_flips = 0;
		int totalSarc = 0;
		for (int i = 0; i < count; i++)
		{
			
			line = s.readLine();
			
			if ((isSarcasmAnnotated && line.trim().endsWith("$$SAR$$")) || (!isSarcasmAnnotated && line.trim().contains("#sarcasm")))
			{	
				totalSarc++;
				
				curr_flips = ss.getNumberOfFlips(line, true,true,false);
				
				total_flips += curr_flips;
				
				if (max_flips<curr_flips)
					max_flips = curr_flips;
				
				if(min_flips>curr_flips)
					min_flips = curr_flips;
				
				if (curr_flips == 0)
					implicit_flips++;
				else
					explicit_flips++;
			}
		}
		
		

		avg_num_flips = (double)total_flips/(double)totalSarc;
		avg_num_flipsInExplicit = (double)total_flips/(double)explicit_flips;
		
		System.out.println("================");
		System.out.println("Statistics\n============");
		System.out.println("File: "+filename);
		if(totalSarc == 0)
		{
			System.out.println("No sarcastic tweeets found");
			return;
		}
		
		System.out.println("Total: "+count);
		System.out.println("Max_flips in a tweet:"+max_flips);
		System.out.println("Min_flips in a tweet:"+min_flips);
		System.out.println("Explicit flips:"+explicit_flips+" ("+(double)explicit_flips/(double)totalSarc*100+"%)");
		System.out.println("Implicit flips:"+implicit_flips+" ("+(double)implicit_flips/(double)totalSarc*100+"%)");
		System.out.println("Total Sarcastic Tweets:"+totalSarc);
		
		if (totalSarc != explicit_flips+implicit_flips)
			System.out.println("Sanity check failed");
		
		System.out.println("Average explicit flips per tweet:"+avg_num_flips);
		System.out.println("Average explicit flips per Explicit Flip Tweet:"+avg_num_flipsInExplicit);
		
	}
}
