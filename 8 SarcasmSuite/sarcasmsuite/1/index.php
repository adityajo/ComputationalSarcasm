<!DOCTYPE HTML>
<html>
	<head>
		
    	<!-- Title of Page -->
        <title>
       		CS699-Lab11-PHPOne
        </title>
        
        <!-- jQuery local used for bootstrap -->
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
			var _validFileExtensions = [".txt"];    
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
    
    	<!-- 
    		Page container in which all the page content is present
    			
    		Import components of Bootstrap, 
    			container: A box used to wrap all the data in a HTML page
    			row: A page-wide division which contains columns
    			col: columns used to divide row into 12 divisions
    		
    		Always follow below hierarchy to design proper webpages
    			container - can contain multiple rows 
    				row	- can contain multiple cols
    					col-xs-*    			
    	-->
        <div class="container">
        	
        	<!-- Class row indicates a new page wide divison -->
            <div class="row">
            
            	<!-- 
            		Class col-xs-12 indicates that this column consumes 12 divisions of the current row 
            		Each row can max contain 12 divisons
            		Class page-header is a helper class to make a page header  
            		-->
            	<div class="col-xs-12 page-header">
                	<span style="font-size:24px">Lab11-Script1</span>                		
                </div>
            </div>
        
        	<div class="row">
            	
            	<div class="col-xs-2">
                <!-- 
                	Example for leaving first 4 of 12 divisions of the current row blank 
                	Add content here to see how positioning using col-xs-<num> helps
                -->
                </div>
                
                <!-- Content that goes between so as to center your content -->
                <div class="col-xs-6">                	
                	
                	<form action="upload.php" method="post" enctype="multipart/form-data" class="form-horizontal" onsubmit="return Validate(this);">
							<br/><br/>
							<input id="input-1" name="input-1" type="file" class="file">
							<br/><br/>
						
						<br>
					</form>
					 
                </div>	
                
                <div class="col-xs-2">
                <!-- 
                	Example for leaving last 2 of 12 divisions of the current row blank 
                	Add content here to see how positioning using col-xs-<num> helps
               	-->
                </div>
                		
         	</div>
                        
       	</div>
        <!-- End of page container -->
                            
        
        
    </body>
</html>
