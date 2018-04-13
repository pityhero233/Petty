import cv2
import numpy as np
import time
#import os.system as sys
import os
import string
lower = np.array([40,0,0])
upper = np.array([85,255,255])
LowerBlue = np.array([100, 0, 0])
UpperBlue = np.array([130, 255, 255])
iBest = -1.0
try:
    cam2 = cv2.VideoCapture(1)
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
except:
    print "E:cam error"
    system._exit()
count = 0
#-------------------------------
while count < 1000:
    count = count + 1
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
    H,S,V = cv2.split(HSV)
    gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
    try:
        circlesm = circles1[0,:,:]
        circlesm = np.uint16(np.around(circlesm))
        bestConf = -1
        for index,i in enumerate(circlesm[:]):
            cv2.circle(frame2,(i[0],i[1]),i[2],(255,0,0),5)
            # cv2.circle(certain,(i[0],i[1]),i[2],(255,0,0),5)
            # cv2.circle(diff,(i[0],i[1]),i[2],(255,0,0),5)
        #print "circle:",i[0],"x",i[1],",r=",i[2]
            bx = i[0]-i[2];by = i[1]-i[2];
            ex = i[0]+i[2]-1;ey = i[1]+i[2]-1;
            confident = 0;
            for x in range(bx,ex):
                for y in range(by,ey):
                    try:
                        h=H[y,x]
                        if 40<h<85:
                            confident = confident + 1 
                    except IndexError,e:
                        pass
                        print e.message;
                        #print("W:Index read error\n")
            confident = confident*1000.0/(4.0*i[2]*i[2]) #the area percent of green detected
            #print "confidence = ",confident
            if bestConf<confident:
                bestConf = confident
                iBest = index

    except TypeError,e:
        print("no circle detected!")
        pass
    if (iBest!=-1):
        print "Best circle chosen @i=",iBest,",conf=",bestConf,",R=",circlesm[iBest][2]

        try:
            cv2.circle(frame2,(circlesm[iBest][0],circlesm[iBest][1]),circlesm[iBest][2],(0,255,0),5)
            #name = "test#"+str(count)+".jpg"
            #name2 = "test#"+str(count)+"c.jpg"
            #cv2.imwrite(name,frame2);
            #cv2.imwrite(name2,diff)
            cv2.imshow("splitter",frame2)
            cv2.waitKey(10)
            pass;
        except TypeError,e:
            #print e.message
            pass
            #print "E:Segmentation Fault while choosing iBest"
    else:
        pass
        #print "no best circle chosen..."
    #cv2.imshow("splitter",frame2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #time.sleep(1)
