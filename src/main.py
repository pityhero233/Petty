#!/usr/bin/python
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask
import time
import os
import thread
import string
import serial

responder = Flask(__name__);
lower = np.array([40,0,0])
upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
iBest = -1.0
automode = True;

def dbg():
    print("2333")

class SerialPort(object):
    def __init__(self):
        # port open 
        self.port = serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=2)

    # send
    def send_cmd(self, cmd):
        self.port.write(cmd)
        response = self.port.readall()
        response = self.convert_hex(response)
        return response

    # converter to 16
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result
print "step0:init COM4"
try:
    #s = SerialPort();#init serial comm;
    pass
except:
    print "serial error"

@responder.route('/left')
def left():
    print 'L OK'
    dbg();
    s.send_cmd("L")

@responder.route('/right')
def right():
    s.send_cmd("R")

@responder.route('/forward')
def forward():
    s.send_cmd("F")

@responder.route('/back')
def back():
    s.send_cmd("B")

@responder.route('/autoup')
def autoup():
    if not automode:
        automode=True;
@responder.route('/autodown')
def autodown():
    if automode:
        automode=False;
@responder.route('/shoot')
def shoot():
    pass;
@responder.route('/push')
def push():
    pass;


def start_service():
    res=os.system('''./mjpg_streamer -i "input_uvc.so -d /dev/video1 -f 10 -y" -o "output_http.so -w www -p 8888"''')

def flasker():#user response service
    responder.run(host='0.0.0.0')


#----------------------------------------------------

print "step1:start auto service..."
try:
    cam2 = cv2.VideoCapture(0)
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
except:
    print "E:cam error"
    os._exit()

print "step 2:start user video service..."
try:
    thread.start_new_thread(start_service,());
except:
    print "E:user camera thread start error"

print "step 3:start user request Flask listener..."
try:
    thread.start_new_thread(flasker,());
except:
    print "E:flask start error"

print "step 4:start auto capture service.."
while True:
    #print "Test #",count,":"
    try:
        _,frame2 = cam2.read()
    #cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
    except aa:
        print("E:get frame error.")
        print(aa.message)
        os._exit()
#es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

    HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)

    #HSV = cv2.GaussianBlur(HSV, (5, 5), 0)
    H,S,V = cv2.split(HSV)
    mask = cv2.inRange(HSV,LowerBlue,UpperBlue)
    certain = cv2.bitwise_and(frame2,frame2,mask=mask)
    #cv2.imshow("splitter",np.stack([frame,frame2,certain]))
    diff = cv2.GaussianBlur(certain,(5,5),0)
    diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
    diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)

    gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
#print(frame2.shape)

#circles1= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=240)
    circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
#circles2 = cv2.HoughCircles(diff,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
    try:
        circlesm = circles1[0,:,:]
        circlesm = np.uint16(np.around(circlesm))
        bestConf = -1
        for index,i in enumerate(circlesm[:]):
            cv2.circle(frame2,(i[0],i[1]),i[2],(255,0,0),5)
            cv2.circle(certain,(i[0],i[1]),i[2],(255,0,0),5)
            cv2.circle(diff,(i[0],i[1]),i[2],(255,0,0),5)
        #print "circle:",i[0],"x",i[1],",r=",i[2]
            bx = i[0]-i[2];by = i[1]-i[2];
            ex = i[0]+i[2];ey = i[1]+i[2];
            confident = 0;
            for x in range(bx,ex):
                for y in range(by,ey):
                    try:
                        for vector in diff[y,x,:]:
                            if vector >125:
                                confident = confident + 1
                    except IndexError,e:
                        pass
                        #print e.message;
                        #print("W:Index read error\n")
            confident = confident*1000.0/(4.0*i[2]*i[2])
            #print "confidence = ",confident
            if bestConf<confident:
                bestConf = confident
                iBest = index

    except TypeError,e:
        #print("no circle detected!")
        pass
    if (iBest!=-1):
        #print "Best circle chosen @i=",iBest,",conf=",bestConf,",R=",circlesm[iBest][2]

        try:
            cv2.circle(frame2,(circlesm[iBest][0],circlesm[iBest][1]),circlesm[iBest][2],(0,255,0),5)
            cv2.imshow("splitter",np.hstack([frame2,diff]))
            cv2.waitKey(10)
            pass
        except TypeError,e:
            #print e.message
            pass
            #print "E:Segmentation Fault while choosing iBest"
    time.sleep(10)


#-------------------------------
