#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import time
import os
import thread
import string
import math
import serial
import serial.tools.list_ports
import pickle
import random
from flask import Flask
import cv2
from enum import Enum


#lower = np.array([40,0,0])
NULL = 424242#MAGIC NUM
lower = (25,85,6)
upper = (64,255,255)
app = Flask("Petty")
#upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
#cam2 = cv2.VideoCapture(1)#system cam
iBest = -1.0
String = ""
R=[30,31,32]
lower = (25,85,6)
upper = (64,255,255)
rounds = []
normalSpeed = 111#100 to 999
minShootTime = 1200;#20 minutes = 1200 secs
pickupThreshold = 20#FIXME
pickAngleThreshold = 200#FIXME
screenx = 640#camera resolution
screeny = 320

systemDevice = "/dev/video2"
directPlayDevice = "/dev/video1"

arduinoLoc = "/dev/ttyACM0"#volatile
blunoLoc = "/dev/ttyACM1"#volatile

lastReceiveBluno = time.time()

shootTryout = 0
lastShootTime = 0
ballHistory=[]
todayMomentum=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#1-24h
uMomentum=0.0
hMomentum=0.0
hLastEntry=-1#last time update todayMomentum
print "step 0 of 6:perform arduino detection"
arduino = serial.Serial(arduinoLoc,57600,timeout=1.5,rtscts=True,dsrdtr=True)#FIX
print("using ",arduino.name," for arduino")
bluno = serial.Serial(blunoLoc,115200,timeout=1.5)
print("using",bluno.name," for bluno")

def scanUno():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list)<=0:
        print("E:arduino base not found.")
        return NULL
    else:
        pl1 =list(port_list[0])
        port_using = pl1[0]
        arduino = serial.Serial(port_using,57600,timeout = 1.5)
        print("using ",arduino.name)
        print("current arduino=",arduino)
        return arduino

def takePhotoFromVideoCapture(cam2):#Deprecated,for it delays badly TESTED ,using multi thread pool instead
    try:
        _,frame = cam2.read()
        return frame
    except:
        print "take fail.frome takePhoto()"
        return -1

def takePhoto():#take a photo using outside func
    try:
        os.system("fswebcam -d "+systemDevice+" -r 640x480 --no-banner tot.jpg")
        pic = cv2.imread("tot.jpg")
        return pic
    except:
        print "takePhoto Error"

currentPhoto=takePhoto()#test if the cam is success

class Command(Enum):
                 # 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT
    STOP = 0
    FORWARD = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4
    TURNLEFT = 5
    TURNRIGHT = 6
    SHOOT = 8
    PICK = 7
    RING = 9

class systemState(Enum):
    empty = 0
    loading = 1
    handmode = 2
    automode_normal = 3
    automode_retrieve = 4#finding the ball
    automode_retrieve_go = 5
    automode_shooting = 6

class userPreference(Enum):
    PlayDog = 0
    RandomShoot = 1
    TimelyShoot = 2

state = systemState.empty
strategy = userPreference.PlayDog#TODO
#-------------HTTP response part
@app.route('/')
def hello_world():
	return 'server run success on port 80'
@app.route('/stop')
def haltit():
    callUno(Command.STOP)
    return 'stopped'
@app.route('/l')
def left():
    print "from flask:begin write left"
    if state==systemState.handmode:
        callUno(Command.LEFT)
    print "from flask:end writing left"
    return 'left done'
@app.route('/r')
def right():
    print "from flask:begin write right"
    if state==systemState.handmode:
        callUno(Command.RIGHT)
    print "from flask:begin write right"
    return 'right done'
@app.route('/f')
def forward():
    print "from flask:begin write forward"
    if state==systemState.handmode:
        callUno(Command.FORWARD)
    print "from flask:begin write forward"
    return 'forward done'
@app.route('/d')
def down():
    print "from flask:begin write down"
    if state==systemState.handmode:
        callUno(Command.BACK)
    print "from flask:begin write down"
    return 'back done'
@app.route('/turnleft')
def turnleft():
    print "from flask:begin write turnleft"
    if state==systemState.handmode:
        callUno(Command.TURNLEFT,150)
    print "from flask:end write turnleft"
    return 'left done'
@app.route('/turnright')
def turnright():
    print "from flask:begin write turnright"
    if state==systemState.handmode:
        callUno(Command.TURNRIGHT,150)
    print "from flask:begin write turnright"
    return 'right done'
@app.route('/up')
def upAuto():
    global state
    state=systemState.automode_normal
    print('now state=',state)
    return 'auto up'
@app.route('/down')
def downAuto():
    global state
    state=systemState.handmode
    print('now state=',state)
    return 'auto down'
@app.route('/shoot')
def shoot():
    if state==systemState.handmode:
        callUno(Command.SHOOT)
    return 'shoot done'
@app.route('/pick')
def pick():
    if state==systemState.handmode:
        callUno(Command.PICK)
    return 'pick done'
@app.route('/prefer_playdog')
def chg_prf_pd():
    strategy = userPreference.PlayDog
    with open("UserPreferences.pk","wb") as filea:
        pickle.dump(strategy,filea)
@app.route('/prefer_random')
def chg_prf_rd():
    strategy = userPreference.RandomShoot
    with open("UserPreferences.pk","wb") as filea:
        pickle.dump(strategy,filea)
#@app.route('/prefer_timelyshoot') TODO
@app.route('/statistics')
def debug_print():
    dst = '''{'''

    tot = 0;
    while (tot<=23):
        dst.join(todayMomentum[tot])
        if tot!=23:
            dst.join(",")
    dst.join('''}''')
    print dst

@app.route('/statisticsB')
def debug_printB():#MAGIC
    print '''{8, 10, 12, 13, 15, 13, 31, 35, 45, 46, 42, 52, 71, 67, 70, 41, 35, \
36, 27, 25, 25, 31, 10, 8}'''

#EOF---------------------

def start_http_handler():
	app.run(host='0.0.0.0',port=5000)

def start_service():
    res=os.system('''mjpg_streamer -i "input_uvc.so -d '''+directPlayDevice+''' -f 10 -y" -o "output_http.so -w www -p 8888"''')#dont forget to change video n

def ReadRawFile(filepath):
    file = open(filepath)
    try:
        tempa = file.read()
    finally:
        file.close()
        tempa = tempa.replace(" ","").replace("\n","")
    return tempa

def callUnoBase(action,parameter=-1):
    if not arduino.writable():
        print("E:arduino not writable")
    if (parameter==-1):
        if action==Command.STOP:
            arduino.write('i')
            time.sleep(0.5)
            print('writed 1 000')
        else:
            arduino.write(str(action)+" "+str(normalSpeed))
            time.sleep(0.5)
            print('writed ',str(action)+" "+str(normalSpeed))
    else:
        if action==Command.STOP:
            arduino.write('i')
            time.sleep(0.5)
            print('writed 1 000')
        else:
            if parameter>0 and parameter<=999:
                arduino.write('i')
                time.sleep(0.5)
                print('writed ',str(action)+" "+str(normalSpeed))
            else:
                print("E:callUno parameter fail")

def callUno(action,parameter=-1):
    callUnoBase(action,parameter)


def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def photoPool(cam):#grab&throw excessive frames and refresh pool every 0.5 secs
    bt = time.time()
    while True:
        _,frame = cam.grab()
        if (time.time()-bt)>0.5:
            _,currentPhoto = cam.read()
            bt = time.time()

def RadJudge(ballx,bally,screenx,screeny):
    return (ballx-screenx/2)

def isDangerous(frame1,frame2,px,py):#detect if point(px,py) is in "the moving area of frame"(dog) PASSED
    gray1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)#FIXED 1
    gray2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)#FIXED 2
    diff = cv2.absdiff(gray1,gray2)
    _,thr = cv2.threshold(diff,15,255,cv2.THRESH_BINARY)#FIXED 3&4
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
    thr = cv2.erode(thr,erode_kernel)
    thr = cv2.dilate(thr,dilate_kernel)
    contours,_ = cv2.findContours(thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for tot in contours:
        ((x,y),radius) = cv2.minEnclosingCircle(tot)
        if dist(x,y,px,py)<=radius:
            return True
    return False

def isFineToShoot():#judge
    dt = math.fabs(time.time()-lastShootTime)
    #1.judge freq
    if (dt>=minShootTime):#if
        pass
    else:
        return False
    #2.judge night
    if (time.localtime(time.time()).tm_hour>6 and time.localtime(time.time()).tm_hour<21):
        return True
    else:
        return False;

def mood():#TODO:return dog mood based on recently acceleration count,1to100,integer/float
    global uMomentum,hMomentum,hLastEntry,lastReceiveBluno
    while True:
        raw=bluno.read_until('\r\n')

        while raw!='':
            lastReceiveBluno = time.time()
            x,y,z = raw.split(",")
            #print("x=",x,",y=",y,",z=",z)
            if x!='' and y!='' and z!='':
                uMomentum=math.fabs(int(x))+math.fabs(int(y))+math.fabs(int(z)) #update current
                hMomentum=hMomentum+uMomentum/3600.0 #add a small bonus
                if time.localtime(time.time()).tm_hour!=hLastEntry:#if a new hour occours
                    hLastEntry=time.localtime(time.time()).tm_hour
                    todayMomentum[hLastEntry-1]=hMomentum
                    hMomentum=0.0#clear the temp momentum
                raw=''

def dogAlarm():
    while True:
        if math.fabs(time.time()-lastReceiveBluno)>=5:
            #callUno(Command.RING)
            print "狗狗不见了！"
            time.sleep(2)
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
        for contour in contours:#TODO:1.for(x,y,r,contourArea,...)
            ((x,y),radius) = cv2.minEnclosingCircle(contour)
            contourArea = cv2.contourArea(contour)
            M=cv2.moments(contour)
            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
            percentage = contourArea / (radius * radius * 3.1415926)
            if percentage>maxPercentage and percentage>0.50 and radius>10.0 and radius<100.0:#requires DEBUG
                maxPercentageContour = contour
                maxPercentage = percentage
        if maxPercentageContour==None:
            #print "hahahahaha,zhao bu dao"
            pass
            return -1
        else:
            ((x,y),radius) = cv2.minEnclosingCircle(contour)
            M=cv2.moments(maxPercentageContour)
            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
            (x,y) = center
            return [x,y,radius]



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
state = systemState.loading
# if True: IGNORED HACK
#     print("testing connection...")
#     callUno(Command.FORWARD)
#     time.sleep(3)
#     callUno(Command.STOP)
#     time.sleep(3)
#     callUno(Command.SHOOT)
#     time.sleep(3)
#     callUno(Command.STOP)
#     print("connection test complete.")
print "step 1 of 6:read user preferences"
with open("UserPreferences.pk","rb") as usf:
    strategy = pickle.load(usf)
    print("strategy=",strategy)
print "step 2 of 6:start user respond service"
thread.start_new_thread(start_http_handler,())
print "step 3 of 6:start direct play service"
thread.start_new_thread(start_service,())
print "PASSED step 4 of 6:start photoPool service"
# thread.start_new_thread(photoPool,(cam2,))#FIXED
# using outer func instead
print "step 5 of 6:start dog mood processing service"
_ = bluno.read_all()#flush the pool
thread.start_new_thread(mood,())
thread.start_new_thread(dogAlarm,())
print "step 6 of 6:start autoretrieve service"

while True:
    #print "R:state=<SystemState>",state
    if math.fabs(uMomentum*2.0)<=0.5:
        print "--"
    else:
        print "心情"+str(uMomentum*2.0)

    if (state==systemState.loading):
        print "handmode started."
        state=systemState.handmode
    elif (state==systemState.automode_normal or state==systemState.automode_shooting):#fixed
        dogmood = uMomentum*2.0
        print "uDogmood=",dogmood
        if dogmood>50:
            state=systemState.automode_shooting
            p1 = takePhoto();time.sleep(1); p2 = takePhoto();
            if not isDangerous(p1,p2,320,240) and isFineToShoot(): #HACK
                callUno(Command.SHOOT)
                print "right to shoot:shoot performed."
                shootTryout = 0;
                time.sleep(random.randint(5,20))
                state=systemState.automode_retrieve
            else:
                print "isDangerous=",isDangerous(p1,p2,320,240)
                print "going right"
                callUno(Command.TURNRIGHT,300)
                time.sleep(4)
                print "stop"
                #time.sleep(5)
                #print "stop completed"
                shootTryout = shootTryout+1
                print "shootTryout=",shootTryout
                if shootTryout>10:
                    shootTryout = 0;
                    state = systemState.automode_normal
                    print("dog not good,shoot another time.")
                    lastShootTime = time.time()
    elif (state==systemState.automode_retrieve):
        pic = takePhoto();
        if 1!=-1:#take success HACK FIXME
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
                print "BALLavgx = ",avgx,"BALLavgy = ",avgy
                print "pickAngle=",math.fabs(RadJudge(ans[0],ans[1],screenx,screeny))
                if dist(ans[0],ans[1],avgx,avgy)<=pickupThreshold:#ball stopped
                    if math.fabs(RadJudge(ans[0],ans[1],screenx,screeny))<=pickAngleThreshold:#angle right
                            state=systemState.automode_retrieve_go
                    else:
                        if math.fabs(RadJudge(ans[0],ans[1],screenx,screeny))>0:
                            callUno(Command.TURNRIGHT,100)
                            time.sleep(1)
                        else:
                            callUno(Command.TURNLEFT,100)
                            time.sleep(1)
            else:#ball not found
                if len(ballHistory)>0:#trying to track ball based on last appear position
                    lastID = len(ballHistory)-1
                    if math.fabs(RadJudge(ballHistory[lastID][0],ballHistory[lastID][1],screenx,screeny))<=pickAngleThreshold:#angle right
                        state=systemState.automode_retrieve_go
                    else:
                        if math.fabs(RadJudge(ballHistory[lastID][0],ballHistory[lastID][1],screenx,screeny))>0:
                            callUno(Command.TURNRIGHT,150)
                            time.sleep(1)
                            callUno(Command.STOP)
                            time.sleep(1)
                        else:
                            callUno(Command.TURNLEFT,150)
                            time.sleep(1)
                            callUno(Command.STOP)
                            time.sleep(1)
    elif (state==systemState.automode_retrieve_go):
        pic = takePhoto()
        if 1!=-1:#HACK FIXME
            loc = TennisDetect(pic)
            if loc!=[0,0,0]:#FIXME
                callUno(Command.FORWARD);
                pass#SHOULD BE JUDGE WHEN TO PICK THE BALL AND EVENTUALLY PICK IT
                if (loc[2]>=73):#FIXME
                    callUno(Command.STOP);
                    print "close enough!"
                    time.sleep(2)
                    callUno(Command.PICK)
                    time.sleep(2)
                    state=systemState.automode_normal
            else:
                print "ball out-of-sight"
                state=systemState.automode_retrieve
    time.sleep(1)#give it a rest
#---------------------------------------------------------
