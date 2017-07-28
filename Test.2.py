#!/usr/bin/env python3
import pyaudio
#import wave

import threading
from array import array
from time import sleep

CHUNK = 512
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 30
#WAVE_OUTPUT_FILENAME = "pyaudio-output.wav"

data = array('b', [0])
done = False

lock = threading.Lock()

def analyze():
    global done
    global data
    
    while not done:
        with lock:
            dataAsInts = array('h', data)
            maxValue = max(dataAsInts)
            print(maxValue)


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

thrd = threading.Thread(target=analyze)
thrd.start()

try:
    while not done:
        with lock
            data = stream.read(CHUNK)
    #frames.append(data) # 2 bytes(16 bits) per channel
except KeyboardInterrupt:
    done = True

thrd.join()

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#wf.setnchannels(CHANNELS)
#wf.setsampwidth(p.get_sample_size(FORMAT))
#wf.setframerate(RATE)
#wf.writeframes(b''.join(frames))
#wf.close()
