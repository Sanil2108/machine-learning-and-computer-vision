from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.initializers import RandomNormal

from keras.utils import to_categorical

import numpy as np

import random

import constants

NUMBER_OF_FRAMES_BEFORE_TRAIN = 300

# For random decision making
RANDOM_X_INTERCEPT = 100000
RANDOM_Y_INTERCEPT = 1

# TODO: Ignored until flow is done
class NeuralNetworkPlayer(object):
    def __init__(self, input_size):
        self.model = Sequential()

        self.model.add(Dense(10, input_shape = (input_size, ), activation = 'relu', kernel_initializer = RandomNormal(mean = 0, stddev = 2), bias_initializer = RandomNormal(mean = 0, stddev = 2)))
        self.model.add(Dense(10, activation = 'relu', bias_initializer = RandomNormal(mean = 0, stddev = 2),kernel_initializer = RandomNormal(mean = 0, stddev = 2)))
        self.model.add(Dense(10, activation = 'relu', bias_initializer = RandomNormal(mean = 0, stddev = 2),kernel_initializer = RandomNormal(mean = 0, stddev = 2)))
        self.model.add(Dense(2, activation = 'softmax', bias_initializer = RandomNormal(mean = 0, stddev = 2),kernel_initializer = RandomNormal(mean = 0, stddev = 2)))

        self.model.compile(Adam(lr=0.1), loss='categorical_crossentropy', metrics=['accuracy'])

        print('Creating model')
        print(self.model.summary())

        self.data_not_trained = []
        self.output_not_trained = []

        self.frame_counter = 0

        self.history = None

    def update_data(self, game_response, game_state, action):
        # print(game_state, end = ' ')
        if (game_response['action_successful']):
            self.data_not_trained.append(
                game_state
            )
            if (action == constants.ACTION_DO_NOTHING):
                output = 0
            else:
                output = 1
            self.output_not_trained.append(to_categorical(output, num_classes=2))

    def random_decision_probability(self):
        # return 0.02
        slope = -RANDOM_Y_INTERCEPT / RANDOM_X_INTERCEPT
        c = RANDOM_Y_INTERCEPT
        return self.frame_counter * slope + c

    def get_random_decision(self):
        temp = random.randint(0, 1)
        if (temp < 0.5):
            return 0
        return 1

    def update(self):
        self.frame_counter += 1
        if (self.frame_counter % NUMBER_OF_FRAMES_BEFORE_TRAIN == 0):
            self.fit_with_new_data(self.data_not_trained, self.output_not_trained)
            self.data_not_trained = []
            self.output_not_trained = []

    def get_action(self, game_state):
        random_decision_prob = self.random_decision_probability()
        random_number = random.randint(0, 1)
        prediction = -1
        if (random_decision_prob > random_number):
            prediction = self.get_random_decision()
        else:
            prediction = self.model.predict(np.array([game_state]))[0][0]
        response = {}
        if (prediction < 0.5):
            response['action'] = constants.ACTION_DO_NOTHING
        else:
            response['action'] = constants.ACTION_JUMP

        return response

    def fit_with_new_data(self, x_value, y_value):
        if (len(x_value) == 0):
            print('No data.')
            return
        self.history = self.model.fit(x = np.array(x_value), y = np.array(y_value), epochs = 20, verbose = 1)

    def get_history(self):
        return self.history

    def get_initialization_params(self):
        return {'birdCount': 1, 'jumpEnabled': False}