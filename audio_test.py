import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import scipy.signal as signal

fs=44100
duration = 5  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
print( "Recording Audio")
sd.wait()
print("Audio recording complete , Play Audio")
sd.play(myrecording, fs)
sd.wait()
print("Play Audio Complete")

print(myrecording)
plt.plot(myrecording)
plt.show()

filtered = signal.medfilt2d(myrecording)
plt.plot(filtered)
plt.show()


def record(duration = 1.0, fs =44100):
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    return myrecording

