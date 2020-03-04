import re
import serial
import serial.tools.list_ports as port_list

a=-1

#Finds and prints ports
ports = list(port_list.comports())
#Dynamically grabs port
for p in ports:
    for comms in p:
        a=a+1
        if comms.startswith('JLink'):
            comport=p[a-1]

#Todo grab port dynamically using regex
port= comport
serialPort = serial.Serial(port, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART


while(1):
    #Appends to this txt file
    f=open("UARTData.txt","a+")
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        message=(serialString.decode('Ascii'))

        #Appends message to text file
        f.write(message)

        # Print the contents of the serial data
        print(message)

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        serialPort.write(b"Thank you for sending data \r\n")

        #Closes txt file
