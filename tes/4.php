<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>

<?php
	for ($i=0; $i<3; $i++) {
		echo "<div style='width: 1px;margin-top: 12px;'>";
		for($a=0;$a<3;$a++){
			echo "
			<span class='blue-circle' style='
				display: block;
			    float: left;
			    margin-left: 28px;'>
			    ";
			}
		echo "</div></br>";
	}
?>

</body>
</html>

