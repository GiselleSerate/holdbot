import keras
from keras.models import Sequential, load_model
import librosa
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal


def record(duration = 2, fs =44100):
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float32')
    sd.wait()
    myrecording_filtered = signal.medfilt2d(myrecording)
    return myrecording_filtered

def get_feature(X, sample_rate=44100):
    if X.ndim > 1:
        X = X[:,0]
    X = X.T
    features = np.empty((0,40))

    # short term fourier transform
    stft = np.abs(librosa.stft(X))

    # mfcc
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    # chroma
   # chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    # melspectrogram
    #mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    # spectral contrast
   # contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
   # tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    ext_features = np.hstack([mfccs])
    features = np.vstack([features,ext_features])
    features = np.expand_dims(features, axis=2)
    return features

class SmartClassifier:
    def __init__(self):
        self.model = load_model("classify_nn.h5.h5")
    def classify(self, rec, sample_rate= 44100):
        features = get_feature(rec, sample_rate)
        pred_class = np.argmax(self.model.predict(features))
        if pred_class < 2:
            return True
        else:
            return False
