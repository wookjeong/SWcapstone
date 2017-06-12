#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import os
import time
import jeongwook
import multiprocessing
import threading
from socket import *
from time import ctime
import sensor
import sys

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'auto\n', 'home', 'x+', 'cameraleft', 'y+', 'y-']
#Set array of Command from Android CLient

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                         # connections are full, others will be rejected. 

video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home() #Set direction of iCar Center
video_dir.move_decrease_y()#Down Camera for Line Detection
video_dir.move_decrease_y()
video_dir.move_decrease_y()

def server(value,collision):#get value as Direction and collision as Collision detection from Shared memory 
	pre_dir = 'home'
	x=0
	flag = 0
	while True:
		sys.stdout.flush()
		print 'Waiting for connection...'
	# Waiting for connection. Once receiving a connection, the function accept() returns a separate 
	# client socket for the subsequent communication. By default, the function accept() is a blocking 
	# one, which means it is suspended before the connection comes.
		tcpCliSock, addr = tcpSerSock.accept() 
		print '...connected from :', addr     # Print the IP address of the client connected with the server.
		
		while True:
			data = ''
			data = tcpCliSock.recv(BUFSIZ)
			# Receive data sent from the client. 
                        # Analyze the command received and control the car accordingly.
			print data
			if not data:
				break
			if x == 1:
				if flag < 5:
					flag = flag + 1
					continue #if there is any collision, Do not receive data from client.If so, Get stacked!
			x=0 #after refusing data from client, start receiving 
			flag = 0
			if data == ctrl_cmd[0]:#If Client send message "forward"
				if collision.value==1:#if there is obstacle in front of iCar
					motor.ctrl(0)#stop
				else:
					motor.forward()#Run the motors to forward
			elif data == ctrl_cmd[1]:#If Client send message "backward"
				motor.backward()
				
			elif data == ctrl_cmd[2]:#If Client send message "left"
				car_dir.turn_left()#change car direction to Left
				
			elif data == ctrl_cmd[3]:#If Client send message "right"
				car_dir.turn_right()#change car direction to Right
				
			elif data == ctrl_cmd[6]:#If Client send message "home"
				car_dir.home()#Set car direction to center
				
			elif data == ctrl_cmd[4]:#if Client send message "stop"
				motor.ctrl(0)#Stop Motor running
				
			elif data == ctrl_cmd[5]:#If Client click auto button, send message "auto"
				#auto drive
				motor.setSpeed(44)#Set motor speed with  optimized speed 44  
				temp = value.value#get Value from jeongwook.py that is information of Car Direction

				if collision.value !=0:#If there is Collision 
					print 'Collision detected'
					if collision.value == 1 : #Collision in front of iCar
						print "Obstacle In Front"
						motor.collision_auto()#collision_auto function let iCar move backward
						car_dir.turn_right()#to avoid collision, turn right
						motor.forward_auto()#move only for 0.8second (forward_auto let iCar move for 0.2second)
						motor.forward_auto()
						motor.forward_auto()
						motor.forward_auto()
						car_dir.home()
						motor.forward_auto()
						motor.forward_auto()
						pre_dir = 'left'#if iCar cannot detect any lane, it SHOULD BE on left side, so makes iCar go left after avoiding 
					elif collision.value == 2 : #Collision on Left side
						print "Obstacle is on Left"
						motor.collision_auto()
						car_dir.turn_right()#to avoid collision, turn right
						motor.forward_auto()
						motor.forward_auto()
						motor.forward_auto()
						motor.forward_auto()
						car_dir.home()
						motor.forward_auto()
						motor.forward_auto()
						pre_dir = 'left'
					elif collision.value == 3 : #go left
						print "Obstacle is on Right"
						motor.collision_auto()
						car_dir.turn_left()#to avoid collision, turn left
						motor.forward_auto()
						motor.forward_auto()
						motor.forward_auto()
						motor.forward_auto()
						car_dir.home()			
						motor.forward_auto()
						motor.forward_auto()
						pre_dir = 'right'#if iCar cannot detect any lane, it SHOULD BE on right side, so makes iCar go right after avoiding 
					
					collision.value = 0
				
					x= 1 #set x = 1 to Not receiving data from client for a moment 
					
 
				elif temp == 1:#iCar is on Lane, Go with center direction
					print 'Lane is on my way'
					car_dir.home()
					motor.forward_auto()#move iCar for 0.2second with 44speed
					#because of camera delay
					
				elif temp == 2:#lane is located on left side
					print 'Lane is on left side'
					car_dir.turn_left()
					motor.forward_auto()
					pre_dir = 'left'

				elif temp == 3:#lane is located on right side
					print 'Lane is on right side'
					car_dir.turn_right()
					motor.setSpeed(44)
					motor.forward_auto()
					pre_dir = 'right'
				else :
					if pre_dir == 'right':#when No detection but predict that lane is on right side
						print 'cannot find but go right'
						car_dir.turn_right()
						motor.setSpeed(44)
						motor.forward_auto()
						
					elif pre_dir == 'left':#when No detection but predict that lane is on left side
						print 'cannot find but go left'
						car_dir.turn_left()
						motor.forward_auto()
					
					else:
						print 'Cannot find a Lane'#No detection with no prediction
						car_dir.home()#set center direction and stop 
						motor.backward()
						time.sleep(0.6)
						motor.ctrl(0)
						time.sleep(1)
				
					       
					
					
			elif data == ctrl_cmd[7]:#move camera right
				video_dir.move_increase_x()
			elif data == ctrl_cmd[8]:#move camera left
				video_dir.move_decrease_x()
			elif data == ctrl_cmd[9]:#move camera up
				video_dir.move_increase_y()
			elif data == ctrl_cmd[10]:#move camera down
				video_dir.move_decrease_y()
			
			elif data[0:5] == 'speed':     # Change the speed
				print data
				numLen = len(data) - len('speed')
				if numLen == 1 or numLen == 2 or numLen == 3:
					tmp = data[-numLen:]
					spd = int(tmp)
					if spd < 24:
						spd = 24
					motor.setSpeed(spd)
					
			elif data[0:7] == 'leftPWM':#If Client send message like ~PWM, it is for initialization or servo motor that control Car direction. 
				numLen = len(data) - len('leftPWM')
				pwm = data[-numLen:]
				leftpwm = int(pwm)
				
				car_dir.change_left(leftpwm)
			elif data[0:7] == 'homePWM':
				numLen = len(data) - len('homePWM')
				pwm = data[-numLen:]
				homepwm = int(pwm)
				
				car_dir.change_home(homepwm)
			elif data[0:8] == 'rightPWM':
				numLen = len(data) - len('rightPWM')
				pwm = data[-numLen:]
				rightpwm = int(pwm)
				car_dir.change_right(rightpwm)

			else:
				print 'Command Error! Cannot recognize command: ' + data

	tcpSerSock.close()

if __name__ == "__main__":
	procs=[]
	value = multiprocessing.Value('i',0)#share memory within multi processing that is about Car direction
	collision = multiprocessing.Value('i',0)#shared memory within multi processing that is about Collision
	procs.append(multiprocessing.Process(target=jeongwook.handle_video,args=(value,)))#Makes 3 multi processing
	procs.append(multiprocessing.Process(target=server, args=(value,collision,)))
	procs.append(multiprocessing.Process(target=sensor.sensor, args=(collision,)))

	for p in procs:
		p.start() 
