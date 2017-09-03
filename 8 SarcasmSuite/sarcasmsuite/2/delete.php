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
	<a href="album.php"><button type="button" class="btn btn-primary">Back to album</button></a>
</html>
<?php
	session_start();
	if(isset($_SESSION['msg']) && $_SESSION['msg']=="OK"){
		$image_id=$_GET['image_id'];
		//echo $image_id;
		$csv = file('images.csv');
		foreach($csv as $line) {
			$line = str_getcsv($line);
			$array[$line[0]] = trim($line[1]);
		}
		$end=sizeof($array);
		$handle = fopen ('images.csv', 'w+');
		foreach($csv as $line) {
			$line = str_getcsv($line);
			//var_dump($line);
			if($line[0]!=$image_id && $line[0] < $image_id){
				$putLine=array($line[0],$line[1]);
				fputcsv($handle, $putLine);
			}
			else if(($line[0]!=$image_id && $line[0] > $image_id){
				$val=$line[0]-1;
				$putLine=array($val,$line[1]);
				fputcsv($handle, $putLine);
			}
			else if(($line[0]==$image_id) && ($line[0]==$end)){
				//$putLine=array(0,$line[1]);
				//fputcsv($handle, $putLine); Dont write 0 at the end, the last button stops working
			}
			//echo "<br/><br/>";
			//var_dump($array);
		}
		//delete_line($image_id);
		echo "<br/><br/>Image no. " . $image_id . " Deleted from DB, not from Server, I could have used exec to do this, but I do not want to give write perms now that is too tacky<br/>If you upload an image with the same extension it would be overwritten!! BEWARE!!";
	}
	else{
		header("location:index.php");
	}
?>
