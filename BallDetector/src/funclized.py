#!/usr/bin/python
import cv2
import numpy as np
import time
import os
import thread
import string
import difflib

lower = np.array([40,0,0])
upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
iBest = -1.0
lastString = ""
#totAvgConfident=0;#last 10 round's average confident,used to recognize round
totAvgRadius=31;#last 3 round's average Radius,used to recognize round
R=[30,31,32]
def start_apache():
    res=os.system('''sudo service apache2 restart''')

def start_service():
    res=os.system('''./mjpg_streamer -i "input_uvc.so -d /dev/video0 -f 10 -y" -o "output_http.so -w www -p 8888"''')

def ReadRawFile(filepath):
    file = open(filepath)
    try:
        tempa = file.read()
    finally:
        file.close()
        tempa = tempa.replace(" ","").replace("\n","")
    return tempa

def requestHandler():
    global lastString
    while True:
        current=ReadRawFile('''/var/log/apache2/access.log''')
        if (current!=lastString):
            #new command detected
            command = current.replace(lastString,"")
            lastString = current;
            if command.find("__MoveLeft")!=-1:
                pass;
                print "Left"
            elif command.find("__MoveRight")!=-1:
                pass;
                print "Right"
            elif command.find("__MoveForward")!=-1:
                pass;
                print "Forward"
            elif command.find("__MoveBackward")!=-1:
                pass;
                print "Backward"
            elif command.find("__AutoModeUp")!=-1:
                pass;
                print "AutoUp"
            elif command.find("__AutoModeDown")!=-1:
                pass;
                print "AutoDown"
            else:
                print "W:unknown HTTP request."
                print command;
            time.sleep(0.05)
        else:
            print "no difference"
            time.sleep(0.5)

def RadJudge(x,y,r,X,Y):
    if (x>X or y>Y):
        print "E:RadJudge Out-of-bound"
        os._exit();
    
    relativeX = (x-X/2)/X
    return relativeX

def getDiff(frame2):
    if True:
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

        HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
        H,S,V = cv2.split(HSV)
        mask = cv2.inRange(HSV,lower,upper)
        certain = cv2.bitwise_and(frame2,frame2,mask=mask)

        diff = cv2.GaussianBlur(certain, (5, 5), 0)
        diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
        diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)
    return diff;

def confidenceCalc(circles1):
    global iBest
    if True:
        try:
            circlesm = circles1[0,:,:]
            circlesm = np.uint16(np.around(circlesm))
            bestConf = -1
            for index,i in enumerate(circlesm[:]):
                cv2.circle(frame2,(i[0],i[1]),i[2],(255,0,0),5)
                cv2.circle(certain,(i[0],i[1]),i[2],(255,0,0),5)
                cv2.circle(diff,(i[0],i[1]),i[2],(255,0,0),5)
                print "circle:",i[0],"x",i[1],",r=",i[2]
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
                            print("W:Index read error\n")
                confident = confident+1000.0*(i[2]-totAvgRadius)/totAvgRadius#consider totavgRadius effect
                print "Radius Bonus = ",confident
                confident = confident*1000.0/(4.0*i[2]*i[2])
                print "confidence = ",confident
                if bestConf<confident:
                    bestConf = confident
                    iBest = index

            if bestConf<1000.0:#no match
                iBest=-1.0;
                print "no best match,best=",bestConf
            else:#update totAvgRadius
                R[2]=R[1];R[1]=R[0];R[0]=circlesm[iBest][2];
                totAvgRadius = (R[2]+R[1]+R[0])/3.0;

def CircleDetect():
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
        gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
        confidenceCalc(circles1);

        except TypeError,e:
            pass
        if (iBest!=-1):
            try:
                cv2.circle(frame2,(circlesm[iBest][0],circlesm[iBest][1]),circlesm[iBest][2],(0,255,0),5)
                p=RadJudge(circlesm[iBest][0],circlesm[iBest][1],circlesm[iBest][2],640,480)
                print "Relative X = p"
                #name = "test#"+str(count)+".jpg"
                #name2 = "test#"+str(count)+"c.jpg"
                #cv2.imwrite(name,frame2);
                #cv2.imwrite(name2,diff)
                cv2.imshow("splitter",np.hstack([frame2,diff]))
                cv2.waitKey(10)
                pass
            except TypeError,e:
                print e.message
                pass
                print "E:Segmentation Fault while choosing iBest"
        else:
            pass
            print "no best circle chosen..."
        #cv2.imshow("splitter",np.hstack([frame2,certain]))
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #time.sleep(1)
    cv2.destroyAllWindows();

#--------------------------------------------------------------
print "start"
CircleDetect()
#-------------------------------

