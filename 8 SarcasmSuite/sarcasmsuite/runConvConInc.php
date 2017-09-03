<?php
	$string = $_GET['sentence'];
	$newString = ereg_replace( "\.",'.<br/>', $string);
	$splitted_text = explode(".", $string);
	//$splitted_text = preg_split( "/ (\.|?|\!) /", $string );
	

	$myfile = fopen("/data/aa1/PhD_Sem8/AAAI17Demo/test_inp2", "w") or die("Unable to open file!");
	fclose($myfile);
	for($i = 0; $i < count($splitted_text); $i++){
		$myfile = fopen("/data/aa1/PhD_Sem8/AAAI17Demo/test_inp2", "a") or die("Unable to open file!");
		fwrite($myfile,$splitted_text[$i]."\n");
		fclose($myfile);
	}

	fclose($myfile);
	//echo "Processing: ";
	//system("cat /data/aa1/PhD_Sem8/AAAI17Demo/test_inp2");
	//for($i = 0; $i < count($splitted_text)-1; $i++){
	//	echo $splitted_text[$i] . ".<br/>";
	//}
	$escaped_command = escapeshellcmd("/usr/bin/python /data/aa1/PhD_Sem8/AAAI17Demo/conll_sequential_te.py /data/aa1/PhD_Sem8/AAAI17Demo/test_inp2 /data/aa1/PhD_Sem8/AAAI17Demo/friends.vocab");
	$mys = exec($escaped_command, $result);
	
	$escaped_command = escapeshellcmd("/data/aa1/PhD_Sem8/AAAI17Demo/svm_hmm_classify /data/aa1/PhD_Sem8/AAAI17Demo/output_seq.o /data/aa1/PhD_Sem8/AAAI17Demo/svm_struct_model /data/aa1/PhD_Sem8/AAAI17Demo/output_seq.o2");
	echo "<h2>";	
	$mys = exec($escaped_command, $result);
	$escaped_command = "sed -e 's/2/\<img class\=profile\-img4 id\=profilePic src\=images\/vaibhav\_nonsarc2.png\>\&nbsp\;/g' -e 's/1/\<img class\=profile\-img3 id=profilePic src\=images\/vaibhav\_sarc2.png\>\&nbsp\;/g' /data/aa1/PhD_Sem8/AAAI17Demo/output_seq.o2";
	$mys1 = system($escaped_command, $result);
	//print_r($result);
	echo "</h2>";
	//$newresult = ereg_replace(".","<br/>", $m);
	//exec("/data/aa1/PhD_Sem7/EMNLPShort/svm_perf/svm_perf_classify /data/aa1/PhD_Sem8/AAAI17Demo/output.o /data/aa1/PhD_Sem8/AAAI17Demo/svm_model.acl15 /data/aa1/PhD_Sem8/AAAI17Demo/finalOutput.o");
	//exec("awk '{if ($1<=0) print \"-1\"; else print \"+1\";}' /data/aa1/PhD_Sem8/AAAI17Demo/finalOutput.o", $result);
	//echo $mys;
	if ($result[0]=="+1"){
		//echo "<h1>The sentence is Sarcastic!</h1>";
	}
	else{
		//echo "<h1>NOT Sarcastic!</h1>";
	}					
?>
