<!DOCTYPE HTML>
<html>
	<head>
    	<!-- Title of Page -->
        <title>
       		CS699-Lab11-PHPOne
        </title>
        
        <!-- jQuery local -->
        <script src="../base/jquery.js"></script>
        
        <!-- Bootstrap -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">        
		<script src="../bootstrap/js/bootstrap.min.js"></script>
                
    </head>
    
    <body>
    	<!-- Page Content -->
        <div class="container">
        	
        	<!-- Class row indicates a new page wide divison -->
            <div class="row">
            
            	<div class="col-xs-12 page-header">
                	<span style="font-size:24px">Processed Output</span>                		
                </div>
            </div>
        	
        	
        	<!-- Class row indicates a new page wide divison -->
            <div class="row">
                     	
            
            	<div class="col-xs-12">
					
					<table class="table table-striped table-bordered">
						
							<?php
								$target_dir = "uploads/";
								$target_file = $target_dir . basename($_FILES["input-1"]["name"]);
								$uploadOk = 1;
								$FileType = pathinfo($target_file,PATHINFO_EXTENSION);
								if ($_FILES["input-1"]["size"] > 102400) { //100KB is 102400 not 100000
									echo "<br/><br/>Sorry, your file is too large.<br/><br/>";
									$uploadOk = 0;
								}
								if($FileType != "txt") {
									echo "<br/><br/>Sorry, only TXT files are allowed.<br/><br/>";
									$uploadOk = 0;
								}
								if ($uploadOk == 0) {
									echo "<br/><br/>No file was uploaded.<br/><br/>";
								} else {
									if (move_uploaded_file($_FILES["input-1"]["tmp_name"], $target_file)) {
										//echo "<br/><br/>The file ". basename( $_FILES["input-1"]["name"]). " has been uploaded.<br/>";
									} else {
										echo "<br/><br/>Sorry, there was an error uploading your file.<br/><br/>";
									}
								}
								$content = strtolower(file_get_contents($target_file));
 
								$wordArray = preg_split('/[^a-z]/', $content, -1, PREG_SPLIT_NO_EMPTY);
				
								$wordFrequencyArray = array_count_values($wordArray);
								
								ksort($wordFrequencyArray);
								echo "<tr>
										<th> Word </th> <th> Occurence </th>
									</tr>";
								foreach ($wordFrequencyArray as $Word => $frequency){
										echo "<tr>";
										echo "<td>$Word</td><td>$frequency</td>";
										echo "</tr>";
								
								}
								echo "</table>";
								echo "<br/><br/>";
							?>
							
					
				</div>
			</div>
				
			<div class="row">
				<div class="col-xs-12">
				</div>
			</div>
				
			</div>
	</body>
</html>

