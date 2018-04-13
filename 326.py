#!/usr/bin/python
import cv2
import numpy as np
import time
import os
import thread
import string
import math
from flask import Flask

#lower = np.array([40,0,0])
lower = (25,85,6)
upper = (64,255,255)
app = Flask("Petty")
automode = True
#upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
cam2 = cv2.VideoCapture(1)
iBest = -1.0
String = ""
#totAvgConfident=0;#last 10 round's average confident,used to recognize round
totAvgRadius=31;#last 3 round's average Radius,used to recognize round
R=[30,31,32]
rounds = []


import serial
class Ser(object):
    def __init__(self):
        #open port
        self.port = serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=2)

    #autosend
    def send_cmd(self, cmd):
        self.port.write(cmd)
        response = self.port.readall()
        response = self.convert_hex(response)
        return response

    #convert to hex
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result
#-------------HTTP response part
@app.route('/')
def hello_world():
	return 'server run success on port 80'
@app.route('/l')
def left():
	pass;
@app.route('/r')
def right():
	pass;
@app.route('/f')
def forward():
	pass;
@app.route('/d')
def down():
	pass;
@app.route('/up')
def upAuto():
	automode = True
@app.route('/down')
def downAuto():
	automode = False
#EOF---------------------
def start_http_handler():
	app.run(host='0.0.0.0',port=5000)

def start_service():
    res=os.system('''mjpg_streamer -i "input_uvc.so -d /dev/video2 -f 10 -y" -o "output_http.so -w www -p 8888"''')#dont forget to change video n

def ReadRawFile(filepath):
    file = open(filepath)
    try:
        tempa = file.read()
    finally:
        file.close()
        tempa = tempa.replace(" ","").replace("\n","")
    return tempa

def RadJudge(x,y,r,X,Y):
    if (x>X or y>Y):
        print "E:RadJudge Out-of-bound"
        os._exit();

    relativeX = (x-X/2)/X
    return relativeX

def getCircle(frame2):#returns a num[] contains [x,y,r]
    if True:
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

        HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
        #H,S,V = cv2.split(HSV)
        mask = cv2.inRange(HSV,lower,upper)
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=4)
	cv2.imshow("debug",mask)
        contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        maxPercentage = 0
        maxPercentageContour = None

        for contour in contours:
            ((x,y),radius) = cv2.minEnclosingCircle(contour)
            contourArea = cv2.contourArea(contour)
            M=cv2.moments(contour)
            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))

            if radius>10.0:
                rounds.append([x,y,radius,contourArea,int([M["m10"]/M["m00"]]),int(M["m01"]/M["m00"])])

        for (x1,y1,r1,s1,cx1,cy1) in rounds:
            for (x2,y2,r2,s2,cx2,cy2) in rounds:
                if (x1!=x2 and y1!=y2 and r1!=r2):
                    dist1 = x1*x1+y1*y1;
                    dist2 = x2*x2+y2*y2;
                    if (math.fabs(dist1-dist2)<=10 and math.fabs(r1-r2)<=10):
                        mergedX = (x1+x2)/2.0
                        mergedY = (y1+y2)/2.0
                        mergedR = (r1+r2)/2.0
                        mergedS = (s1+s2)
                        rounds.remove([x1,y1,r1,s1,cx1,cy1])
                        rounds.remove([x2,y2,r2,s2,cx2,cy2])
                        rounds.append([mergedX,mergedY,mergedR,mergedS])
                        print "one round merged."


        for contour in rounds:#TODO:1.for(x,y,r,contourArea,...)
                       #2:add moments for finding center.leave 142 behind.
            contourArea=contour[3];
            radius = contour[2];
            percentage = contourArea / (radius * radius * 3.1415926)
        	if percentage>maxPercentage and percentage>0.50:#requires DEBUG
        	    maxPercentageContour = contour
        	    maxPercentage = percentage

        if (maxPercentageContour!=None):
            x = maxPercentageContour[0]
            y = maxPercentageContour[1]
            radius = maxPercentageContour[2]
            center = (maxPercentageContour[4],contourArea[5])
            #M=cv2.moments(maxPercentageContour)
            #center = (int(M["m10"]/M["m00"]), int(M["m01"] / M["m00"]))
            #((x,y),radius) = cv2.minEnclosingCircle(contour)
            cv2.circle(frame2,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame2,center,5,(0,0,255),-1)
            datatorep = [int(x),int(y),int(radius)]
            return datatorep
        # if len(contours)>0:
        #     c = max(contours,key=cv2.contourArea
        #     ((x,y),radius) = cv2.minEnclosingCircle(c)
        #     M=cv2.moments(c)
        #     center = (int(M["m10"]/M["m00"]), int(M["m01"] / M["m00"]))
        #     if radius > 10: #confirm it is a ball
        #         datatorep = [int(x),int(y),int(radius)]
        #         cv2.circle(frame2,(int(x),int(y)),int(radius),(0,255,255),2)
        #         cv2.circle(frame2,center,5,(0,0,255),-1)
        #         return datatorep

def CircleDetect():#detect circle
    global lower,upper,LowerBlue,UpperBlue,iBest
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("debug",cv2.WINDOW_AUTOSIZE)
    count = 0
    while True:
        count = count + 1
        try:
            _,frame2 = cam2.read()
        except:
            print("E:get frame error.")
            #print(aa.message)
            os._exit()

        diff=getCircle(frame2)
        cv2.imshow("splitter",frame2)
        cv2.waitKey(1)
        print diff #show the data containing [x,y,r]
    cv2.destroyAllWindows();

def mood:
    #TODO 233

#--------------------------------------------------------------
print "step 1 of 5:start flask service"
thread.start_new_thread(start_http_handler,())
print "step 2 of 5:start direct play service"
thread.start_new_thread(start_service,())
print "step 3 of 5:start dog mood detection service"

print "step 5 of 5:start tennis detect service"
CircleDetect()

#-------------------------------

