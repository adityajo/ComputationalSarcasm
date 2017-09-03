<!DOCTYPE HTML>
<html>
	<head>
    	<!-- Title of Page -->
        <title>
       		CS699-Lab11-PHPTwo
        </title>
        
        <!-- jQuery local -->
        <script src="../base/jquery.js"></script>
        
        <!-- Bootstrap headers required -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">        
		<link href="../bootstrap/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />


		<script src="../bootstrap/js/plugins/sortable.min.js" type="text/javascript"></script>

		<script src="../bootstrap/js/plugins/purify.min.js" type="text/javascript"></script>
		
		<script src="../bootstrap/js/fileinput.min.js"></script>

		<script src="../bootstrap/js/bootstrap.min.js"></script>
		<!-- optionally if you need a theme like font awesome theme you can include 
			it as mentioned below -->
		<script src="../bootstrap/themes/fa/theme.js"></script>
	<head>
</html>

<a href="album.php"><button type="button" class="btn btn-primary">Back to album</button></a>
<?php
	session_start();
	if(isset($_SESSION['msg']) && $_SESSION['msg']=="OK"){
		$target_dir = "images/";
		$target_file = $target_dir . basename($_FILES["input-1"]["name"]);
		$uploadOk = 1;
		$FileType = pathinfo($target_file,PATHINFO_EXTENSION);
		if ($_FILES["input-1"]["size"] > 204800) { //200KB is 204800 not 200000
			echo "<br/><br/>Sorry, your file is too large.<br/><br/>";
			$uploadOk = 0;
		}
		if($FileType != "jpg" && $FileType != "gif" && $FileType != "jpeg" && $FileType != "png") {
			echo "<br/><br/>Sorry, only image files are allowed.<br/><br/>";
			$uploadOk = 0;
		}
		$csv = file('images.csv');
		
		foreach($csv as $line) {
			$line = str_getcsv($line);
			$array[$line[0]] = trim($line[1]);
		}
		$end=sizeof($array);
		if($end==10){
			echo "<br/><br/>Sorry, Only 10 files are allowed.<br/><br/>";
			$uploadOk = 0;
		}
		if($end==1){
			$curr = $end;
		}
		else{
			$curr = $end + 1;
		}
		if ($uploadOk == 0) {
			echo "<br/><br/>No file was uploaded.<br/><br/>";
		} else {
			$currName = $curr . "." . $FileType;
			$target_file = $target_dir . basename($currName);
			echo $target_file;
			if (move_uploaded_file($_FILES["input-1"]["tmp_name"], $target_file)) {
				echo "<br/><br/>The file ". $target_file . " has been uploaded.<br/>";
				$file = fopen("images.csv","a");
				$file2 = fopen("backup.csv","a");
				$line=array($curr,$currName);
				print_r($line);
				fputcsv($file,$line);
				fputcsv($file2,$line);
				fclose($file2);
				fclose($file);
			} else {
				echo "<br/><br/>Sorry, there was an error uploading your file.<br/><br/>";
			}
		}
		echo "<br/><br/>";
	}
	else{
		header("location:index.php");
	}
?>
