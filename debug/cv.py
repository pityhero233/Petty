import cv2
import math
import time
import thread
lower = (25,85,6)
upper = (64,255,255)
rounds = []
def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def takePhoto(cam2):
    try:
        _,frame = cam2.read()
        return frame
    except:
        print "take fail.frome takePhoto()"
        return -1
cam2 = cv2.VideoCapture(0)
currentPhoto = takePhoto(cam2)

def photoPool(cam):#grab&throw excessive frames and refresh pool every 0.5 secs
    bt = time.time()
    while True:
        _,_ = cam.grab()#FIXME #1
        if (time.time()-bt)>0.5:
            print "photoPool updated."
            _,currentPhoto = cam.read()
            bt = time.time()

def flush(cam):
    bt = time.time()
    while bt==time.time():
        cam.grab()
    print "flush complete."


def getPhoto(cam):
    flush(cam)
    return takePhoto(cam)

def current():
    show(getPhoto(cam2))

def show(pic):
    try:
        cv2.namedWindow("debug",cv2.WINDOW_AUTOSIZE)
        cv2.imshow("debug",pic)
        cv2.waitKey(0)
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



