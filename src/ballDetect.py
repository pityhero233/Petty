import cv2
import numpy as np
class circle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r

def getCircles(frame2):
    gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,150,param1=100,param2=30,minRadius=15,maxRadius=100)
    circlesm = circles1[0,:,:]
    circlesm = np.uint16(np.around(circlesm))
    return circlesm

def ChooseBest(frame2,circlesm):
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    pass;
    HSV =  cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(HSV)
    mask = cv2.inRange(HSV,lower,upper)
    certain = cv2.bitwise_and(frame2,frame2,mask=mask)
    pass;
    diff = cv2.GaussianBlur(certain,(5,5),0)
    diff = cv2.threshold(certain, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,element)
    diff = cv2.morphologyEx(diff,cv2.MORPH_CLOSE,element)
    pass;
    try:
        bestConf = -1
        for index,i in enumerate(circlesm[:]):
            bx = i[0]-i[2];by = i[1]-i[2];
            ex = i[0]+i[2];ey = i[1]+i[2];
            confident = 0;
            for x in range(bx,ex):
                for y in range(by,ey):
                    try:
                        for vector in diff[y,x,:]:
                            if vector >125:
                                confident = confident + 1
                    except IndexError:
                        pass;
            confident = confident*1000.0/(4.0*i[2]*i[2])
            if bestConf<confident:
                bestConf = confident
                iBest = index
    except TypeError:
        pass
    if (iBest!=-1):
        try:
            c = circle(circlesm[iBest][0],circlesm[iBest][1],circlesm[iBest][2]);
            return c;
        except TypeError:
            pass;

