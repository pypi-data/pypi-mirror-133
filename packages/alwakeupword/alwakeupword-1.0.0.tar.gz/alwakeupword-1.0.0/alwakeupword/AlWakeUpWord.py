from winsound import PlaySound, SND_FILENAME
import sounddevice as sd
import librosa
import sys
import numpy as np
from tensorflow.keras.models import load_model
import os

cwd = os.path.dirname(os.path.realpath(__file__))
notification = os.path.join(cwd, 'notification.wav')
fs = 22050
seconds = 2


def callback(indata, outdata, frames, time, status):
    """
    This function obtains audio data from the input channels.
    """
    if status:
        print(status)
    return indata


def getAudioInputStream(callback):
    """
    This function is returns stream for simultaneous input and output.
    """
    stream = sd.Stream(
        samplerate=fs,
        channels=1,
        callback=callback
    )
    return stream


def detectTriggerWordSpectrum(model, y):
    """
    This function is used to predict the location of the trigger word.

    Parameters
    ----------
    x:
        Spectrum of input audio

    Returns
    -------
        True if wake up word detected as false
    """
    prediction = model.predict(np.expand_dims(y, axis=0))
    if prediction[:, 1] > 0.96:
        return True
    else:
        return False


def wakeUpWord(modelPath=os.path.join(cwd + '\\savedModel', 'model.h5')):
    """
    This function is used to detect wake up word
    """
    run = True
    model = load_model(modelPath)
    stream = getAudioInputStream(callback)
    stream.start()
    try:
        while run:
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
            sd.wait()
            mfcc = librosa.feature.mfcc(y=myrecording.ravel(), sr=fs,
                                        n_mfcc=40)
            mfccProcessed = np.mean(mfcc.T, axis=0)
            isTrigger = detectTriggerWordSpectrum(model, mfccProcessed)
            if isTrigger:
                sys.stdout.write('Activated: ')
                run = False
                PlaySound(notification, SND_FILENAME)
                stream.stop()
                stream.close()
                break
    except (KeyboardInterrupt, SystemExit):
        stream.stop()
        stream.close()
        run = False
