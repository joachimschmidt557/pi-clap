#!/usr/bin/python

import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())    #List of serial ports (loaded automatically)

def getCOM():
    """
    Function that returns the COM port of the XBee (if available)
    """
    #Is list ports empty?
    if not ports:
        print("No Serial Ports found! Exiting now")
        exit()

    #If there is only one port available, automatically use that one
    if len(ports) == 1:
        return ports[0][0]

    #Display all available ports if there are more than one available
    print("Available Ports: ")
    for port in ports:
        print(port)
    return input("Enter Xbee Serialport: ")

if __name__ == "__main__":
    #Set up serial
    #try:
    serialport = getCOM()
    print("Establishing connection to: %s" % serialport)
    ser = serial.Serial(serialport, 9600, timeout=1)
    #except:
        #print("Error establishing connection to serial port. Exiting now")
        #exit()
    try:
        while True:
            ser.write(bytes([int(input("Enter value to send: "))]))
    except (KeyboardInterrupt, SystemExit):
        ser.close()
