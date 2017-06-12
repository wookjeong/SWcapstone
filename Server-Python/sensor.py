import RPi.GPIO as gpio
import time
import motor
#========================================================================
#raspberry pi board number33,35,38,40 for ultrasonic sensor input,output
#========================================================================
gpio.setmode(gpio.BOARD)
trig = 38#PIN NUMBER of Sensor 1 
echo = 40
print "start sensor1,2"
trig2=33#PIN NUMBER of Sensor 2 
echo2=35

#========================================================================
#Using two ultrasonics, detect obstacle to avoid collision
#Parameter(collision) means location of obstacle 
#========================================================================

def sensor(collision):
	try :
		while True :
			gpio.setup(trig, gpio.OUT)
			gpio.setup(echo, gpio.IN)
			gpio.output(trig, False)
			time.sleep(0.5)
			gpio.output(trig, True)
			time.sleep(0.00001)
			gpio.output(trig, False)
			while gpio.input(echo) == 0 :
				pulse_start = time.time()
			while gpio.input(echo) == 1 :
				pulse_end = time.time()
			
			#calculate distance between car and obstacle
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17000
			distance = round(distance, 2)
			if 0<distance < 18:
				col = 1
				
			else:
				col = 0
			if col == 1:
				print "Sensor1 Distance : ", distance, "cm"

			gpio.setup(trig2, gpio.OUT)
			gpio.setup(echo2, gpio.IN)
            gpio.output(trig2, False)
            time.sleep(0.5)
			gpio.output(trig2, True)
            time.sleep(0.00001)
                       
			gpio.output(trig2, False)

            while gpio.input(echo2) == 0 :
                pulse_start2 = time.time()

			while gpio.input(echo2) == 1 :
                pulse_end2 = time.time()
                        
            pulse_duration2 = pulse_end2 - pulse_start2
            distance2 = pulse_duration2 * 17000
            distance2 = round(distance2, 2)

            if 0 < distance2 < 18:
                col2 = 1
                    
            else:
                col2 = 0
            if col2 == 1:
                print "Sensor2 Distance : ", distance2, "cm"
			

			if col == 1:
				if col2 == 1:
					collision.value = 1 #The obstacle is on the front
					motor.ctrl(0)
				elif col2 == 0:
					collision.value = 2 #The obstacle is on the left
			elif col == 0: 
				if col2 == 1:
					collision.value = 3 #The obstacle is on the right
				elif col2 == 0:
					collision.value = 0 #There is no obstacle
					

	except :
		gpio.cleanup()
