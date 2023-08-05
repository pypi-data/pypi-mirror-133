import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from sklearn.metrics import confusion_matrix, classification_report
import os

cwd = os.path.dirname(os.path.realpath(__file__))
finalAudioPath = os.path.join(cwd + '\\finalAudio', 'audio.csv')


def trainData(modelPath=os.path.join(cwd + '\\savedModel', 'model.h5')):
    """
    This function will make a model of the data that has been preprocessed.
    """
    df = pd.read_pickle(finalAudioPath)
    x = df["feature"].values
    x = np.concatenate(x, axis=0).reshape(len(x), 40)
    y = np.array(df["classLabel"].tolist())
    y = to_categorical(y)
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2,
                                                    random_state=42)
    model = Sequential([
        Dense(256, input_shape=xTrain[0].shape),
        Activation('relu'),
        Dropout(0.5),
        Dense(256),
        Activation('relu'),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])
    print(model.summary())
    model.compile(
        loss="categorical_crossentropy",
        optimizer='adam',
        metrics=['accuracy']
    )
    print("Model Score: \n")
    model.fit(xTrain, yTrain, epochs=1000)
    model.save(modelPath)
    score = model.evaluate(xTest, yTest)
    print(score)
    print("Model Classification Report: \n")
    yPred = np.argmax(model.predict(xTest), axis=1)
    print(confusion_matrix(np.argmax(yTest, axis=1), yPred))
    print(classification_report(np.argmax(yTest, axis=1), yPred))
