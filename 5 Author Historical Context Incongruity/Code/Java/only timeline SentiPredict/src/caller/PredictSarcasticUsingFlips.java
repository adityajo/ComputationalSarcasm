package caller;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import SentencePredictor.SentimentSentence;

public class PredictSarcasticUsingFlips {

	static double totPrecision = 0.0d;
	static double totRecall = 0.0d;
	static double totalRuns = 0.0d;
	public static void main(String[] args) throws IOException{
		String filename = "/data/aa1/PhD_Sem4/Vinita_CD/System/SarcasmSystem/corpus/CorpusWithUser";
		PredictSarcasticUsingFlips fi = new PredictSarcasticUsingFlips();
		
	//	fi.fileToFile(filename, true); 
		
		filename= "/data/aa1/PhD_Sem4/Vinita_CD/System/SarcasmSystem/corpus/CorpusWithoutUser";
	//	fi.fileToFile(filename, true);
		
		filename = "/data/aa1/PhD_Sem3/PoliticalTopicModels/PoliticalCorpus_US/all.clean";
	//	fi.fileToFile(filename, false);
		filename="/data/aa1/PhD_Sem4/Sarcasm/test";
		fi.fileToFile(filename, true);
		
		filename="/data/aa1/PhD_Sem4/Sarcasm/test.f1";
	//	fi.fileToFile(filename, true);
		filename="/data/aa1/PhD_Sem4/Sarcasm/test.f2";
	//	fi.fileToFile(filename, true);
		filename="/data/aa1/PhD_Sem4/Sarcasm/test.f3";
		//fi.fileToFile(filename, true);
		filename="/data/aa1/PhD_Sem4/Sarcasm/test.f4";
		//fi.fileToFile(filename, true);
		filename="/data/aa1/PhD_Sem4/Sarcasm/test.f5";
		//fi.fileToFile(filename, true);
		
	}
	
	public static void fileToFile(String filename, boolean isSarcasmAnnotated) throws IOException{
		BufferedReader s = new BufferedReader(new FileReader(new File(filename)));
	
		totalRuns++;
		String line = "";
		SentimentSentence ss = new SentimentSentence("/data/aa1/PhD_Sem3/SentiTranslation/sentiwordlist");
		
		int count=0;
		int curr_flips;
		int true_positive = 0, false_positive = 0, false_negative = 0;
	
		int totalSarc = 0;
		while((line=s.readLine())!=null)
		{
			
			line = s.readLine();
			
			System.out.println(line);
				
				
				curr_flips = ss.getNumberOfFlips(line, true,true,false);
				
				if (curr_flips == -1)
				{
					
						System.out.println("count = "+count);
						System.out.println("###");
					return;
					
				}
				count++; 
				
				
				if (line.trim().endsWith("$$SAR$$"))
				{
					if (curr_flips > 0)
						true_positive++;
					else
						false_negative++;
				}
				else if (line.trim().endsWith("$$NSAR$$"))
				{
					if (curr_flips > 0)
						false_positive++;
					
						
				}
				
			//}
		}
		
		
		double precision, recall;
		
		
		precision = (double)true_positive / (double)(true_positive+false_positive);
		recall = (double)true_positive/ (double)(true_positive+false_negative);
		totPrecision += precision;
		totRecall += recall;
		
		System.out.println("================");
		System.out.println("Statistics\n============");
		System.out.println("File: "+filename);
		System.out.println("Total tweets:"+count);
		
		System.out.println("True/False positives:"+true_positive+"/"+false_positive);
		System.out.println("False negative:"+false_negative);
		System.out.println("Precision:"+precision);
		System.out.println("Recall:"+recall);
		System.out.println("Average Precision:"+totPrecision/totalRuns);
		System.out.println("Average Recall:"+totRecall/totalRuns);
	}
}
