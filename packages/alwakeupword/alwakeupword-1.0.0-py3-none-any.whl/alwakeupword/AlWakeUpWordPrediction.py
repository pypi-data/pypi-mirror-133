import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from tensorflow.keras.models import load_model
import os

cwd = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(cwd, 'prediction.wav')


def predictWord(modelPath=os.path.join(cwd + '\\savedModel', 'model.h5')):
    """
    This function will predict if the word is wake up word or not.
    """
    fs = 44100
    seconds = 2
    model = load_model(modelPath)
    while True:
        print("Prediction Started: ")
        print("Say Now: ")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write(filename, fs, myrecording)
        audio, sample_rate = librosa.load(filename)
        mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        prediction = model.predict(np.expand_dims(mfcc_processed, axis=0))
        if prediction[:, 1] > 0.99:
            print("Wake Word Detected")
            print("Confidence:", prediction[:, 1])
            break
        else:
            print("Wake Word not Detected")
            print("Confidence:", prediction[:, 0])
