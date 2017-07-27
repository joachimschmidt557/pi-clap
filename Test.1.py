#!/usr/bin/env python3
import pyaudio
import wave
from array import array

CHUNK = 512
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "pyaudio-output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

try:
    print("Clap detection initialized")
    while True:
		#Get audio data
        data = stream.read(num_frames=CHUNK)
        as_ints = array('h', data)
        MAX_VALUE = max(as_ints)
        #Evaluate audio data
        print(MAX_VALUE)
except (KeyboardInterrupt, SystemExit):
	print("Exiting")
	stream.stop_stream()
	stream.close()
	p.terminate()
	#GPIO.cleanup()

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #data = stream.read(CHUNK)
    #frames.append(data) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()