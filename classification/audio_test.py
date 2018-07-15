import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal


def record(duration = 2, fs =44100):
    print( "Recording Audio")
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float32')
    sd.wait()
    myrecording_filtered = signal.medfilt2d(myrecording)
    return myrecording_filtered

def save_recording(rec, outputfile, fs = 44100,  iswav = True):
    if iswav:
        wav.write(outputfile, fs, rec)
        return 
    np.save(outputfile, rec) 


# for i in range(10):
#     rec = record()
#     outfile = "data/hold/" + str(i) +".wav"
#     save_recording(rec, outfile)
