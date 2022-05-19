from typing import List
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Conv1D
from statistics import mean

from snake_ai_function import SnakeAI

class CustomTrainer():
    def __init__(self) -> None:
        self.avgAcc = 0
        pass
    
    def train(self, data_path: str, save_path:str, start_activation, end_acttivation, config: List[List]) -> None:
        data = pd.read_csv(data_path)

        # remove special character
        data.columns = data.columns.str.replace(' ', '')
        
        X = pd.concat( [data['foodDiffX'], data['foodDiffY'], data['up_collision'], data['down_collision'], data['left_collision'], data['right_collision'], data['direction']], axis=1)
        Y = pd.get_dummies(data['action'])
        
        model = Sequential()
        # add first layer
        model.add(Dense(7, input_dim=7, activation=start_activation))
        # model.add(Conv1D(7, 4, input_shape=(20, 1,7), activation='relu'))

        for layer in config:
            model.add(Dense(int(layer[0]), activation=layer[1]))
    
        # final layer
        model.add(Dense(4, activation=end_acttivation))

        # combine the Keras model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the keras model on the dataset
        hist = model.fit(X,Y, epochs=150, batch_size=20)   
        

        self.avgAcc = mean(hist.history['accuracy'])
        
        model.save(save_path)
        self.save_path = save_path
        return save_path
    
    def getAverageAccuracy(self):
        return self.avgAcc

    def run_evaluation(self, path = None, eval_count = 5):
        if path == None:
            path = self.save_path
        ai = SnakeAI(path)
        ai.ai_play(eval_count)
        return ai.get_average()
