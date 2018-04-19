import serial
import serial.tools.list_ports

def callUno(action,parameter=-1):
    if (parameter==-1):
        arduino.write(str(action)+" "+str(normalSpeed))
    else:
        if parameter>0 and parameter<=999:
            arduino.write(str(action)+" "+str(parameter))
        else:
            print("E:callUno parameter fail")
def scanUno():
    print "step 0 of 6:perform arduino detection"
    port_list = list(serial.tools.list_ports.comports())  
    if len(port_list)<=0:
        print("E:arduino base not found.")
    else:
        pl1 =list(port_list[0]) 
        port_using = pl1[0]
        return arduino.name