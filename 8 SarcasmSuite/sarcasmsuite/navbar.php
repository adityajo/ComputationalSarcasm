<?php 

$ext = pathinfo($filename, PATHINFO_FILENAME);
//echo $ext;

?>
<style>
.inverse-dropdown{
  background-color: #FFFF;
  border-color: #080808;
  &>li>a{
    color: #FFFF;
    &:hover{
      color: #fff;
      background-color: #000;
    }
  }
  &>.divider {
    background-color: #000;
  }
}
</style>
<nav  class="navbar navbar-inverse" role="navigation" style="margin-top:0px;">
	<div class="container-fluid">
		<!-- Brand and toggle get grouped for better mobile display -->
		<div class="navbar-header">
		<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
			<span class="sr-only">Toggle navigation</span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
		</button>
    </div>
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
    	<ul class="nav navbar-nav" style="width:100%;">
			<li <?php if($ext=="index"){ echo "class=\"active\""; } ?>><a href="./index.php" >Home</a></li>
			<li><a onclick="location.reload();" href="javascript:void(0)">Refresh</a></li>
						<li><a onclick = "window.open('about.html','About Tool','location=no,scrollbars=yes,height=600,width=600')" href="javascript:void(0)">About Sarcasm Suite</a></li>
	
			<li <?php if($ext=="SarcasmGen"){ echo "class=\"active\""; } ?>><a href="SarcasmGen.php">Sarcasm Generator</a></li>
	
			<li class="dropdown dropdown-inverse">
				<a id="drop4" href="#" class="dropdown-toggle" data-toggle="dropdown">Sarcasm Detection <b class="caret"></b></a>
				<ul class="dropdown-menu inverse-dropdown">
					<li <?php if($ext=="sentimentInc"){ echo "class=\"active\""; } ?>><a href="sentimentInc.php">Using Sentiment Incongruity</a></li>						
					<li <?php if($ext=="semanticInc"){ echo "class=\"active\""; } ?>><a href="semanticInc.php">Using Semantic Incongruity</a></li>						
					<li <?php if($ext=="HisConInc"){ echo "class=\"active\""; } ?>><a href="HisConInc.php">Using Historical Context Incongruity</a></li>
					<li <?php if($ext=="ConvConInc"){ echo "class=\"active\""; } ?>><a href="ConvConInc.php">Using Conversational Context Incongruity</a></li>	
				</ul>
			</li>
		<!--li class="navbar-right" style="float:right;"><a href="./admin/logout.php">Logout</a></li-->		
		</ul>
	</div>
	</center>
</nav>
