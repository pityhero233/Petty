#!/usr/bin/python
import cv2
import numpy as np
import time
import os
import thread
import string
from flask import Flask

#lower = np.array([40,0,0])
lower = (25,85,6)
upper = (64,255,255)
app = Flask("Petty")
automode = True
#upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
iBest = -1.0
lastString = ""
#totAvgConfident=0;#last 10 round's average confident,used to recognize round
totAvgRadius=31;#last 3 round's average Radius,used to recognize round
R=[30,31,32]

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
	app.run()

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

def getDiff(frame2):#returns a num[] contains [x,y,r]
    if True:
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

        HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
        #H,S,V = cv2.split(HSV)
        mask = cv2.inRange(HSV,lower,upper)
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=2)
        contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(contours)>0:
            c = max(contours.key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M=cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10: #confirm it is a ball
                datatorep = [int(x),int(y),int(radius)]
                cv2.circle(frame2,(int(x),int(y)),int(radius),(0,255,255),2)
                cv2.circle(frame2,center,5,(0,0,255),-1)
                return datatorep

def CircleDetect():#detect circle
    global lower,upper,LowerBlue,UpperBlue,iBest
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
    count = 0
    while True:
        count = count + 1
        try:
            _,frame2 = cam2.read()
        except aa:
            print("E:get frame error.")
            print(aa.message)
            os._exit()

        diff=getDiff(frame2)
        cv2.imshow("splitter",frame2)
        cv2.waitKey(10)
        print diff #show the data containing [x,y,r]

    cv2.destroyAllWindows();

#--------------------------------------------------------------
print "step 1 of 4:start flask service"
thread.start_new_thread(start_http_handler,())
print "step 2 of 4:start direct play service"
thread.start_new_thread(start_service,())
print "step 3 of 4:start tennis detect service"
CircleDetect()
print "step 4:circle detect"

#-------------------------------

