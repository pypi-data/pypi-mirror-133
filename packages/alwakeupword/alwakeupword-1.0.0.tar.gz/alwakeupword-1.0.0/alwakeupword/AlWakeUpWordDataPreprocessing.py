import os
import librosa
import librosa.display
import numpy as np
import pandas as pd
import os

cwd = os.path.dirname(os.path.realpath(__file__))


def preprocessData(audioPath=os.path.join(cwd, 'audio'),
                   backgroundAudioPath=os.path.join(cwd, 'backgroundAudio')):
    """
    This function will create audio.csv file which will be used to create
    model while training

    Parameters
    ----------
    audioPath: str, default=./audio
        Path of recorded audio files.

    backgroundAudioPath: str, default=./audio
        Path of recorded background audio files.
    """
    allData = []
    finalAudioPath = os.path.join(cwd + '\\finalAudio', 'audio.csv')
    dataPath = {
        0: [os.path.join(backgroundAudioPath, filePath)
            for filePath in os.listdir(backgroundAudioPath)],
        1: [os.path.join(audioPath, filePath)
            for filePath in os.listdir(audioPath)]
    }
    for classLabel, listFiles in dataPath.items():
        for audioFile in listFiles:
            audio, sampleRate = librosa.load(audioFile)
            mfcc = librosa.feature.mfcc(y=audio, sr=sampleRate, n_mfcc=40)
            mfccProcessed = np.mean(mfcc.T, axis=0)
            allData.append([mfccProcessed, classLabel])
        print(f"Info: Succesfully Preprocessed Class Label {classLabel}")
    df = pd.DataFrame(allData, columns=["feature", "classLabel"])
    df.to_pickle(finalAudioPath)
