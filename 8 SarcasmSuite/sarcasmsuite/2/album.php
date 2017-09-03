<?php session_start(); 

	if(!isset($_SESSION['UserData']['Username'])){
		header("location:index.php");
		exit;
	}
	$csv = file('images.csv');
			
	foreach($csv as $line) {
		$line = str_getcsv($line);
		$array[$line[0]] = trim($line[1]);
	}
	$end=sizeof($array);
	

	//Setting default image_id
	$image_id = '1';
	
	if(isset($_GET['image_id'])){
		$image_id = $_GET['image_id'];
	}
	if($image_id > $end){
		$image_id = 1;
		header("location:album.php?&image_id=1");
	}
	if($image_id < 1){
		$image_id = 1;
		header("location:album.php?&image_id=1");
	}
	//var_dump($array);
	$file=isset($array[$image_id]) ? $array[$image_id] : null;
	$nextFile=isset($array[$image_id+1]) ? $array[$image_id+1] : null;
	$prevFile=isset($array[$image_id-1]) ? $array[$image_id-1] : null;
	//echo $file;
	if($file == null){
		$image_id = 1;
		header("location:album.php?&image_id=1");
	}

?>

<!DOCTYPE HTML>
<html>
	<head>
    	
    	<!-- Change author to your name -->
    	<meta name="author" content="Diptesh"/>
        
        <!-- Title of Page -->
        <title>
       		Photo Viewer || Photo Album
        </title>
        
        <!-- Bootstrap -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">        
		<script src="../bootstrap/js/bootstrap.min.js"></script>
		
		<script>
			<!-- Javascript goes here -->
		</script>
		
		<style>
			a{
				color: inherit;
			}
			a:hover{
				color: inherit;
			}
		</style>
		        
    </head>
    
    <body>
    
    	<!-- Page Container -->
        <div class="container">
        	
            <div class="row">
            	<div class="col-xs-12 jumbotron well well-lg">
                	<strong> Photo Album </strong>
                	
                	<div class="pull-right">
                		<a href="new_upload.php" class="btn btn-info" role="button">Upload New Image</a>
                		<a href="delete.php?&image_id=<?php echo $image_id; ?>" class="btn btn-warning" role="button">Delete from DB</a>
                		<a href="logout.php" class="btn btn-danger" role="button">Logout</a>
                	</div>
                </div>
            </div>
        
        	<div class="row" style="min-height:500px;">
        		
        		<div class="col-xs-3">
        		</div>

            	<div class="col-xs-6">
            		 <img src="images/<?php echo $file; ?>" class="img-thumbnail" width="600">
               	</div> 
               	
               	<div class="col-xs-3">        			
        		</div>    		
        		
         	</div>
         	
         	<div class="row">
         		<!-- 
         			You will have to change the button to dynamically assign url with images ids
         			The navigation should look at the number of images you have stored and navigate accordingly
         			Invalid navigations not allowed
         				Eg: If you had 5 images, and you were on the last image a next click shouldn't be possible         			
         		-->        		
         		<div class="col-xs-12" style="text-align:center">
		     		<div class="btn-group">
						<?php if($image_id!=1) { ?>
						<a href="album.php?&image_id=1" class="btn btn-lg btn-success" role="button">  
								<span class="glyphicon glyphicon-fast-backward"></span>&nbsp;First
						</a>
						<?php } ?>
						<?php if($image_id!=1 && $prevFile!=null) { ?>
						<a href="album.php?&image_id=<?php echo $image_id-1 ?>" class="btn btn-lg btn-warning" role="button">
								<span class="glyphicon glyphicon-step-backward"></span>&nbsp;Prev  
						</a> 
						<?php } ?>
						<?php if($image_id!=$end && $nextFile!=null) { ?>
						<a href="album.php?&image_id=<?php echo $image_id+1 ?>" class="btn btn-lg btn-warning" role="button">
								Next&nbsp;<span class="glyphicon glyphicon-step-forward"></span>
						</a>
						<?php } ?>
						<?php if($image_id!=$end) { ?>
						<a href="album.php?&image_id=<?php echo $end ?>" class="btn btn-lg btn-success" role="button">
								Last&nbsp;<span class="glyphicon glyphicon-fast-forward"></span>
						</a>
						<?php } ?>
					</div>
				</div>
				<br/><br/>
         	</div>
         	
         	<div class="row">
         		<div class="col-xs-12" style="text-align:center; background-color:black; color:white; padding:10px">
                    
                    <p>
                        <span class="glyphicon glyphicon-copyright-mark"></span> Diptesh, 2016 <br>
						Original Template Credits to: Prashanth, 2016 <br>

                        All Rights Reserved.
                    </p>
                </div>
            </div>
                        
       	</div>
        <!-- End of page container -->
                            
        
    </body>
</html>
