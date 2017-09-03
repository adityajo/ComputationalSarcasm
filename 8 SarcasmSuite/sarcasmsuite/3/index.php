<!DOCTYPE HTML>
<html>
	<head>
		
    	<!-- Title of Page -->
        <title>
       		CS699-Lab11-PHPThree
        </title>
        <style>
			#eventForm .form-control-feedback {
				top: 0;
				right: -15px;
			}
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
			.table td {
				text-align: center;
			}
        </style>
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
			$('#datePicker2')
			.datepicker({
				autoclose: true,
				format: 'yyyy/mm/dd'
			})
			$('#formadddiv').hide();
			$('#formdeldiv').hide();
			$('#formupddiv').hide();
			$('#formdisddiv').hide();
			$('#formdisadiv').hide();
			$('#submitbuttondiv').hide();
		});
		</script>
		
		<script>
		$(function(){
			$("#button1-add").click(function(){
				$("#formdeldiv").hide();				
				$("#formupddiv").hide();				
				$("#formdisadiv").hide();								
				$("#formdisddiv").hide();
				$('#submitbuttondiv').hide();				
				$('<input>').attr({
					type: 'hidden',
					id: 'task',
					name: 'task',
					value: 'add'
				}).appendTo('#eventForm');			
				$("#formadddiv").show(1000);
				$('#submitbuttondiv').delay(1000).fadeIn(300);
				//alert('1clicked!');
			});
		});
		$(function(){
			$("#button2-del").click(function(){
				$("#formadddiv").hide();				
				$("#formupddiv").hide();				
				$("#formdisadiv").hide();								
				$("#formdisddiv").hide();
				$('#submitbuttondiv').hide();								
				$('<input>').attr({
					type: 'hidden',
					id: 'task',
					name: 'task',
					value: 'del'
				}).appendTo('#eventForm');				
				$("#formdeldiv").show(1000);
				$('#submitbuttondiv').delay(1000).fadeIn(300);
				//alert('2clicked!');
			});
		});
		$(function(){
			$("#button3-upd").click(function(){
				$("#formadddiv").hide();				
				$("#formdeldiv").hide();				
				$("#formdisadiv").hide();								
				$("#formdisddiv").hide();
				$('#submitbuttondiv').hide();				
				$('<input>').attr({
					type: 'hidden',
					id: 'task',
					name: 'task',
					value: 'upd'
				}).appendTo('#eventForm');	
				$("#formupddiv").show(1000);
				$('#submitbuttondiv').delay(1000).fadeIn(300);
				//alert('3clicked!');
			});
		});
		$(function(){
			$("#button4-disd").click(function(){
				$("#formadddiv").hide();				
				$("#formdeldiv").hide();				
				$("#formdisadiv").hide();								
				$("#formupddiv").hide();
				$('#submitbuttondiv').hide();								
				$('<input>').attr({
					type: 'hidden',
					id: 'task',
					name: 'task',
					value: 'disd'
				}).appendTo('#eventForm');			
				$("#formdisddiv").show(1000);	
				$('#submitbuttondiv').delay(1000).fadeIn(300);
				//alert('4clicked!');
			});
		});
		$(function(){
			$("#button5-disa").click(function(){
				$("#formadddiv").hide();				
				$("#formdeldiv").hide();				
				$("#formdisddiv").hide();								
				$("#formupddiv").hide();	
				$('#submitbuttondiv').hide();				
				$('<input>').attr({
					type: 'hidden',
					id: 'task',
					name: 'task',
					value: 'disa'
				}).appendTo('#eventForm');
				$("#eventForm").submit();
				//alert('5clicked!');
			});
		});

		</script>
                
    </head>
    
    <body>
        <div class="container">
            <div class="row">
            	<div class="col-xs-12 page-header">
                	<span style="font-size:24px">Lab11-Script3</span>                		
                </div>
            </div>
        
        	<div class="row">
            	
            	<div class="col-xs-12">

					<button class="btn btn-lg btn-primary" id="button1-add" name="button1-add">Add Event</button> &nbsp; &nbsp; &nbsp;
					<button class="btn btn-lg btn-danger" id="button2-del" name="button2-del">Delete Event</button> &nbsp; &nbsp; &nbsp;
					<button class="btn btn-lg btn-warning" id="button3-upd" name="button3-upd">Update Event</button> &nbsp; &nbsp; &nbsp;
					<button class="btn btn-lg btn-success" id="button4-disd" name="button4-disd">Display Events (by day)</button> &nbsp; &nbsp; &nbsp;
					<button class="btn btn-lg btn-success" id="button5-disa" name="button5-disa">Display Events (all)</button> &nbsp; &nbsp; &nbsp;
					<br/><br/>
					<form action="process.php" id="eventForm" name="eventForm" method="post" class="form-horizontal">
						<div id="formadddiv" class="col-xs-10">
							<br/>
							<h1>Add an Event</h1>
							<br/>
							<div class="form-group">
								<label class="col-xs-3 control-label">Event Date</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date" id="datePicker">
										<input type="text" class="form-control" name="date" id="addeventdate" placeholder="Enter Event Date Here! (YYYY/MM/DD)" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-calendar"></span></span>
									</div>
								</div>
							</div>
							<br/>
							<div class="form-group">
								<label class="col-xs-3 control-label">Event Start Time</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date" id="datePicker">
										<input type="text" class="form-control" name="addeventstime" id="addeventstime" placeholder="Enter Event Start Time Here! (HH:MM:SS)" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-time"></span></span>
									</div>
								</div>
							</div>
							<br/>
							<div class="form-group">
								<label class="col-xs-3 control-label">Event End Time</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date" id="datePicker">
										<input type="text" class="form-control" name="addeventetime" id="addeventetime" placeholder="Enter Event End Time Here! (HH:MM:SS)" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-time"></span></span>
									</div>
								</div>
							</div>
							<br/>
							<b>Event Description:&nbsp;</b><br/><textarea class="form-control" name="addeventdesc" id="addeventdesc" placeholder="Enter Event Description Here!" rows="4"></textarea>
							<br/>
						</div>
						<div id="formdeldiv" class="col-xs-10">
							<br/>
							<h1>Delete an Event</h1>
							<br/>
							<?php
								$servername = "1.db.cse.iitb.ac.in";
								$username = "cs699user";
								$password = "cs699user@123";
								$dbname = "cs699db";
								
								$conn = new mysqli($servername, $username, $password, $dbname);
								
								if ($conn->connect_error) {
									die("Connection failed: ".$conn->connect_error);
								}
								$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event";
								$result = $conn->query($sql);
								
								if ($result->num_rows > 0) {
									echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
									while($row = $result->fetch_assoc()) {
										echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
									}
									echo "</table>";
								} else {
									echo "<table class=\"table table-striped table-bordered\"><th>Table has no data!</th></table>";
								}
								$conn->close();
							?>
							<div class="form-group">
								<label class="col-xs-3 control-label">Event ID</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date">
										<input type="text" class="form-control" name="eventdelid" id="eventdelid" placeholder="Enter Event ID for Deletion!" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-remove-circle"></span></span>
									</div>
								</div>
							</div>
							<br/>
						</div>
						<div id="formupddiv" class="col-xs-10">
							<br/>
							<h1>Update an Event</h1>
							<br/>
							<?php
								$servername = "1.db.cse.iitb.ac.in";
								$username = "cs699user";
								$password = "cs699user@123";
								$dbname = "cs699db";
								
								$conn = new mysqli($servername, $username, $password, $dbname);
								
								if ($conn->connect_error) {
									die("Connection failed: ".$conn->connect_error);
								}
								$sql = "SELECT event_id, event_date, start_time, end_time, description FROM event";
								$result = $conn->query($sql);
								
								if ($result->num_rows > 0) {
									echo "<table class=\"table table-striped table-bordered\"><th>Event ID</th><th>Event Date</th><th>Start Time</th><th>End Time</th><th>Description</th>";
									while($row = $result->fetch_assoc()) {
										echo "<tr><td>". $row["event_id"] . "</td><td>". $row["event_date"]."</td><td>". $row["start_time"]."</td><td>". $row["end_time"]."</td><td>". $row["description"]."</td></tr>";
									}
									echo "</table>";
								} else {
									echo "<table class=\"table table-striped table-bordered\"><th>Table has no data!</th></table>";
								}
								$conn->close();
							?>
							<div id="formdeldiv" class="col-xs-10">
							<div class="form-group">
								<label class="col-xs-3 control-label">Event ID</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date">
										<input type="text" class="form-control" name="eventupdid" id="eventupdid" placeholder="Enter Event ID for Updation!" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-ok-circle"></span></span>
									</div>
								</div>
							</div>
							<br/>
						</div>
						</div>
						<div id="formdisddiv" class="col-xs-10">
							<br/>
							<h1>Display an Event</h1>
							<br/>
							<br/>
							<div class="form-group">
								<label class="col-xs-3 control-label">Event Date</label>
								<div class="col-xs-5 date">
									<div class="input-group input-append date" id="datePicker2">
										<input type="text" class="form-control" name="eventdisdid" id="eventdisdid" placeholder="Enter Event Date Here! (YYYY/MM/DD)" />
										<span class="input-group-addon add-on"><span class="glyphicon glyphicon-calendar"></span></span>
									</div>
								</div>
							</div>
							<br/>
						</div>
						<div id="submitbuttondiv" class="col-xs-10">
							<button type="submit" id="subbut" class="btn btn-lg btn-success" value="Submit">Submit</button>
							<br/><br/>
						</div>
					</form>
					 
				</div>
                <div class="col-xs-2">
                </div>
         	</div>
       	</div>

    </body>
</html>
