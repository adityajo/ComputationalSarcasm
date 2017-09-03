<?php 
	session_start();
	if(isset($_SESSION['msg']) && $_SESSION['msg']=="OK"){ ?>
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
		<script>
			var _validFileExtensions = [".jpg", ".gif", ".png", ".jpeg"];    
			function Validate(oForm) {
				var arrInputs = oForm.getElementsByTagName("input");
				for (var i = 0; i < arrInputs.length; i++) {
					var oInput = arrInputs[i];
					if (oInput.type == "file") {
						var sFileName = oInput.value;
						if (sFileName.length > 0) {
							var blnValid = false;
							for (var j = 0; j < _validFileExtensions.length; j++) {
								var sCurExtension = _validFileExtensions[j];
								if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
									blnValid = true;
									break;
								}
							}
							if (!blnValid) {
								alert("Sorry, File Extension is invalid \nAllowed extensions are: " + _validFileExtensions.join(", "));
								window.location.reload(false);
								return false;
							}
						}
					}
				}
				return true;
			}
					
		</script>
                
    </head>
    
    <body>
    
    	 <div class="container">
		 <a href="album.php"><button type="button" class="btn btn-primary">Back to album</button></a>

        	
        	<!-- Class row indicates a new page wide divison -->
            <div class="row">
            
            	<div class="col-xs-12 page-header">
                	<span style="font-size:24px">Upload Image</span>                		
                </div>
            </div>
        
        	<div class="row">
            	
            	<div class="col-xs-6" style="min-height:500px;">
               		<form action="upload.php" method="post" enctype="multipart/form-data" class="form-horizontal" onsubmit="return Validate(this);">
							<br/><br/>
							<input id="input-1" name="input-1" type="file" class="file">
							<br/><br/>
						<br>
					</form>
                </div>
                		
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
<?php } 
	else{
		header("location:index.php");
	}
?>

