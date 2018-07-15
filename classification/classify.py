import numpy as np
import keras
from keras.models import Sequential, load_model
import h5py 
import librosa
import numpy as np
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import scipy.signal as signal

from audio_test import *

def get_feature(X, sample_rate=44100):
    if X.ndim > 1:
        X = X[:,0]
    X = X.T
    features = np.empty((0,193))

    # short term fourier transform
    stft = np.abs(librosa.stft(X))

    # mfcc
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    # chroma
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    # melspectrogram
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    # spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    features = np.vstack([features,ext_features])
    features = np.expand_dims(features, axis=2)
    return features


def classify(rec, sample_rate = 44110):
    features = get_feature(rec, sample_rate)
    classifier = load_model("hold_classifier.h5")
    print(classifier.predict(features))
    return np.argmax(classifier.predict(features))
    


rec = record()
print(classify(rec))