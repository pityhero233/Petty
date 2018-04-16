#!/usr/bin/python
import numpy as np
import time
import os
import thread
import string
import math
import serial
import pickle
import random
from flask import Flask
import cv2
from enum import Enum


#lower = np.array([40,0,0])
lower = (25,85,6)
upper = (64,255,255)
app = Flask("Petty")
#upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
cam2 = cv2.VideoCapture(1)#system cam
iBest = -1.0
String = ""
R=[30,31,32]

normalSpeed = 111#100 to 999
minShootTime = 1200;#20 minutes = 1200 secs
pickupThreshold = 20#FIXME
pickAngleThreshold = 50#FIXME
screenx = 640#camera resolution
screeny = 320

shootTryout = 0;
lastShootTime = 0;
ballHistory=[]

Command = {
                 # 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT
    "STOP" : 0,
    "FORWARD" : 1,
    "BACK" : 2,
    "LEFT" : 3,
    "RIGHT" : 4,
    "TURNLEFT" : 5,
    "TURNRIGHT" : 6,
    "SHOOT" : 7,
    "PICK" : 8
};
systemState = {
    "empty" : 0,
    "loading" : 1,
    "handmode" : 2,
    "automode_normal" : 3,
    "automode_retrieve" : 4,#finding the ball,
    "automode_retrieve_go" : 5,
    "automode_shooting" : 6
};
userPreference = {
    "PlayDog" : 0,
    "RandomShoot" : 1,
    "TimelyShoot" : 2
}
state = systemState("empty")
strategy = userPreference["PlayDog"]#TODO
#-------------HTTP response part
@app.route('/')
def hello_world():
	return 'server run success on port 80'
@app.route('/l')
def left():
	if state==systemState("handmode"):
        callUno(Command("LEFT"))
@app.route('/r')
def right():
	if state==systemState("handmode"):
        callUno(Command("RIGHT"))
@app.route('/f')
def forward():
	if state==systemState("handmode"):
        callUno(Command("FORWARD"))
@app.route('/d')
def down():
	if state==systemState("handmode"):
        callUno(Command("BACK"))
@app.route('/up')
def upAuto():
	state=systemState("automode_normal")

@app.route('/down')
def downAuto():
	state=systemState("handmode")
@app.route('/shoot')
def shoot():
	if state==systemState("handmode"):
        callUno(Command("SHOOT"))

@app.route('/pick')
def pick():
	if state==systemState("handmode"):
        callUno(Command("PICK"))

@app.route('/prefer_playdog')
def chg_prf_pd():
    strategy = userPreference["PlayDog"]
@app.route('/prefer_random')
def chg_prf_rd():
    strategy = userPreference["RandomShoot"]
@app.route('/prefer_timelyshoot')

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

def callUno(action,parameter=-1):
    if (parameter==-1):
        arduino.write(str(action.value)+" "+str(normalSpeed))
    else:
        if parameter>0 and parameter<=999:
            arduino.write(str(action.value)+" "+str(parameter))
        else:
            print("E:callUno parameter fail")

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def RadJudge(ballx,bally,screenx,screeny):
    return (ballx-screenx/2)

def isDangerous(frame1,frame2,px,py):#detect if point(px,py) is in "the moving area of frame"(dog)
    gray1 = cv2.cvtColor(frame1,cv2.CV_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2,cv2.CV_BGR2GRAY)
    diff = cv2.absdiff(gray1,gray2)
    thr = cv2.threshold(diff,50,255,cv2.THRESH_BINARY)
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
    thr = cv2.erode(thr,erode_kernel)
    thr = cv2.dilate(thr,dilate_kernel)
    contours = cv2.findContours(thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for tot in contours:
        ((x1,y1),(x2,y2)) = cv2.boundingRect(tot)
        if (x1<=px and px<=x2 and y1<=py and py<=y2):
            return True
    return False

def isFineToShoot():#judge
    dt = math.fabs(time.time()-lastShootTime)
    #1.judge freq
    if (dt>=minShootTime):#if 
        pass
    else:
        return False;
    #2.judge night
    if (time.localtime(time.time()).tm_hour>6 and time.localtime(time.time()).tm_hour<21):
        return True
    else:
        return False;
    
def mood():#TODO:return dog mood based on recently acceleration count,1to100,integer/float
    pass

def takePhoto():
    try:
        _,frame = cam2.read()
        return frame
    except:
        print "take fail.frome takePhoto()"
        return -1
    import cv2
import math
lower = (25,85,6)
upper = (64,255,255)
rounds = []
def getCircle(frame2):#returns a num[] contains [x,y,r]
    if True:
        HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
        #H,S,V = cv2.split(HSV)
        mask = cv2.inRange(HSV,lower,upper)
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=4)
	    #cv2.imshow("debug",mask)
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
        else:
            return -1
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



def TennisDetect(frame2):#capture a picture and perform a tennis detect 
    global lower,upper,LowerBlue,UpperBlue,iBest
    #cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
    #cv2.namedWindow("debug",cv2.WINDOW_AUTOSIZE)

    diff=getCircle(frame2)
    #cv2.imshow("splitter",frame2)
    #cv2.waitKey(1)
    print diff #show the data containing [x,y,r]
    #cv2.destroyAllWindows();
    if diff!=-1:
        return diff
    else:
        return [0,0,0]
#--------------------------------------------------------------
state = systemState("loading")
print "step 0 of 5:perform arduino detection"
port_list = list(serial.tools.list_ports.comports())  
if len(port_list)<=0:
    print("E:arduino base not found.")
else:
    pl1 =list(port_list[0]) 
    port_using = pl1[0]
    arduino = serial.Serial(port_using,57600,timeout = 60) 
    print("using ",arduino.name)
    print("testing connection...")
    callUno(Command("FORWARD"))
    time.sleep(0.5)
    callUno(Command("STOP"))
    time.sleep(0.5)
    callUno(Command("SHOOT"))
    time.sleep(0.5)
    callUno(Command("STOP"))
    print("connection test complete.")
print "step 1 of 5:read user preferences"
with open("UserPreferences.pk","r") as usf:
    strategy = pickle.load(usf)
    print("strategy=",strategy)
print "step 2 of 5:start user respond service"
thread.start_new_thread(start_http_handler,())
print "step 3 of 5:start direct play service"
thread.start_new_thread(start_service,())
print "step 4 of 5:start dog mood processing service"

print "step 5 of 5:start tennis detect service"
if (state==systemState("loading")):
    print "automode started."
    state=systemState("automode_normal")
elif (state==systemState("automode_normal")):
    dogmood = mood()
    if dogmood>50:
        state=systemState("automode_shooting")
        p1 = takePhoto();time.sleep(1); p2 = takePhoto();
        if not isDangerous(p1,p2,320,240) and isFineToShoot(): #HACK
            callUno(Command("SHOOT"))
            shootTryout = 0;
            time.sleep(random.randint(5,20))
            state=systemState("automode_retrieve")
        else:
            callUno(Command("RIGHT"))
            time.sleep(0.5)
            callUno(Command("STOP"))
            shootTryout = shootTryout+1
            if shootTryout>10:
                shootTryout = 0;
                print("dog not good,shoot another time.")
                lastShootTime = time.time()
elif (state==systemState("automode_retrieve")):
    pic = takePhoto();
    if pic!=-1:#take success
        ans = TennisDetect(pic)
        if ans!=[0,0,0]:#ball found
            ballHistory.append(ans)
            if len(ballHistory)>10:#clear data,
                for i in range(0,5):
                    ballHistory.pop(i)
            _sx=0;_sy=0;_numbercnt=0#calc if the ball has been stopped
            for (x,y,r) in ballHistory:
                _sx=_sx+x
                _sy=_sy+y
                _numbercnt=_numbercnt+1
            avgx = _sx/_numbercnt
            avgy = _sy/_numbercnt
            if dist(ans[0],ans[1],avgx,avgy)<=pickupThreshold:#ball stopped
                if math.fabs(RadJudge(ans[0],ans[1],screenx,screeny))<=pickAngleThreshold:#angle right
                        state=systemState("automode_retrieve_go")
                else:
                    if math.fabs(RadJudge(ans[0],ans[1],screenx,screeny))>0:
                        callUno(Command("TURNRIGHT"),100)
                        time.sleep(0.3)
                        callUno(Command("STOP"))
                    else:
                        callUno(Command("TURNLEFT"),100)
                        time.sleep(0.3)
                        callUno(Command("STOP"))
        else:#ball not found
            if len(ballHistory)>0:#trying to track ball based on last appear position
                lastID = len(ballHistory)-1
                if math.fabs(RadJudge(ballHistory[lastID][0],ballHistory[lastID][1],screenx,screeny))<=pickAngleThreshold:#angle right
                    state=systemState("automode_retrieve_go")
                else:
                    if math.fabs(RadJudge(ballHistory[lastID][0],ballHistory[lastID][1],screenx,screeny))>0:
                        callUno(Command("TURNRIGHT"),100)
                        time.sleep(0.3)
                        callUno(Command("STOP"))
                    else:
                        callUno(Command("TURNLEFT"),100)
                        time.sleep(0.3)
                        callUno(Command("STOP"))
            
elif (state==systemState("automode_retrieve_go")):
    pic = takePhoto()
    if pic!=-1:
        loc = TennisDetect(pic)
        if loc!=[0,0,0]:#FIXME
            pass#SHOULD BE JUDGE WHEN TO PICK THE BALL AND EVENTUALLY PICK IT 
            state=systemState("automode_normal")
        else:
            state=systemState("automode_retrieve")

#-------------------------------
