<?php

   //Connecting to Redis server on localhost
   $redis = new Redis();
   $redis->connect('127.0.0.1', 6379);
   echo "Connected to server sucessfully" . "<br>";
   echo "<hr>";
   $pumpOnError = $pumpOffError = $lightOnError = $lightOffError = "";
   $pumpOnTime = $pumpOffTime = $lightOnTime = $lightOffTime = "";

   if(isset($_POST['submit'])) {
     if (empty($_POST["lightOnTime"])) {
       $lightOnError = "Light On Timer Unchanged";
     } else {
       $redis->set("lightOnTime", $_POST['lightOnTime']);
     }

     if (empty($_POST["lightOffTime"])) {
       $lightOffError = "Light Off Timer Unchanged";
     } else {
       $redis->set("lightOffTime", $_POST['lightOffTime']);
     }

     if (empty($_POST["pumpOnTime"])) {
       $pumpOnError = "Pump On Timer Unchanged";
     } else {
       $redis->set("pumpOnTime", $_POST['pumpOnTime']);
     }

     if (empty($_POST["pumpOffTime"])) {
       $pumpOffError = "Pump Off Timer Unchanged";
     } else {
       $redis->set("pumpOffTime", $_POST['pumpOffTime']);
     }

   }
   echo "<p>Current Timers:";
   echo "<br>Light On Timer: " . $redis->get("lightOnTime") . " seconds";
   echo "<br>Light Off Timer: " . $redis->get("lightOffTime") . " seconds";
   echo "<br>Pump On Timer: " . $redis->get("pumpOnTime") . " seconds";
   echo "<br>Pump Off Timer: " . $redis->get("pumpOffTime") . " seconds";
?>

<form method="post">
<p>Light On Timer: <input type="text" name="lightOnTime" />
<br>Default: 57600 sec
<span class="error">* <?php echo $lightOnError;?></span><br>
<p>Light Off Timer: <input type="text" name="lightOffTime" />
<br>Default: 28800 sec
<span class="error">* <?php echo $lightOffError;?></span><br>
<p>Pump On Timer: <input type="text" name="pumpOnTime" />
<br>Default: 300 sec
<span class="error">* <?php echo $pumpOnError;?></span><br>
<p>Pump Off Timer: <input type="text" name="pumpOffTime" />
<br>Default 900 sec
<span class="error">* <?php echo $pumpOffError;?></span><br>
<p><input type="submit" name="submit" value="Submit" />
</form>

<p>Quick Reference Guide:
<p>300 sec = 5 min
<br>3600 sec = 1 hour
<br>28800 sec = 8 hours
<br>57600 sec = 16 hours
