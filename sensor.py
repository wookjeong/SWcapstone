import RPi.GPIO as gpio
import time
import motor

gpio.setmode(gpio.BOARD)
trig = 33
echo = 35
print "start"
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
col = 0

def sensor(collision):
	global col
	try :
		while True :
			gpio.output(trig, False)
			time.sleep(0.5)
			gpio.output(trig, True)
			time.sleep(0.00001)
			gpio.output(trig, False)
			while gpio.input(echo) == 0 :
				pulse_start = time.time()
			while gpio.input(echo) == 1 :
				pulse_end = time.time()
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17000
			distance = round(distance, 2)

			if distance < 25:
				collision.value = 1
				col = 1
				motor.ctrl(0)
			else:
				collision.value = 0
				col = 0

			print "Distance : ", distance, "cm | collision : ", collision.value
	#		print "col value : ", col
	except :
		gpio.cleanup()

