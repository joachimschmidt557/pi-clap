#!/usr/bin/python
import pyaudio
import sys
import _thread
from time import sleep
from array import array
#import RPi.GPIO as GPIO

import serial
import serial.tools.list_ports

clap = 0
wait = 2
pin = 24
exitFlag = False
waitingForMoreClaps = False

ports = list(serial.tools.list_ports.comports())    #List of serial ports (loaded automatically)

currentlyOn = False
clapInProgress = False

ON_POSITION = 0
OFF_POSITION = 180

TIME_TO_WAIT_AFTER_EACH_CLAP = 0
LOOP_DELAY = 1

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

def toggleLight(c):
    GPIO.output(c, True)
    sleep(1)
    GPIO.output(c, False)
    print("Light toggled")

def waitForClaps(threadName):
    global clap
    global wait
    global exitFlag
    global pin
    global waitingForMoreClaps

    print("Waiting for more claps")
    sleep(wait)
    if clap == 2:
        print("Two claps")
        #toggleLight(pin)
        toggleServo()
    # elif clap == 3:
    #     print "Three claps"
    elif clap == 4:
        exitFlag = True
    print("Claping Ended")
    clap = 0
    waitingForMoreClaps = False

def main():
    global clap
    global pin
    global clapInProgress
    global waitingForMoreClaps

    CHUNK = 8192
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 3000
    MAX_VALUE = 0
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    #output=True,
                    frames_per_buffer=CHUNK)
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pin, GPIO.OUT)
    try:
        print("Clap detection initialized")
        while True:
            #Get audio data
            try:
                data = stream.read(num_frames=CHUNK)
            except:
                data = array('b', [0])
                print("E")
            as_ints = array('h', data)
            MAX_VALUE = max(as_ints)
            #Evaluate audio data
            print(MAX_VALUE)
            if MAX_VALUE > THRESHOLD:
                #Clap detected
                if not clapInProgress:
                    #Clap started now
                    clapInProgress = True
                    print("Clap started")
                else:
                    print("Clap in progress")
            if not MAX_VALUE > THRESHOLD:
                #No clap detected
                if clapInProgress:
                    #Clap ended now
                    clapInProgress = False
                    clap += 1
                    print("Clap ended")
                    sleep(TIME_TO_WAIT_AFTER_EACH_CLAP)
            if clap == 1 and not waitingForMoreClaps:
                #First clap in a series of claps
                _thread.start_new_thread( waitForClaps, ("waitThread",) )
                waitingForMoreClaps = True
            if exitFlag:
                #Exit program
                sys.exit(0)
            #sleep(LOOP_DELAY)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting")
        stream.stop_stream()
        stream.close()
        p.terminate()
        #GPIO.cleanup()

def toggleServo():
    global currentlyOn
    if currentlyOn:
        currentlyOn = False
        ser.write(bytes([OFF_POSITION]))
        print("Now switched off")
    else:
        currentlyOn = True
        ser.write(bytes([ON_POSITION]))
        print("Now switched on")

if __name__ == "__main__":
    #Set up serial
    #try:
    serialport = getCOM()
    print("Establishing connection to: %s" % serialport)
    ser = serial.Serial(serialport, 9600, timeout=1)
    #except:
        #print("Error establishing connection to serial port. Exiting now")
        #exit()
    main()
