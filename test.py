import RPi.GPIO as GPIO
import time
import redis
import sched
import random

random.seed(time.time())

s = sched.scheduler(time.time, time.sleep)

r = redis.Redis(host='localhost', port=6379, db=0)

ledR = 16
ledG = 13
ledB = 12

pump = 6
lights = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledR,GPIO.OUT)
GPIO.setup(ledG,GPIO.OUT)
GPIO.setup(ledB,GPIO.OUT)

GPIO.output(ledR,GPIO.HIGH)
r.set(ledR, 'GPIO.HIGH')
GPIO.output(ledG,GPIO.HIGH)
r.set(ledG, 'GPIO.HIGH')
GPIO.output(ledB,GPIO.HIGH)
r.set(ledB, 'GPIO.HIGH')

def reSchedule(ledName):
	s.enter(random.randint(2, 5), 1, toggleLED, (ledName, ))

def toggleLED(ledName):
	state = str(r.get(ledName)).strip("b'")
	print(ledName)
	print(state)
	if(state == 'GPIO.HIGH'):
		GPIO.output(ledName,GPIO.LOW)
		r.set(ledName, 'GPIO.LOW')
	elif(state == 'GPIO.LOW'):
		GPIO.output(ledName,GPIO.HIGH)
		r.set(ledName, 'GPIO.HIGH')
	reSchedule(ledName)

s.enter(random.randint(2, 5), 1, toggleLED, (ledR, ))
s.enter(random.randint(2, 5), 1, toggleLED, (ledG, ))
s.enter(random.randint(2, 5), 1, toggleLED, (ledB, ))

while(True):
	s.run()

#while(True):
#	print("toggle red")
#	toggleLED(ledR)
#	time.sleep(1)
#	print("toggle green")
#	toggleLED(ledG)
#	time.sleep(1)
#	print("toggle blue")
#	toggleLED(ledB)
#	time.sleep(1)

