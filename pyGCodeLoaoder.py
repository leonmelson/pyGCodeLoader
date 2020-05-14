#!/usr/bin/python3.7
#version=0.1
import argparse
import serial
import time

start_time = time.time()
inf = 1
parser = argparse.ArgumentParser(description='pyGCodeLoader')
parser.add_argument('-p', '--port', help="TTY/COM port path in '' if folders have spaces", required=False)
parser.add_argument('-pb', '--portbaud', help='Baudrate', required=False)
parser.add_argument('-f', '--file', help="Gcode file path in '' if folders have spaces", required=False)
parser.add_argument('-c', '--code', help="Gcode string seperated by <> enclosed in ''", required=False)
parser.add_argument('-w', '--wait', help='Wait for a value="ok" to get returned before sending next line', required=False)
parser.add_argument('-s', '--sleep', help='Sleep time = float = 0.001 between each command sent')
parser.add_argument('-l', '--log', help="Append Log file path in '' if folders have spaces")
parser.add_argument('-inf', '--infloop', help='Infinite loop with manual code add until exit is typed = enable')
parser.add_argument('-debug', '--debug', help='Disable Writing to port and disable -w --wait funtion as not return will be available = enable')
args = parser.parse_args()
#Disable Wait if Debug is enabled
if(args.debug=="enable"):
    args.wait = None
    
#Infinte loop will be disabled if a file or code is add
if(args.file != None or args.code != None):
    args.infloop = None

#print(args)
print("\n TTY/COM Port = ", args.port, " / Gcode file = ", args.file, " / Gcode string = ", args.code,"\n")

def GCodeLineFixer(code):
    #Change code to Upper    
    code = code.upper()
    #remove comments
    if(code.find(';') >= 0):
        code = code.split(";", 1)
        code = code[0]
    elif(code.find('#') >= 0):
        code = code.split("#", 1)
        code = code[0]
    else:
        code = code
    
    #Add \n to code
    code = code + '\n'
    return code

# Create New Serail Port
if(args.port != None and args.portbaud != None):
    print("\n Creating Serial Port ", args.port, args.portbaud,"\n")
    SPort = serial.Serial(args.port, args.portbaud)
else:
    print("\n Port not added exiting\n")
    exit()
            
# Read FILE in if code is empty
if(args.file != None and args.code == None):
    print (' GCode File is being opened')
    GCodeFile = open(args.file, 'r')
    #print (ReadGCode.readlines())
    #remove \n from lines with .read().splitlines()
    ReadGCode = GCodeFile.read().splitlines()
    #print (ReadGCode)

# Read GCODE if file is empty
elif(args.code != None and args.file == None):
    print (' GCode is being sorted')
    ReadGCode = args.code.split("<>")
    #print (" ",ReadGCode)

elif(args.code == None and args.file == None):
    print ("\n No File or GCode has been add Enabling Typing Mode\n")

else:
    print (" Please do not provide a file and code at the same time")
 

    #Display Functions in a Class
    #print(dir(SPort))
while(inf==1):
    if(args.code == None and args.file == None):
        ReadGCode = input(" Waiting for command string seperated by <> enclosed in ''. \n\n >>> ")
        if(ReadGCode == 'EXIT' or ReadGCode == 'exit'):
            print ("\n\n Exiting pyGCodeLoader!!!")
            print (" >>>>>")
            print (" >>>>>>>>>>")
            print (" >>>>>>>>>>>>>>>")
            break
        elif(ReadGCode==""):
            ReadGCode = ""
        else:
            ReadGCode = ReadGCode.split("<>")
            #print (" ",ReadGCode)
    
    if(ReadGCode!=""):    
        print(' Staring loading GCode')

        for GCode in ReadGCode:
            code = GCodeLineFixer(GCode)
            if(len(code) > 0):                
                if(args.debug == "enable"):
                    print(' Sending:   ' + code)
                    print(" Debug Mode")
                else:
                    print(' Sending:   ' + code)
                    SPort.write(str.encode(code))
                    if(args.wait != None):
                        while(inf==1):
                            ReadPort = SPort.readline()
                            ReadPort = ReadPort.decode("utf-8")
                            ReadPort = ReadPort.strip()
                            print(' Received: ',ReadPort)
                            if(ReadPort.find(args.wait) >= 0):
                                break
                    #print (ReadPort)
            if(args.sleep!=None):
                time.sleep(float(args.sleep))
                

        if(args.infloop==None):
            print ("\n\n Exiting pyGCodeLoader!!!")
            print (" >>>>>")
            print (" >>>>>>>>>>")
            print (" >>>>>>>>>>>>>>>>")
            break

SPort.close()
SPort.close()
print("--- %s seconds ---" % (time.time() - start_time))
