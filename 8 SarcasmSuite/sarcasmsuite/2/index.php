<!DOCTYPE HTML>
<?php session_start(); 
if(isset($_SESSION['msg']) && $_SESSION['msg']=="OK"){
	header("location:album.php");
}
?>
<html>
	<head>
    	
    	<meta name="author" content="Diptesh"/>
        
        <title>
       		CS699-Lab11-PHPTwo
        </title>
        
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">        
		<script src="../bootstrap/js/bootstrap.min.js"></script>
		
		<script>
			<!-- Javascript goes here -->
		</script>
		        
    </head>
    
    <body>
    
        <div class="container">
        	
            <div class="row">
            	<div class="col-xs-12 jumbotron well well-lg">
                	<strong> Photo Album Login </strong> <br/>
                </div>
            </div>
        
        	<div class="row" style="min-height:500px;">
            	<div class="col-xs-12">
            	
            		<form action="login.php" method="post" name="Login_Form">
						<table width="400" border="0" align="center" cellpadding="5" cellspacing="1" class="Table">
							<?php if(isset($_SESSION['msg']) && $_SESSION['msg']=="No"){?>
							<tr>
							<td colspan="2" align="center" valign="top"><?php echo "Invalid Login Credentials!"; ?></td>
							</tr>
							<?php } ?>
							<tr>
							<td colspan="2" align="left" valign="top"><h3>Login</h3></td>
							</tr>
							<tr>
							<td align="right" valign="top">Username</td>
							<td><input name="Username" type="text" class="Input"></td>
							</tr>
							<tr>
							<td align="right">Password</td>
							<td><input name="Password" type="password" class="Input"></td>
							</tr>
							<tr>
							<td> </td>
							<td><input name="Submit" type="submit" value="Login" class="Button3"></td>
							</tr>
						</table>
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
