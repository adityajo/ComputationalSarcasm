package hello;


import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class WriteFile {
	String file_path ;
	FileWriter write;
	BufferedWriter bw;
	PrintWriter print ;
	public WriteFile(String path){
		file_path = path ;		
		
		try {
			write = new FileWriter(file_path,true);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		bw = new BufferedWriter(write);
		print = new PrintWriter(write) ;
	
	}
	//open file
	public void open(){
		try {
			write = new FileWriter(file_path,true);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		bw = new BufferedWriter(write);
		print = new PrintWriter(write) ;
	
	}
	//write to the file
	public void write(String line) throws IOException{
		
		print.println(line) ;
	}
	//close file
	public void close() {
		print.close() ;
	}
		
	
}
