import sounddevice as sd
import soundfile as sf

def alert_offhold():
    X, _ = sf.read('OFFHOLD.wav', dtype='float64')
    sd.play(X)
    sd.wait()

