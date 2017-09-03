<!DOCTYPE HTML>
<html>
	<head>
    	
    	<meta name="author" content="Diptesh"/>
        
        <!-- Title of Page -->
        <title>
       		CS699-Lab11-PHPThree
        </title>
        
        <!-- Bootstrap -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="../base/jquery.js"></script>

	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="../bootstrap/css/bootstrap.min.css" rel="stylesheet">        
		<link href="../bootstrap/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />


		<script src="../bootstrap/js/plugins/sortable.min.js" type="text/javascript"></script>

		<script src="../bootstrap/js/plugins/purify.min.js" type="text/javascript"></script>
		
		<script src="../bootstrap/js/fileinput.min.js"></script>

		<script src="../bootstrap/js/bootstrap.min.js"></script>

		<script src="../bootstrap/themes/fa/theme.js"></script>
		<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.3.0/css/datepicker.min.css" />
		<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.3.0/css/datepicker3.min.css" />
		
		<script src="//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.3.0/js/bootstrap-datepicker.min.js"></script>
		
		<script>
		$(document).ready(function() {
			$('#datePicker')
				.datepicker({
					autoclose: true,
					format: 'yyyy/mm/dd'
				})
			});
		</script>
		<style>
			table,
			thead,
			tr,
			tbody,
			th,
			td {
				text-align: center;
			}
			.table {
				border-radius: 5px;
				width: 50%;
				margin: 0px auto;
				float: none;
			}
			#formdeldiv.col-xs-10 .table td th tr{
				text-align: center;   
			}
		</style>
	</head>
	<body>
		<br/><br/>
		<?php
		$servername = "1.db.cse.iitb.ac.in";
		$username = "cs699user";
		$password = "cs699user@123";
		$dbname = "cs699db";
		
		$conn = new mysqli($servername, $username, $password, $dbname);
		
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
		} 
		//echo "Connected successfully";
		//var_dump($_POST);
		if($_POST['task']=="add"){
			//echo "<br/>add aala!";
			
			$date = mysqli_real_escape_string($conn, $_POST['date']); // to safeguard against SQL Injection
			$stime = mysqli_real_escape_string($conn, $_POST['addeventstime']); // to safeguard against SQL Injection
			$etime = mysqli_real_escape_string($conn, $_POST['addeventetime']);// to safeguard against SQL Injection
			$desc = mysqli_real_escape_string($conn, $_POST['addeventdesc']); // to safeguard against SQL Injection
		
			$sql = "INSERT INTO event (event_date, start_time, end_time, description)
					VALUES ('".$date."', '".$stime."', '".$etime."', '".$desc."')";
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";		
			if ($conn->query($sql) === TRUE) {
				$last_id = $conn->insert_id;
				echo "<table class=\"table table-striped table-bordered\"><th colspan=2>Event Added to Database </th><tr><td>Event Date</td><td>".$date."</td></tr><tr><td>Event Start Time</td><td>".$stime."</td></tr><tr><td>Event End Time</td><td>".$etime."</td></tr><tr><td>Event Description</td><td>".$desc."</td></tr><tr><td>Last inserted ID is</td><td>".$last_id."</td></tr></table>";		
			} else {
				echo "<br/>Error: " . $sql . "<br/>" . $conn->error . "<br/>";
			}
			
		}
		else if($_POST['task']=="del"){
			//echo "<br/>del aala!";
			$id = mysqli_real_escape_string($conn, $_POST['eventdelid']); // to safeguard against SQL Injection
			$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event WHERE event_id='".$id."'";
			$result = $conn->query($sql);
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";
			if ($result->num_rows > 0) {
				echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
				while($row = $result->fetch_assoc()) {
					echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
				}
				$sql = "DELETE FROM event WHERE event_id='".$id."'";
				$result = $conn->query($sql);
				if ($conn->query($sql) === TRUE) {
					echo "<tr><td colspan=5><b>Event with ID ".$id." shown above has been deleted successfully</b></td></tr>";
				} else {
					echo "<tr><td colspan=2><b>Error Deleting ID ".$id." shown above</b></td><td colspan=3>" . $conn->error . "</td></tr>";
				}
				echo "</table>";
				
			} else {
				echo "<table class=\"table table-striped table-bordered\"><th>Table has no event data for this ID!</th></table>";
			}

			
		}
		else if($_POST['task']=="upd"){
			//echo "<br/>upd aala!";
			$id = mysqli_real_escape_string($conn, $_POST['eventupdid']); // to safeguard against SQL Injection
			$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event WHERE event_id='".$id."'";
			$result = $conn->query($sql);
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";
			if ($result->num_rows > 0) {
				echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
				while($row = $result->fetch_assoc()) {
					echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
				}
				echo "</table>";
				?>
				<br/><br/>
				<form action="" id="updateForm" name="updateForm" method="post" class="form-horizontal">
				<div class="form-group">
					<label class="col-xs-2 control-label">Event Date</label>
						<div class="col-xs-4 date">
							<div class="input-group input-append date" id="datePicker">
								<input type="text" class="form-control" name="date" id="updeventdate" placeholder="Enter Event Date Here! (YYYY/MM/DD)" />
								<span class="input-group-addon add-on"><span class="glyphicon glyphicon-calendar"></span></span>
							</div>
						</div>
					</div>
					<br/>
					<div class="form-group">
						<label class="col-xs-2 control-label">Event Start Time</label>
						<div class="col-xs-4 date">
							<div class="input-group input-append date" id="datePicker">
								<input type="text" class="form-control" name="updeventstime" id="updeventstime" placeholder="Enter Event Start Time Here! (HH:MM:SS)" />
								<span class="input-group-addon add-on"><span class="glyphicon glyphicon-time"></span></span>
							</div>
						</div>
					</div>
					<br/>
					<div class="form-group">
						<label class="col-xs-2 control-label">Event End Time</label>
						<div class="col-xs-4 date">
							<div class="input-group input-append date" id="datePicker">
								<input type="text" class="form-control" name="updeventetime" id="updeventetime" placeholder="Enter Event End Time Here! (HH:MM:SS)" />
								<span class="input-group-addon add-on"><span class="glyphicon glyphicon-time"></span></span>
							</div>
						</div>
					</div>
					<br/>
					<b>Event Description:&nbsp;</b><br/><textarea style="width:65%;" class="form-control" name="updeventdesc" id="updeventdesc" placeholder="Enter Event Description Here!" rows="4"></textarea>
					<br/>
					<div id="submitbuttondiv" class="col-xs-10">
						<button type="submit" id="subbut" class="btn btn-lg btn-success" value="Submit">Submit</button>
						<br/><br/>
					</div>
					<input type="hidden" id="task" name="task" value="updateThisForm"/>
					<input type="hidden" id="hidid" name="hidid" value="<?php echo $id; ?>"/>
					</form>
					<?php 
					
			} else {
				echo "<table class=\"table table-striped table-bordered\"><th>Table has no event data for this ID!</th></table>";
			}
		}
		else if($_POST['task']=="updateThisForm"){
			$id = mysqli_real_escape_string($conn, $_POST['hidid']); // to safeguard against SQL Injection
			$date = mysqli_real_escape_string($conn, $_POST['date']); // to safeguard against SQL Injection
			$stime = mysqli_real_escape_string($conn, $_POST['updeventstime']); // to safeguard against SQL Injection
			$etime = mysqli_real_escape_string($conn, $_POST['updeventetime']);// to safeguard against SQL Injection
			$desc = mysqli_real_escape_string($conn, $_POST['updeventdesc']); // to safeguard against SQL Injection			
			//echo $id;
			
			$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event WHERE event_id='".$id."'";
			$result = $conn->query($sql);
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";
			if ($result->num_rows > 0) {
				echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
				while($row = $result->fetch_assoc()) {
					echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
				}
				echo "</table>";
				$sql = "UPDATE event SET event_date='".$date."', start_time='".$stime."', end_time='".$etime."', description='".$desc."' WHERE event_id='".$id."'";
				//echo $sql;
				if ($conn->query($sql) === TRUE) {
					echo "<br/><table class=\"table table-striped table-bordered\"><th>Event with ID ".$id." has been updated successfully</th></table>";
				} else {
					echo "Error updating record: " . $conn->error;
				}
				$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event WHERE event_id='".$id."'";
				$result = $conn->query($sql);
				if ($result->num_rows > 0) {
					echo "<center><h1>Post Update data is : </h1></center><br/>";
					echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
					while($row = $result->fetch_assoc()) {
						echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
					}
					echo "</table>";
				}
				
			} else {
				echo "<table class=\"table table-striped table-bordered\"><th>Table has no event data for this date!</th></table>";
			}
		}
		else if($_POST['task']=="disd"){
			//echo "<br/>disd aala!";
			$date2 = mysqli_real_escape_string($conn, $_POST['eventdisdid']); // to safeguard against SQL Injection
			//echo $date2;
			$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event WHERE event_date='".$date2."'";
			$result = $conn->query($sql);
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";
			if ($result->num_rows > 0) {
				echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
				while($row = $result->fetch_assoc()) {
					echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
				}
				echo "</table>";
			} else {
				echo "<table class=\"table table-striped table-bordered\"><th>Table has no event data for this date!</th></table>";
			}
		}
		else if($_POST['task']=="disa"){
			//echo "<br/>disa aala!";
			$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event";
			$result = $conn->query($sql);
			echo "<center><a href=\"index.php\"><button class=\"btn btn-primary\" id=\"backbutton\" name=\"backbutton\"><span class=\"glyphicon glyphicon-step-backward\">&nbsp;</span>Back to Main</button></a></center><br/><br/>";
			if ($result->num_rows > 0) {
				echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
				while($row = $result->fetch_assoc()) {
					echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
				}
				echo "</table>";
			} else {
				echo "<table class=\"table table-striped table-bordered\"><th>Table has no data!</th></table>";
			}
		}
		else{
			echo "Not cool, send a task maadi!";
		}
		$conn->close();
		?>
		<br/><br/>
	</body>
</html>

