<?php
	$string = $_GET['sentence'];
	//echo $string;
	$rmcommand = escapeshellcmd("rm /data/aa1/PhD_Sem8/AAAI17Demo/emnlpoutput");
	$escaped_command = escapeshellcmd("/usr/bin/python /data/aa1/PhD_Sem8/AAAI17Demo/emnlp_testing.py \"$string\"");
	$mys = exec($escaped_command, $result);
	exec("/data/aa1/PhD_Sem7/EMNLPShort/svm_perf/svm_perf_classify /data/aa1/PhD_Sem8/AAAI17Demo/emnlptest /data/aa1/PhD_Sem8/AAAI17Demo/emnlpmodel /data/aa1/PhD_Sem8/AAAI17Demo/emnlpoutput");
	exec("awk '{if ($1<=0) print \"-1\"; else print \"+1\";}' /data/aa1/PhD_Sem8/AAAI17Demo/emnlpoutput", $result);
	exec("echo \"$string $result[0]\" >> /data/aa1/PhD_Sem8/AAAI17Demo/SemanticLog");
	//echo $result[0];
	if ($result[0]=="+1"){
		echo "1";
	}
	else{
		echo "0";
	}					 
?>
