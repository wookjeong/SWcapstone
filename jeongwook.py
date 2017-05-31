import cv2 # opencv
import numpy as np
import os

def average(values):
        if len(values) == 0:
                return None
        return sum(values,0.0) / len(values)


def circle(mark, y):
	list = []
	for x in range (0,320):
		if mark[y][x][2] == 255 :
			list.append(x)
	if len(list) != 0:
		average_point = int(average(list))
		cv2.circle(mark, (average_point,y),5,(0,255,0),1,8,0)
	else:
		average_point = None
	return average_point

def region_of_interest(img, vertices, color3=(255,255,255), color1=255):
	mask = np.zeros_like(img) 
	cv2.fillPoly(mask, vertices, color3)
	ROI_image = cv2.bitwise_and(img, mask)
	return ROI_image

def mark_img(img):
	bgr_threshold = [200,200,200]
	thresholds = (img[:,:,0] < bgr_threshold[0]) \
                | (img[:,:,1] < bgr_threshold[1]) \
                | (img[:,:,2] < bgr_threshold[2])
	test = (img[:,:,0] > 200)|(img[:,:,1] > 200)|(img[:,:,2] > 200)
	img[test] = [0,0,255]
	img[thresholds] = [0,0,0]
	return img


def handle_video(value):
	os.system('sudo modprobe bcm2835-v4l2')
	cap = cv2.VideoCapture(0)
	cap.set(3,360)
	cap.set(4,240)
	n=0
	while True :
		ret,frame = cap.read()
		w = cap.get(3)
		h = cap.get(4)		
		vertices = np.array([[(0,h),(0, h/2),(w+60, h/2), (w,h)]], dtype=np.int32)
		roi_img = region_of_interest(frame, vertices)
		
		mark = np.copy(roi_img)
		
		mark = mark_img(roi_img)
		color_thresholds = (mark[:,:,0]==0) & (mark[:,:,1] ==0) & (mark[:,:,2]>200)
		frame[color_thresholds]=[0,0,255]
		if not ret : 
			print('Not Found Device')
			break

		if ret:
			n=0
			cv2.line(mark,(130,200), (130,180),(0,255,0), 1)
			cv2.line(mark,(190,200), (190,180), (0,255,0), 1)
			
			point1 = circle(mark, 180)
			point2 = circle(mark, 200)
			#point3 = circle(mark,140)
			#point4 = circle(mark,120)
			#point5 = circle(mark, 220)
			if point1 != None:
				if point2 != None:
					cv2.line(mark,(point1,180),(point2,200),(0,255,0),1)
			
			if  130< point1 < 190:	
				value.value = 1
			elif 1<point1 < 130:
				value.value = 2 #should turn left
			elif 190 <point1 < 319:
				value.value = 3
			else: 
				value.value = 0
				
			#cv2.imshow('roi image', roi_img)
			cv2.imshow('frame', frame)
			cv2.imshow('line_detection', mark)			
		if cv2.waitKey(1)&0xFF == 27 :
			break

	cap.release()
	cv2.destroyAllWindows()
#handle_video()


