from gpiozero import Button
import RPi.GPIO as GPIO
import time
import redis
import sched
import board
import digitalio
import socket
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 64
BORDER = 5

i2c = board.I2C()  # uses board.SCL and board.SDA
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

padding = -2
top = padding
bottom = HEIGHT-padding
x = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))
IP = s.getsockname()[0]

text1 = "AeroGarden Pi"
text2 = "v 1.03"
text3 = "bit.ly/AeroPiCode"
draw.text((x, top),       text1,  font=font, fill=255)
draw.text((x, top+16),    text2, font=font, fill=255)
draw.text((x, top+32),    text3,  font=font, fill=255)
draw.text((x, top+56),    "IP: " + str(IP),  font=font, fill=255)

oled.image(image)
oled.show()


s = sched.scheduler(time.time, time.sleep)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Default values are stored in 'aerogardenInit.py', which is run when the Pi boots
# Verify the values below in that file if you believe they have been changed from the defaults shown here
#
# r.set('pumpPIN', '27')
# r.set('pumpState', 'Off')
# r.set('pumpTimer', '300')
# r.set('lightPIN', '22')
# r.set('lightState', 'Off')
# r.set('lightTimer', '3600')
# r.set('pumpLastAction', time.time())
# r.set('lightsLastAction', time.time())

pumpPIN = int(r.get('pumpPIN'))
lightPIN = int(r.get('lightPIN'))
buttonPIN = int(r.get('buttonPIN'))

button = Button(buttonPIN)
prevState = 1
currState = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pumpPIN,GPIO.OUT)
GPIO.setup(lightPIN,GPIO.OUT)

GPIO.output(pumpPIN,1)
GPIO.output(lightPIN,1)

def updateLCD():
	draw.rectangle((0,0,oled.width,oled.height), outline=0, fill=0)
	pumpState = r.get('pumpState')
	if( int(pumpState) == 0 ):
		pumpStateString = "Off"
	elif( int(pumpState) == 1 ):
		pumpStateString = "On"
	pumpTimer = float(r.get('pumpTimer'))
	pumpLastAction = float(r.get('pumpLastAction'))
	lightState = r.get('lightState')
	if( int(lightState) == 0 ):
		lightStateString = "Off"
	elif( int(lightState) == 1 ):
		lightStateString = "On"
	lightTimer = float(r.get('lightTimer'))
	lightLastAction = float(r.get('lightLastAction'))
	#lcd.close(clear=True)
	#lcd.write_string(str(time.strftime("%I:%M %p %a %m/%d")))
	#lcd.crlf()
	pumpStateOutput = "P: " + pumpStateString + " " + str(time.strftime("%I:%M %p", time.localtime(pumpLastAction + pumpTimer)))
	#lcd.write_string(pumpStateOutput)
	#lcd.crlf()
	lightStateOutput = "L: " + lightStateString + " " + str(time.strftime("%I:%M %p", time.localtime(lightLastAction + lightTimer)))
	#lcd.write_string(lightStateOutput)
	#lcd.crlf()
	updateText1 = str(time.strftime("%I:%M:%S %p %a %m/%d"))
	draw.text((x, top), updateText1, font=font, fill=255)
	draw.text((x, top+16), pumpStateOutput, font=font, fill=255)
	draw.text((x, top+32), lightStateOutput, font=font, fill=255)
	draw.text((x, top+56), "IP: " + str(IP),  font=font, fill=255)
	oled.image(image)
	oled.show()
	s.enter(1, 1, updateLCD)

def updateDevices():
	pumpLastAction = float(r.get('pumpLastAction'))
	pumpTimer = int(r.get('pumpTimer'))
	pumpState = int(r.get('pumpState'))
	pumpOnTime = int(r.get('pumpOnTime'))
	pumpOffTime = int(r.get('pumpOffTime'))
	if( pumpLastAction + pumpTimer <= time.time() ):
		if( pumpState == 1):
			r.set('pumpState', 0)
			r.set('pumpTimer', pumpOffTime)
			r.set('pumpLastAction', time.time())
			GPIO.output(pumpPIN, 0)
		elif ( pumpState == 0 ):
			r.set('pumpState', 1)
			r.set('pumpTimer', pumpOnTime)
			r.set('pumpLastAction', time.time())
			GPIO.output(pumpPIN, 1)

	lightLastAction = float(r.get('lightLastAction'))
	lightTimer = int(r.get('lightTimer'))
	lightState = int(r.get('lightState'))
	lightOnTime = int(r.get('lightOnTime'))
	lightOffTime = int(r.get('lightOffTime'))
	if( lightLastAction + lightTimer <= time.time() ):
		if( lightState == 1):
			r.set('lightState', 0)
			r.set('lightTimer', lightOffTime)
			r.set('lightLastAction', time.time())
			GPIO.output(lightPIN, 0)
		elif ( lightState == 0 ):
			r.set('lightState', 1)
			r.set('lightTimer', lightOnTime)
			r.set('lightLastAction', time.time())
			GPIO.output(lightPIN, 1)
	s.enter(10, 1, updateDevices)

def buttonPress():
	if currState == 1:
		print("Button Pressed!")
	if currState == 0:
		print("Button Released!")

s.enter(10, 1, updateLCD)
s.enter(30, 1, updateDevices)

while(True):
	if button.is_pressed:
		if prevState != currState:
			currState = 1
			buttonPress()
			sleep(0.15)
		else:
			currState = 0
			buttonPress()
			sleep(0.15)
	s.run()

