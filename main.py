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
flag = 0
pin = 24
exitFlag = False

ports = list(serial.tools.list_ports.comports())    #List of serial ports (loaded automatically)

currentlyOn = False

ON_POSITION = 0
OFF_POSITION = 180

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
        return ports[0].device

    #Display all available ports if there are more than one available
    print("Available Ports: ")
    for port in ports:
        print(port)
    return input("Enter Xbee Serialport: ")

def toggleLight(c):
	GPIO.output(c,True)
	sleep(1)
	GPIO.output(c,False)
	print("Light toggled")

def waitForClaps(threadName):
	global clap
	global flag
	global wait
	global exitFlag
	global pin
	print("Waiting for more claps")
	sleep(wait)
	if clap == 2:
		print("Two claps")
		#toggleLight(pin)
		toggleServo()
	# elif clap == 3:
	# 	print "Three claps"
	elif clap == 4:
		exitFlag = True
	print("Claping Ended")
	clap = 0
	flag = 0

def main():
	global clap
	global flag
	global pin

	chunk = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	threshold = 15000
	max_value = 0
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS, 
					rate=RATE, 
					input=True,
					output=True,
					frames_per_buffer=chunk)
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setup(pin, GPIO.OUT)

	#Set up serial
	try:
		serialport = getCOM()
		print("Establishing connection to: %s" % serialport)
		ser = serial.Serial(serialport, 9600, timeout=1)
	except:
		print("Error establishing connection to serial port. Exiting now")
		exit()

	try:
		print("Clap detection initialized")
		while True:
			data = stream.read(chunk)
			as_ints = array('h', data)
			max_value = max(as_ints)
			if max_value > threshold:
				clap += 1
				print("Clapped")
			if clap == 1 and flag == 0:
				_thread.start_new_thread( waitForClaps, ("waitThread",) )
				flag = 1
			if exitFlag:
				sys.exit(0)
	except (KeyboardInterrupt, SystemExit):
		print("\rExiting")
		stream.stop_stream()
		stream.close()
		p.terminate()
		#GPIO.cleanup()

def toggleServo():
	if currentlyOn:
		currentlyOn = False
		ser.write(bytes[OFF_POSITION])
	else:
		currentlyOn = True
		ser.write(bytes[ON_POSITION])

if __name__ == "__main__":
	main()
