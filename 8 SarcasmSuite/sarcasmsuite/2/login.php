<?php 

session_start();
	
	
	if(isset($_POST['Submit'])){
	
		$logins = array('diptesh' => 'diptesh','eval' => 'eval'); //Server side, secure, don't worry, could have easily used a mysql connection and encrypted storage using md5, but do not have the time.

		$Username = isset($_POST['Username']) ? $_POST['Username'] : '';
		$Password = isset($_POST['Password']) ? $_POST['Password'] : '';
		
	
		if (isset($logins[$Username]) && $logins[$Username] == $Password){
			$_SESSION['UserData']['Username']=$logins[$Username];
			$_SESSION['msg']="OK";
			header("location:album.php");
			exit;
		} else {
			$msg="<span style='color:red'>Invalid Login Details</span>";
			$_SESSION['msg']="No";
			header("location:index.php");
		}
	}
?>
