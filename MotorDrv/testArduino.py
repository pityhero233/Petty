import serial
# class Ser(object):
#     def __init__(self):
#         #open port
#         self.port = serial.Serial(port='ttyACM0', baudrate=9600, bytesize=8, parity='E', stopbits=1, timeout=2)

#     #autosend
#     def send_cmd(self, cmd):
#         self.port.write(cmd)
#         response = self.port.readall()
#         response = self.convert_hex(response)
#         return response

#     #convert to hex
#     def convert_hex(self, string):
#         res = []
#         result = []
#         for item in string:
#             res.append(item)
#         for i in res:
#             result.append(hex(i))
#         return result
# ser = serial.Serial("/dev/ttyACM1",9600)
# ser.write("1 111")
#!/usr/bin/env python  
# -*- coding: utf-8 -*  
   
import serial.tools.list_ports  
   
port_list = list(serial.tools.list_ports.comports())  
   
if len(port_list) <= 0:  
    print "The Serial port can't find!"  
       
else:  
    port_list_0 =list(port_list[0])  
   
    port_serial = port_list_0[0]  
   
    ser = serial.Serial(port_serial,9600,timeout = 60)  
   
    print "check which port was really used >",ser.name  
