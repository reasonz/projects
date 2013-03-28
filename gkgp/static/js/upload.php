<?php
	// Work-around for setting up a session because Flash Player doesn't send the cookies
	if (isset($_POST["PHPSESSID"])) {
		session_id($_POST["PHPSESSID"]);
	}
	session_start();
    $json = '{"result":"true", "url":"http://180.153.99.73/?token=95133885_162744364"}';  
    echo $json;
	// The Demos don't save files
	
	exit(0);
?>