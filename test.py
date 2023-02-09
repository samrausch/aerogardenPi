import RPi.GPIO as GPIO
import time
import redis
import sched
from RPLCD import i2c

lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1

lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
  cols=cols, rows=rows)

s = sched.scheduler(time.time, time.sleep)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Default values are stored in 'aerogardenInit.py', which is run when the Pi boots
# Verify the values below in that file if you believe they have been changed from the defaults shown here
#
# r.set('pumpPIN', '17')
# r.set('pumpState', 'Off')
# r.set('pumpTimer', '300')
# r.set('lightPIN', '27')
# r.set('lightState', 'Off')
# r.set('lightTimer', '3600')
# r.set('pumpLastAction', time.time())
# r.set('lightsLastAction', time.time())

pumpPIN = int(r.get('pumpPIN'))
lightPIN = int(r.get('lightPIN'))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pumpPIN,GPIO.OUT)
GPIO.setup(lightPIN,GPIO.OUT)

GPIO.output(pumpPIN,1)
GPIO.output(lightPIN,1)

def updateLCD():
	pumpState = r.get('pumpState')
	if( int(pumpState) == 0 ):
		pumpStateString = "On"
	elif( int(pumpState) == 1 ):
		pumpStateString = "Off"
	pumpTimer = float(r.get('pumpTimer'))
	pumpLastAction = float(r.get('pumpLastAction'))
	lightState = r.get('lightState')
	if( int(lightState) == 0 ):
		lightStateString = "On"
	elif( int(lightState) == 1 ):
		lightStateString = "Off"
	lightTimer = float(r.get('lightTimer'))
	lightLastAction = float(r.get('lightLastAction'))
	lcd.close(clear=True)
	lcd.write_string(str(time.strftime("%I:%M %p %a %m/%d")))
	lcd.crlf()
	pumpStateOutput = "P: " + pumpStateString + " " + str(time.strftime("%I:%M %p", time.localtime(pumpLastAction + pumpTimer)))
	lcd.write_string(pumpStateOutput)
	lcd.crlf()
	lightStateOutput = "L: " + lightStateString + " " + str(time.strftime("%I:%M %p", time.localtime(lightLastAction + lightTimer)))
	lcd.write_string(lightStateOutput)
	lcd.crlf()
	s.enter(10, 1, updateLCD)

def updateDevices():
	pumpLastAction = float(r.get('pumpLastAction'))
	pumpTimer = int(r.get('pumpTimer'))
	pumpState = int(r.get('pumpState'))
	pumpOnTime = int(r.get('pumpOnTime'))
	pumpOffTime = int(r.get('pumpOffTime'))
	if( pumpLastAction + pumpTimer <= time.time() ):
		if( pumpState == 0):
			r.set('pumpState', 1)
			r.set('pumpTimer', pumpOffTime)
			r.set('pumpLastAction', time.time())
			GPIO.output(pumpPIN, 1)
		elif ( pumpState == 1 ):
			r.set('pumpState', 0)
			r.set('pumpTimer', pumpOnTime)
			r.set('pumpLastAction', time.time())
			GPIO.output(pumpPIN, 0)

	lightLastAction = float(r.get('lightLastAction'))
	lightTimer = int(r.get('lightTimer'))
	lightState = int(r.get('lightState'))
	lightOnTime = int(r.get('lightOnTime'))
	lightOffTime = int(r.get('lightOffTime'))
	if( lightLastAction + lightTimer <= time.time() ):
		if( lightState == 0):
			r.set('lightState', 1)
			r.set('lightTimer', lightOffTime)
			r.set('lightLastAction', time.time())
			GPIO.output(lightPIN, 1)
		elif ( lightState == 1 ):
			r.set('lightState', 0)
			r.set('lightTimer', lightOnTime)
			r.set('lightLastAction', time.time())
			GPIO.output(lightPIN, 0)
	s.enter(30, 1, updateDevices)


lcd.close(clear=True)
lcd.write_string("Aerogarden Pi Server")
lcd.crlf()
lcd.write_string("V: 1.03")
lcd.crlf()
lcd.write_string("bit.ly/AeroPiCode")

s.enter(10, 1, updateLCD)
s.enter(30, 1, updateDevices)

while(True):
	s.run()

