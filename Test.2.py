#!/usr/bin/env python3
import pyaudio
#import wave

import threading
import array

CHUNK = 512
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 30
#WAVE_OUTPUT_FILENAME = "pyaudio-output.wav"

data = None
done = False

def analyze():
    while not done:
        dataAsInts = array.array('h', data)
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

try:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
    #frames.append(data) # 2 bytes(16 bits) per channel
except KeyboardInterrupt:
    done = True


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