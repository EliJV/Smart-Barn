import re
import json
import serial
import serial.tools.list_ports as port_list
from Hologram.HologramCloud import HologramCloud


a=-1

#Finds and prints ports
ports = list(port_list.comports())

#Dynamically grabs port
for p in ports:
    for comms in p:
        a = a + 1
        if comms.startswith('JLink'):
            comport = p[a-1]

#Sets port information
print (comport)
port = comport
serialPort = serial.Serial(port, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART

def waterlevel(data):
    if data.startswith('<info> app: WL data:'):
            waterout = int(data[20:])
            percentfull = (waterout/255)
            gallons = (5.5*percentfull)
            return gallons

while(1):
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):
        #Opens a text file to append to
        text_file=open("UARTData.txt","a+")

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        message=(serialString.decode('Ascii'))

        # Appends message to text file
        text_file.write(message)

        # Print the contents of the serial data
        print(message)

        #Water logic if connected
        gallons = waterlevel(message)
        print('Gallons in Bucket:' + str(gallons))

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        serialPort.write(b"Thank you for sending data \r\n")

        #Send information to the cloud
        hologram = HologramCloud(dict(), network'cellular')
        print('Cloud type: ' + str(hologram))
        payload = {"WaterLevel":gallons}
        recv =hologram.sendMessage(json.dumps(payload)

        # Closes txt file
        text_file.close()
