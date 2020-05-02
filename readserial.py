import sys
import time
import re
import json
import serial
import serial.tools.list_ports as port_list
from Hologram.HologramCloud import HologramCloud

ports = list(port_list.comports())

uplimit = 0
lowlimit = 0

#Python changes made it unable to grab dynamically
#Dynamically grabs port
for p in ports:
    print (p)


#Sets port information
comport = '/dev/ttyACM0'
print ("Using: " + comport)
serialPort = serial.Serial(comport, baudrate=115200,
                           bytesize=8, timeout=3, stopbits=serial.STOPBITS_ONE)

while(1):
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        message=(serialString.decode('Ascii'))
        percentfull = 0
        sensor = ""
        #print(message)
        msgTemp  = message.split(':')
        try:
            sensor = msgTemp[1]
        except:
            print("No sensor data detected: %s", message)


        if "WL" in sensor:
            if "cal" in sensor:
                lo, hi = msgTemp[2].split(',')
                lowlimit = int(lo.strip())
                uplimit = int(hi.strip())
                print("WL Cal values recieved: ", lowlimit, uplimit)
            else:
                try:
                    print(msgTemp[2])
                    level = int(msgTemp[2]) - lowlimit if  \
                            int(msgTemp[2])- lowlimit > 0 else 0 #avoid problems with bad cal
                    gallons = 5.5 * (level / (uplimit - lowlimit))
                    msg = {"WaterLevel":gallons}
                    print(msg)
                    hologram = HologramCloud(dict(), network='cellular')
                    recv = hologram.sendMessage(json.dumps(msg), timeout=3)
                    print(hologram.getResultString(recv))
                except:
                    print("Error sending msg: ", msg)
                    try:
                        print("Hologram msg: ", recv)
                    except:
                        print("Holoram msg error: ", sys.exc_info()[0])
                    print("Error info: ", sys.exc_info()[0])
        elif "DS" in sensor:
            try:
                msg = {"DoorAlarm": msgTemp[2].strip()}
                print(msg)
                hologram = HologramCloud(dict(), network='cellular')
                recv = hologram.sendMessage(json.dumps(msg), timeout=3)
                print(hologram.getResultString(recv))
            except:
                print("Error sending msg: ", msg)
                try:
                    print("Hologram msg: ", recv)
                except:
                    print("Holoram msg error: ", sys.exc_info()[0])
                print("Error info: ", sys.exc_info()[0])
        elif "FA" in sensor:
            try:
                msg = {"FireAlarm": msgTemp[2].strip()}
                print(msg)
                hologram = HologramCloud(dict(), network='cellular')
                recv = hologram.sendMessage(json.dumps(msg), timeout=3)
                print(hologram.getResultString(recv))
            except:
                print("Error sending msg: ", msg)
                try:
                    print("Hologram msg: ", recv)
                except:
                    print("Holoram msg error: ", sys.exc_info()[0])
                print("Error info: ", sys.exc_info()[0])
