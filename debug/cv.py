import cv2
import math
import time
import thread
import os
import numpy as np
lower = (25,85,6)
upper = (64,255,255)
rounds = []
systemDevice = "/dev/video1"

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def takePhotoDeprecated(cam2):
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

currentPhoto = takePhoto()

# def photoPool(cam):#grab&throw excessive frames and refresh pool every 0.5 secs
#     bt = time.time()
#     while True:
#         _,_ = cam.grab()#FIXME #1
#         if (time.time()-bt)>0.5:
#             print "photoPool updated."
#             _,currentPhoto = cam.read()
#             bt = time.time()

# def flush(cam):
#     bt = time.time()
#     while bt==time.time():
#         cam.grab()
#     print "flush complete."


# def getPhoto(cam):
#     flush(cam)
#     return takePhoto(cam)

def current():
    show(takePhoto())

def show(pic):
    try:
        cv2.namedWindow("debug",cv2.WINDOW_AUTOSIZE)
        cv2.imshow("debug",pic)
        cv2.waitKey(20)
    except:
        print "fail in show()"
    finally:
        cv2.destroyAllWindows()
def isDangerous(frame1,frame2,px,py):#detect if point(px,py) is in "the moving area of frame"(dog)
    gray1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)#FIXME 1
    gray2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)#FIXME 2
    diff = cv2.absdiff(gray1,gray2)
    _,thr = cv2.threshold(diff,15,255,cv2.THRESH_BINARY)#FIXME 3&4
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




def getCircleOrg(frame2):
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(HSV)
    gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    circles1 = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
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
            return frame2
        except:
            print "E:Segmentation Fault while choosing iBest"

def getCircleOrgBetter(frame2):
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

    HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)

    #HSV = cv2.GaussianBlur(HSV, (5, 5), 0)
    H,S,V = cv2.split(HSV)
    mask = cv2.inRange(HSV,lower,upper)
    certain = cv2.bitwise_and(frame2,frame2,mask=mask)
    #cv2.imshow("splitter",np.stack([frame,frame2,certain]))
    diff = cv2.GaussianBlur(certain,(5,5),0)
    diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
    diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)

    gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
#print(frame2.shape)

#circles1= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=240)
    circles1 = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
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
            #name = "test#"+str(count)+".jpg"
            #name2 = "test#"+str(count)+"c.jpg"
            #cv2.imwrite(name,frame2);
            #cv2.imwrite(name2,diff)
            return frame2
            #v2.waitKey(10)
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
