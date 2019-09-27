from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np

import constants

NUMBER_OF_FRAMES_BEFORE_TRAIN = 100

class NeuralNetworkPlayer(object):
    def __init__(self, input_size):
        self.model = Sequential()

        self.model.add(Dense(10, input_shape = (input_size, ), activation = 'relu'))
        self.model.add(Dense(10, activation = 'relu'))
        self.model.add(Dense(10, activation = 'relu'))
        self.model.add(Dense(1, activation = 'softmax'))

        self.model.compile(Adam(lr=0.1), loss='categorical_crossentropy', metrics=['accuracy'])

        print('Creating model')
        print(self.model.summary())

        self.data_not_trained = []
        self.output_not_trained = []

        self.frame_counter = 0

        self.history = None

    def update_data(self, game_response, game_state, action):
        print(game_state, end = ' ')
        self.data_not_trained.append(
            game_state
        )
        output = [0]
        if (game_response['action_successful']):
            output = [1]
        self.output_not_trained.append([output])
        print(output)

    def update(self):
        self.frame_counter += 1
        if (self.frame_counter >= NUMBER_OF_FRAMES_BEFORE_TRAIN):
            self.frame_counter = 0
            self.fit_with_new_data(self.data_not_trained, self.output_not_trained)
            self.data_not_trained = []
            self.output_not_trained = []

    def get_action(self, game_state):
        return {'action' : constants.ACTION_JUMP}

    def fit_with_new_data(self, x_value, y_value):
        self.history = self.model.fit(x = np.array(x_value), y = np.array(y_value), epochs = 20, verbose = 1)

    def get_history(self):
        return self.history

    def predict(self, x_value):
        return self.model.predict(x_value, verbose = 1)