import serial
import serial.tools.list_ports
from enum import Enum
normalSpeed = 111
class Command(Enum):
                 # 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT
    STOP = 0
    FORWARD = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4
    TURNLEFT = 5
    TURNRIGHT = 6
    SHOOT = 7
    PICK = 8
def scanUno():
    print "step 0 of 6:perform arduino detection"
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list)<=0:
        print("E:arduino base not found.")
    else:
        pl1 =list(port_list[0])
        port_using = pl1[0]
        arduino = serial.Serial(port_using,57600,timeout = 60)
        print("using ",arduino.name)
        return arduino

def callUno(arduino,action,parameter=-1):
    if (parameter==-1):
        if action==Command.STOP:
            arduino.write('0')
        else:
            arduino.write(str(action)+" "+str(normalSpeed))
    else:
        if action==Command.STOP:
            arduino.write('0')
        else:
            if parameter>0 and parameter<=999:
                arduino.write(str(action)+" "+str(parameter))
            else:
                print("E:callUno parameter fail")

def mood(bluno):#TODO:return dog mood based on recently acceleration count,1to100,integer/float
    while True:
        raw=bluno.read_until("\r\n")
        while raw!='':
            x,y,z = raw.split(",")
            print("x=",x,",y=",y,",z=",z)
            raw=''
