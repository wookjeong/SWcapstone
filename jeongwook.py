import cv2 # opencv
import numpy as np
import os

def average(values):# return Average value of Array 
        if len(values) == 0:
                return None
        return sum(values,0.0) / len(values) #Use for Getting average x-axis point from Camera

def circle_only(mark,x,y): #Show Circle Only on Frame with Green color and radius 5
	cv2.circle(mark, (x,y),5,(255,0,0),1,8,0)

def circle(mark, y):#Circle on Frame with returning Average Point of x-aix
	list = []
	for x in range (176):
		if mark[y][x][2] == 255 :#if a pixel of frame is red, Append to List
			list.append(x)
	if len(list) != 0:#if there is any Red Pixel(lane detection)
		average_point = int(average(list))#get average and 
		cv2.circle(mark, (average_point,y),5,(0,255,0),1,8,0)#circle on frame
	else:
		average_point = None#if nothing is detected, input None value 
	return average_point

def region_of_interest(img, vertices, color3=(255,255,255), color1=255):#Get only half size of Frame because the background is not 
	mask = np.zeros_like(img)                                                                            #          necessary
        #make same blank image with image (frame)
	cv2.fillPoly(mask, vertices, color3)#fill BLACK on unnecessary region 
	ROI_image = cv2.bitwise_and(img, mask)#Bitwise-AND mask and original image 
	return ROI_image#return ROI-ed image

def mark_img(img):#Function for getting interesting color(pixels)
	bgr_threshold = [200,200,200]#set Threshold with 200,200,200 = lite gray ~ pure white color
	thresholds = (img[:,:,0] < bgr_threshold[0]) \
                | (img[:,:,1] < bgr_threshold[1]) \
                | (img[:,:,2] < bgr_threshold[2])#Check all the pixels of image that is lower than threshold
	test = (img[:,:,0] > 200)|(img[:,:,1] > 200)|(img[:,:,2] > 200)#check all the pixels of image that is higher than threshold
	img[test] = [0,0,255]#if higher than threshold, makes RED pixel. (showing Line)
	img[thresholds] = [0,0,0]
	return img


def handle_video(value):
	os.system('sudo modprobe bcm2835-v4l2')
	cap = cv2.VideoCapture(0)#Getting Real-time Image from Camera
	cap.set(3,176)#Set size 176 x 144 image 
	cap.set(4,144)#Minimum size of video 
	n=0
	direction='home'
	
	while True :
		ret,frame = cap.read()#get real-time image 
		w = cap.get(3)#get Size width
		h = cap.get(4)#get Size height
		vertices = np.array([[(0,h),(0, h/2),(w, h/2), (w,h)]], dtype=np.int32)#Set the region We wants
		roi_img = region_of_interest(frame, vertices)#Get only region of interest from image, makes black the others
		
		mark = np.copy(roi_img)
		
		mark = mark_img(roi_img)#Line detection with RED pixels (if pixel is higher than threshold)
		color_thresholds = (mark[:,:,0]==0) & (mark[:,:,1] ==0) & (mark[:,:,2]>200)#make threshold 
		frame[color_thresholds]=[0,0,255]#Show Lane with RED color on Original Image too 
		if not ret : 
			print('Not Found Device')
			break

		if ret:#if there is Device 
			n=0
			cv2.line(mark,(47,72), (47,144),(0,255,0), 1)#Show the two lines that are boundary line which conclude the Direction of iCar should be
			cv2.line(mark,(129,72), (129,144), (0,255,0), 1) 
			
			point1 = circle(mark, 108)
			point2 = circle(mark, 120)
			point3 = circle(mark, 86)
			point4 = circle(mark, 98)
			point5 = circle(mark, 143)
			#show circles that we think Important
			avr_for = None
			if point3 != None:
				if point4 != None:
					avr_for = (point3+point4)/2 #Set avr_for a point from front side of image 
			avr_mid = None
			if point2 != None:
				if point5 != None:
					avr_mid = (point2+point5)/2 #Set avr_mid a point from middle side of image
				elif point5 == None:
					avr_mid = point2
			elif point2 == None:
				if point5 != None:
					avr_mid = point5
			
			
			if point1 != None:
				if point2 != None:
					cv2.line(mark,(point1,108),(point2,120),(0,255,0),1) #Makes line from avr_for and avr_mid
			if avr_mid!=None:
				circle_only(mark, avr_mid,130)
			if avr_for!=None:
				circle_only(mark,avr_for,92)
			if avr_mid!= None:
				if avr_for!=None:
					cv2.line(mark,(avr_mid, 130), (avr_for, 92),(255,0,0),1)
			if  48< avr_mid < 130:	
				if avr_for > 129:#if the Front average points is on right side, iCar should go right 
					value.value = 3 #value is shared memory from multiprocessing. Let server know that icar should go right
					direction = 'right'
				elif 1 < avr_for < 47:#if the Front average points is on left side, iCar should go left
					value.value = 2#Let server know that icar should go left
					direction = 'left'
				value.value = 1#if value is 1, iCar should go center
				direction = 'home'
			elif 1<avr_mid < 48:#Give Front average point first priority, and Middle average point is Second priority
				value.value = 2 #should turn left if Lane is on left side
				direction = 'left'
			elif 130 <avr_mid < 176: #should turn right if Lane is on right side
				value.value = 3
				direction = 'right'
			else: 
				
				value.value = 0#if nothing is detected
				
			#cv2.imshow('roi image', roi_img)
			cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
			cv2.resizeWindow('frame', 352,288)#makes frame size 352x288
			cv2.namedWindow('line_detection', cv2.WINDOW_NORMAL)
			cv2.resizeWindow('line_detection', 352,288))#makes frame size 352x288
			cv2.imshow('frame', frame)
			cv2.imshow('line_detection', mark)			
		if cv2.waitKey(1)&0xFF == 27 :
			break

	cap.release()
	cv2.destroyAllWindows()
#handle_video()


