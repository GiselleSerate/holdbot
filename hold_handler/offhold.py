import sounddevice as sd
import soundfile as sf
import os

def alert_offhold():
    audiofile = os.path.join(os.path.dirname(__file__), 'OFFHOLD.wav')
    X, _ = sf.read(audiofile, dtype='float64')
    sd.play(X)
    sd.wait()
