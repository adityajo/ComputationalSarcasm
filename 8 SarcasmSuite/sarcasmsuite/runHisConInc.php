<?php
	$string1 = $_GET['sentence'];
	$string2 = $_GET['username'];

	exec("java -jar /data/aa1/PhD_Sem8/AAAI17Demo/wassa.jar \"$string2\" \"$string1\"", $result);
	exec("echo \"$string2 $string1 $result[0]\" >> /data/aa1/PhD_Sem8/AAAI17Demo/HistoricalLog");
	if ($result[0]=="sarc"){
		echo "1";
	}
	else{
		echo "0";
	}					
?>
