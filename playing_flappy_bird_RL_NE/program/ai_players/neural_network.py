from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import constants

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

        self.history = None

    def update_data(self, action_successful, action, inputs):
        if (action_successful):
            pass

    def update(self):
        pass

    def get_action(self):
        return {'action' : constants.ACTION_JUMP}

    def fit_with_new_data(self, x_value, y_value):
        self.history = self.model.fit(x = x_value, y = y_value, epochs = 20, verbose = 1)

    def get_history(self):
        return self.history

    def predict(self, x_value):
        return self.model.predict(x_value, verbose = 1)