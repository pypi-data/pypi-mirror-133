import sounddevice as sd
from scipy.io.wavfile import write
import os

cwd = os.path.dirname(os.path.realpath(__file__))


def recordAudio(savePath=os.path.join(cwd, 'audio'), nTimes=200):
    """
    This function will run `nTimes`

    Parameters
    ----------
    nTimes: int, default=200
        The function will run nTimes default is set to 200.

    savePath: str, default=./audio
        Where to save the wav file which is generated in every iteration.
    """
    fs = 44100
    seconds = 2
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    if type(nTimes) == int:
        nTimes = (nTimes,)
    if len(nTimes) >= 2:
        for i in range(nTimes[0], nTimes[1]):
            write(savePath + '\\' + str(i) + ".wav", fs, myrecording)
    else:
        for i in range(nTimes[0]):
            write(savePath + '\\' + str(i) + ".wav", fs, myrecording)


def recordBackgroundAudio(savePath=os.path.join(cwd, 'backgroundAudio'),
                          nTimes=200):
    """
    This function will run automatically `nTimes` and record your background
    sounds so you can make some keybaord typing sound and saying something
    gibberish.
    Note: Keep in mind that you don't have to say the wake word this time.

    Parameters
    ----------
    nTimes: int, default=200
        The function will run nTimes default is set to 200.

    savePath: str, default=./backgroundAudio
        Where to save the wav file which is generated in every iteration.
        Note: DON'T set it to the same directory where you have saved the wake
              word or it will overwrite the files.
    """
    for i in range(nTimes):
        fs = 44100
        seconds = 2
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write(savePath + '\\' + str(i) + ".wav", fs, myrecording)
        print(f"Currently on {i+1}/{nTimes}")
