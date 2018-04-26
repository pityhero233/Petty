import time
import difflib
lastString = ""
def ReadRawFile(filepath):
    file = open(filepath)
    try:
        tempa = file.read();
    finally:
        file.close()
        tempa = tempa.replace(" ","").replace("\n","")
    return tempa

def requestHandler():
    global lastString
    current=ReadRawFile('''/var/log/apache2/access.log''')
    if (current!=lastString):
        #new command detected
        command = current.replace(lastString,"")
        lastString = current;
        if command.find("__MoveLeft"):
            pass;
            print "Left"
        elif command.find("__MoveRight"):
            pass;
            print "Right"
        elif command.find("__MoveForward"):
            pass;
            print "Forward"
        elif command.find("__MoveBackward"):
            pass;
            print "Backward"
        elif command.find("__AutoModeUp"):
            pass;
            print "AutoUp"
        elif command.find("__AutoModeDown"):
            pass;
            print "AutoDown"
        else:
            print "W:unknown HTTP request."
            print command;
        time.sleep(0.1)
    else:
        time.sleep(0.5)
        print "no difference"

lastString = ReadRawFile('''/var/log/apache2/access.log''')
print "beg,lastString=",lastString
while True:
    requestHandler();

