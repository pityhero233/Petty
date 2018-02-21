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
            time.sleep(0.1)
        else:
            print "no difference"
            time.sleep(0.5)

def CircleDetect():
    global lower,upper,LowerBlue,UpperBlue,iBest
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            _,frame2 = cam2.read()
            
        except aa:
            print("E:get frame error.")
            print(aa.message)
            os._exit()
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

        HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
        H,S,V = cv2.split(HSV)
        mask = cv2.inRange(HSV,lower,upper)
        certain = cv2.bitwise_and(frame2,frame2,mask=mask)

        diff = cv2.GaussianBlur(certain,(5,5),0)
        diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
        diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)

        gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)



        circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)

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
            pass
        if (iBest!=-1):
            try:
                cv2.circle(frame2,(circlesm[iBest][0],circlesm[iBest][1]),circlesm[iBest][2],(0,255,0),5)
                #name = "test#"+str(count)+".jpg"
                #name2 = "test#"+str(count)+"c.jpg"
                #cv2.imwrite(name,frame2);
                #cv2.imwrite(name2,diff)
                cv2.imshow("splitter",np.hstack([frame2,diff]))
                cv2.waitKey(10)
                pass
            except TypeError,e:
                #print e.message
                pass
                #print "E:Segmentation Fault while choosing iBest"
        else:
            pass
            #print "no best circle chosen..."
        #cv2.imshow("splitter",np.hstack([frame2,certain]))
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #time.sleep(1)
    cv2.destroyAllWindows();

#--------------------------------------------------------------
print "step 1:start camera and apache2 service..."
try:
    lastString = ReadRawFile('''/var/log/apache2/access.log''')
    print "lastString=",lastString
    start_apache()

except:
    print "apache2 start error."
    print "perhaps root priveilges not given?"
    os._exit()

try:
    cam2 = cv2.VideoCapture(1)
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
except:
    print "E:cam error"
    system._exit()
count = 0
print "step 2:start video service..."
try:
    thread.start_new_thread(start_service,())
except:
    print "New Thread Error"
    os._exit()

print "step 3:start android responding service..."
try:
    thread.start_new_thread(requestHandler,())
except:
    print "New requestHandler thread Error"
    os._exit()

print "step 4:circle detect"
CircleDetect();
#-------------------------------

