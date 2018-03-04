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
class SerialPort(object):
    def __init__(self):
        # 打开端口
        self.port = serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=2)

    # 发送指令的完整流程
    def send_cmd(self, cmd):
        self.port.write(cmd)
        response = self.port.readall()
        response = self.convert_hex(response)
        return response

    # 转成16进制的函数
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result

s = SerialPort();#init serial comm;
@app.route('/left')
def left():
    s.send_cmd("L")

@app.route('/right')
def right():
    s.send_cmd("R")

@app.route('/forward')
def forward():
    s.send_cmd("F")

@app.route('/back')
def back():
    s.send_cmd("B")

@app.route('/autoup')
def autoup():
    if !automode:
        automode=True;
@app.route('/autodown')
def autodown():
    if automode:
        automode=False;


def start_service():
    res=os.system('''./mjpg_streamer -i "input_uvc.so -d /dev/video1 -f 10 -y" -o "output_http.so -w www -p 8888"''')

def flasker():#user response service
    app.run()


#----------------------------------------------------


try:
    cam2 = cv2.VideoCapture(0)
    cv2.namedWindow("splitter",cv2.WINDOW_AUTOSIZE)
except:
    print "E:cam error"
    system._exit()

print "step 2:start video service..."

print "step 3:start handy motion service..."




#-------------------------------
