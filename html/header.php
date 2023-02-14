<?php
   header("Refresh:5");
   //Connecting to Redis server on localhost
   $redis = new Redis();
   $redis->connect('127.0.0.1', 6379);
   $pumpState = $redis->get("pumpState");
   $lightState = $redis->get("lightState");
   $pumpLastAction = $redis->get("pumpLastAction");
   $lightLastAction = $redis->get("lightLastAction");
   $pumpIs = $lightIs = "";


   if ($lightState == 1) {
     $lightIs = "Off";
     $lightNextEvent = $lightLastAction + $redis->get("lightOffTime");
   } else {
     $lightIs = "On";
     $lightNextEvent = $lightLastAction + $redis->get("lightOnTime");
   }

   if ($pumpState == 1) {
     $pumpIs = "Off";
     $pumpNextEvent = $pumpLastAction + $redis->get("pumpOffTime");
   } else {
     $pumpIs = "On";
     $pumpNextEvent = $pumpLastAction + $redis->get("pumpOnTime");
   }

//   echo "Debug: " . date("h:i", $lightLastAction) . " " . date("h:i", $lightNextEvent) . " " . date("h:i", $pumpLastAction) . " " . date("h:i", $pumpNextEvent) . "<br>";

   echo "Current time: " . date("h:i:s a");
   echo "<p>Pump is: " . $pumpIs . "<br>";
//   echo "Pump next event is: " . date("h:i a", $pumpNextEvent) . "<br>";
   echo "<p>Light is: " . $lightIs . "<br>";
//   echo "Light next event is: " . date("h:i a", $lightNextEvent) . "<br>";
   echo "<p>";


?>
