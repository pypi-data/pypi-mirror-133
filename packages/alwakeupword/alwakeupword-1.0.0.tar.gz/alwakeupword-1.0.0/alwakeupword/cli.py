import argparse
from alwakeupword.AlWakeUpWordDataPreparation import recordAudio, recordBackgroundAudio
from alwakeupword.AlWakeUpWordDataPreprocessing import preprocessData
from alwakeupword.AlWakeUpWordTrainer import trainData
from alwakeupword.AlWakeUpWordPrediction import predictWord
import os


def main():
    cwd = os.path.dirname(os.path.realpath(__file__))
    backgroundAudioPath = os.path.join(cwd, 'backgroundAudio')
    audioPath = os.path.join(cwd, 'audio')
    modelPath = os.path.join(cwd + '\\savedModel', 'model.h5')
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store', type=str, default=None,
                        help='Use one command from either makeData or '
                        'processData or trainData or predictWord')
    parser.add_argument('-r', action='store', type=str, default='recordAudio',
                        help='Use one command from either recordAudio or '
                        'recordBackgroundAudio')
    parser.add_argument('-rad', action='store', type=str, default=audioPath,
                        help='Directory path for audio files')
    parser.add_argument('-rbad', action='store', type=str,
                        default=backgroundAudioPath, help='Directory path for '
                        'background audio files')
    parser.add_argument('-n', action='store', nargs='+', type=int,
                        default=200, help='No of audio files to be generated')
    parser.add_argument('-mp', action='store', type=str, default=modelPath,
                        help='Path of model with model name (e.g. model.h5)')
    args = parser.parse_args()
    command = args.c
    if command == 'makeData':
        recordCommand = args.r
        if recordCommand == 'recordAudio':
            directory = args.rad
            if type(args.n) == int:
                args.n = [args.n]
            iterations = tuple(args.n)
            input("To start recording Wake Up Word press Enter: ")
            recordAudio(directory, iterations)
        elif recordCommand == 'recordBackgroundAudio':
            directory = args.rbad
            iterations = args.n
            recordBackgroundAudio(directory, iterations)
    elif command == 'processData':
        audioDirectory = args.rad
        backgroundAudioDirectory = args.rbad
        preprocessData(audioDirectory, backgroundAudioDirectory)
    elif command == 'trainData':
        modelFilePath = args.mp
        trainData(modelFilePath)
    elif command == 'predictWord':
        modelFilePath = args.mp
        predictWord(modelFilePath)


if __name__ == "__main__":
    main()