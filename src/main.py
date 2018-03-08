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

while True:
    print 'fine'
    time.sleep(10)


#-------------------------------
