# alwakeupword
alwakeupword explicitly request the attention of a computer using a wake up word and also allows user to train model of their own wake up word.


## Installation
You can install alwakeupword from [PyPI](https://pypi.org/project/alwakeupword/):
```pip install alwakeupword```.

The alwakeupword supports Python 3.6 and above.


## Usage

### Step 1: ```AlWakeUpWordDataPreparation.py```
Following query on command line will help you to create a dataset for your own wake up word:
#### For recording wake up word
```
alwakeupword -c makeData -r recordAudio -rad "./audio" -n 200
```
Note: Here, -rad and -n are set to default values of ./audio in alwakeupword package path and 200 respectively.
#### For recording background audio
```
alwakeupword -c makeData -r recordBackgroundAudio -rbad "./backgroundAudio" -n 200
```
Note: Here, -rbad and -n are set to default values of ./backgroundAudio in alwakeupword package path and 200 respectively.

### Step 2: ```AlWakeUpWordDataPreprocessing.py```
Following query on command line will help you to preprocess the dataset you have created:
```
alwakeupword -c processData -rad "./audio" -rbad "./backgroundAudio"
```
Note: Here, -rad and -rbad are set to default values of ./audio and ./backgroundAudio in alwakeupword package path respectively.

### Step 3: ```AlWakeUpWordTrainer.py```
Following query on command line will help you to train the preprocess data and to create a model:
```
alwakeupword -c trainData -mp "./savedModel/model.h5"
```
Note: Here, -mp is set to default value of ./savedModel/model.h5 in alwakeupword package path.

### Step 4: ```AlWakeUpWordPrediction.py```
Following query on command line will help you to predict the accuracy of model and to detect if word is wake up word or not:
```
alwakeupword -c predictWord -mp "./savedModel/model.h5"
```
Note: Here, -mp is set to default value of ./savedModel/model.h5 in alwakeupword package path.

### Step 5: ```AlWakeUpWord.py```
Following example.py will show you how to use wakeUpWord() function from AlWakeUpWord.py file to your scripts:
```
"""
# example.py
from alwakeupword.AlWakeUpWord import wakeUpWord

modelPath = '{Path of your wake up  word model}'
while True:
    wakeUpWord(modelPath)
    print('Wake up word detected')
"""
"""
Output: When you run the file it will wait for your response. When you utter the wake up word then only 'Wake up word detected' will be printed in the console. 
"""
```
Note: Here, if you saved your model in the default path while training data then you don't have to give modelPath parameter to wakeUpWord() function as it is already set to default path.


## License
&copy; 2022 Alankar Singh

This repository is licensed under the MIT license. See LICENSE for details.