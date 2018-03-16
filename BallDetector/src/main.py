import cv2
import numpy as np
#import os.system as sys

import os
#lower = np.array([40,0,0])
#upper = np.array([85,255,255])
lower = (25,86,6)
upper = (64,255,255)
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
iBest = -1.0
try:
    cam2 = cv2.VideoCapture(1)
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
except aa:
    print(aa.message)
    os._exit()
#es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

while True:
	print "fine."
	_,frame2 = cam2.read()
	HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
	#HSV = cv2.GaussianBlur(HSV, (5, 5), 0)
	H,S,V = cv2.split(HSV)
	mask = cv2.inRange(HSV,lower,upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	certain = cv2.bitwise_and(frame2,frame2,mask=mask)
	#cv2.imshow("splitter",np.stack([frame,frame2,certain]))
	diff = cv2.GaussianBlur(certain,(5,5),0)
	diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
	diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
	diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)
	cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts)>0:
    	c = max(cnts,key=cv2.contourArea)
    	((x,y),radius) = cv2.minEnclosingCircle(c)
    	M=cv2.moments(c)
    	center = (int(M["m10"]/M["m00"]), int(M["m01"] / M["m00"]))
    	if radius > 10:
        	cv2.circle(frame2,(int(x),int(y)),int(radius),(0,255,255),2)
        	cv2.circle(frame2,center,5,(0,0,255),-1)


	gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
	print(frame2.shape)

	cv2.imshow("splitter",np.hstack([frame2,certain]))
cv2.waitKey(0)
cv2.destroyAllWindows()

