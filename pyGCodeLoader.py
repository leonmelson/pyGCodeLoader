# !/usr/bin/python3
# version=0.1
import argparse
import serial
import time
# import os.path
from datetime import datetime
from urllib.request import urlopen

start_time = time.time()
ReadGCode = None
PortReceiveData = None
ReadLineCount = 0
ReadLineNCount = str()
inf = 1
parser = argparse.ArgumentParser(description='pyGCodeLoader')
parser.add_argument('-p', '--port', help="TTY/COM port path in '' if folders have spaces", required=False)
parser.add_argument('-pb', '--portbaud', help='Baud-rate', required=False)
parser.add_argument('-f', '--file', help="Gcode file path in '' if folders have spaces", required=False)
parser.add_argument('-u', '--url', help="Url to GCode", required=False)
parser.add_argument('-c', '--code', help="Gcode string separated by <> enclosed in ''", required=False)
parser.add_argument('-w', '--wait', help='Wait for a value="ok" to get returned before sending next line',
                    required=False)
parser.add_argument('-s', '--sleep', help='Sleep time = float = 0.001 between each command sent')
parser.add_argument('-r', '--receive', help='Receive port data with --sleep time only when --code, --url, '
                                            '--file is empty = enable')
parser.add_argument('-l', '--log', help="Append Log file path in '' if folders have spaces")
parser.add_argument('-inf', '--infloop', help='Infinite loop with manual code add until exit is typed = enable')
parser.add_argument('-debug', '--debug', help='Disable Writing to port and disable '
                                              '-w --wait function as not return will be available = enable')
args = parser.parse_args()
# Disable Wait if Debug is enabled
if args.debug == "enable":
    args.wait = None

# Infinite loop will be disabled if a file or code is add
if args.file is not None or args.code is not None:
    args.infloop = None

# print(args)
print("\n TTY/COM Port = ", args.port, " / Gcode file = ", args.file, " / Gcode string = ", args.code, "\n")


def gcode_line_fixer(gcode):
    # Change code to Upper
    # code = code.upper()
    # remove comments
    if gcode.find(';') >= 0:
        gcode = gcode.split(";", 1)
        gcode = gcode[0]
    elif gcode.find('#') >= 0:
        gcode = gcode.split("#", 1)
        gcode = gcode[0]
    else:
        gcode = gcode
    # Add G1 if it is not added
    if len(gcode) > 0 or gcode != "":
        if gcode[0] == "X" or gcode[0] == "Y" or gcode[0] == "Z":
            gcode = "G1" + gcode
    return gcode


# Create New Serial Port
if args.port is not None and args.portbaud is not None:
    print("\n Creating Serial Port ", args.port, args.portbaud, "\n")
    SPort = serial.Serial(args.port, args.portbaud)
else:
    print("\n Port not added exiting\n")
    exit()

# Read FILE if code and url is empty
if args.file is not None and args.code is None and args.url is None:
    print(' GCode File is being opened')
    with open(args.file, 'r') as GCodeFile:
        # GCodeFile = open(args.file, 'r')
        # print (ReadGCode.readlines())
        # remove \n from lines with .read().splitlines()
        ReadGCode = GCodeFile.read().splitlines()
        # print (" ",ReadGCode)

# Read URL
# TODO: decode html url
elif args.file is None and args.code is None and args.url is not None:
    print(' Url is being opened\n')
    GCodeFile = urlopen(args.url)
    GetGCode = GCodeFile.read()
    GetGCode = str(GetGCode)
    GetGCode = GetGCode.replace("b'", "")
    GetGCode = GetGCode.replace("'", "")
    if GetGCode.find('\\r\\n') >= 0:
        ReadGCode = GetGCode.split("\\r\\n")
    elif GetGCode.find('\\n') >= 0:
        ReadGCode = GetGCode.split("\\n")
    # print (ReadGCode)


# Read GCODE if file is empty
elif args.code is not None and args.file is None and args.url is None:
    print(' GCode is being sorted\n')
    ReadGCode = args.code.split("<>")
    # print (" ",ReadGCode)

elif args.code is None and args.file is None and args.url is None:
    if args.receive is not None and args.sleep is not None and args.wait is None:
        PortReceiveData = 1
        print("\n No File or GCode has been add Enabling Receive Mode\n")
    else:
        print("\n No File or GCode has been add Enabling Typing Mode\n")

else:
    print(" Please do not provide a file and code at the same time")

    # Display Functions in a Class
    # print(dir(SPort))
while inf == 1:
    infstart_time = time.time()
    if args.code is None and args.file is None and args.url is None and PortReceiveData is None:
        ReadGCode = input(" Waiting for command string separated by <> enclosed in ''. \n\n >>> ")
        if ReadGCode == 'EXIT' or ReadGCode == 'exit':
            # print ("\n\n Exiting pyGCodeLoader!!!")
            # print (" >>>>>")
            # print (" >>>>>>>>>>")
            # print (" >>>>>>>>>>>>>>>")
            break
        elif ReadGCode == "":
            ReadGCode = ""
        else:
            ReadGCode = ReadGCode.split("<>")
            # print (" ",ReadGCode)

    if ReadGCode is not None:
        print(' Staring loading GCode\n')

        for GCode in ReadGCode:
            if args.file is not None or args.url is not None:
                ReadLineCount = ReadLineCount + 1
                ReadLineNCount = "N" + str(ReadLineCount) + " "
            gcode_line = gcode_line_fixer(GCode)
            if len(gcode_line) > 0 or gcode_line != "":
                if args.debug == "enable":
                    print(' Sending:   ' + gcode_line)
                    print(" Debug Mode")
                else:
                    # Add log for sent
                    if args.log is not None:
                        with open(args.log, "a") as logfile:
                            # logfile = open(args.log, "a+")
                            # SendCommandString = datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f") + " - Send: "
                            # + code.strip() + "\n"
                            logfile.write(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S.%f')}"
                                          f" - Send: {ReadLineNCount} {gcode_line.strip()} \n")
                    print(' Sending:   ' + gcode_line.strip())
                    # noinspection PyUnboundLocalVariable
                    SPort.write(str.encode(gcode_line + '\n'))
                    if args.wait is not None:
                        while inf == 1:
                            ReadPort = SPort.readline()
                            ReadPort = ReadPort.decode("utf-8")
                            ReadPort = ReadPort.strip()
                            # Add log for received
                            if args.log is not None and args.wait is not None:
                                with open(args.log, "a") as logfile:
                                    logfile.write(datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f")
                                                  + " - Recv: " + ReadPort + "\n")
                            print(' Received: ', ReadPort)
                            if ReadPort.find(args.wait) >= 0:
                                break
                    # print (ReadPort)
            if args.sleep is not None:
                time.sleep(float(args.sleep))
    # If Receive is enabled
    if PortReceiveData == 1:
        ReadPort = SPort.readline()
        ReadPort = ReadPort.decode("utf-8")
        ReadPort = ReadPort.strip()
        print(ReadPort)
        if args.log is not None:
            with open(args.log, "a") as logfile:
                # logfile = open(args.log, "a+")
                logfile.write(datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f") + " - Recv: " + ReadPort + "\n")
        time.sleep(float(args.sleep))
    # If Inf loop is disable exit
    if args.infloop is None:
        # print ("\n\n Exiting pyGCodeLoader!!!")
        # print (" >>>>>")
        # print (" >>>>>>>>>>")
        # print (" >>>>>>>>>>>>>>>>")
        break
# Close file if Wait is empty
# if args.log is not None and args.wait is None:
#     logfile.close()
SPort.close()
if args.debug is not None:
    print("--- %s seconds ---" % (time.time() - start_time))
