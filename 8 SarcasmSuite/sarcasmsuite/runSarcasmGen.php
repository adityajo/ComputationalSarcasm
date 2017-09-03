<?php
	$string = $_GET['sentence'];
	//echo $string;
	$escaped_command = escapeshellcmd("java -jar /data/aa1/PhD_Sem5/ACLDemo/acldemo.jar /home/aadi/Downloads/stanford-postagger-2014-01-04/models/english-left3words-distsim.tagger /data/aa1/PhD_Sem3/PoliticalTopicModels/sentiwordlist \"$string\"");
	$mys = exec($escaped_command, $result);
	exec("echo \"$string\t$result[1]\" >> /data/aa1/PhD_Sem8/AAAI17Demo/SarcasmGenLog");
	echo "<center><b>You</b>: $string <br><b>SarcasmBot</b>: $result[1]</center>";

?>
