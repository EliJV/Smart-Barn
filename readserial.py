import time
import re
import json
import serial
import serial.tools.list_ports as port_list
from Hologram.HologramCloud import HologramCloud

ports = list(port_list.comports())

#Python changes made it unable to grab dynamically
#Dynamically grabs port
for p in ports:
    print (p)

#Sets port information
comport = '/dev/ttyACM7'
print ("Using: " + comport)
serialPort = serial.Serial(comport, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# Used to hold data coming over UART
serialString = ""

def waterlevel(data):
    if data.startswith('<info> app: WL data:'):
        waterdata = int(data[20:])
    if data.starts('<info> app: WL cal:'):
        x = re.split(',|\.',data)
        upperlimit, lowerlimit = x
        upperlimitd = re.findall(r'\d+', upperlimit)
        lowerlimitd = re.findall(r'\d+', lowerlimit)
        uplimit = (int(upperlimitd[0]))
        lowlimit = (int(lowerlimitd[0]))
        print (uplimit)
        print (lowlimit)
        adjustdata = (waterdata - lowlimit)
        datarange = (uplimit - lowlimit)
        percentfull = (adjustdata/datarange)
        gallons = percentfull*5.5
        return gallons

while(1):
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        message=(serialString.decode('Ascii'))

        # Print the contents of the serial data
        print(message)

        #Water logic if connected
        gallons = waterlevel(message)
        print('Gallons in Bucket:' + str(gallons))

        #Send information to the cloud
        hologram = HologramCloud(dict(), network='cellular')
        print('Cloud type: ' + str(hologram))