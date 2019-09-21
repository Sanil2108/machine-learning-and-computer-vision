from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class NeuralNetworkPlayer(object):
    def __init__(self, input_size):
        self.model = Sequential()

        self.model.add(Dense(10, input_shape = (input_size, ), activation = 'relu'))
        self.model.add(Dense(10, activation = 'relu'))
        self.model.add(Dense(10, activation = 'relu'))
        self.model.add(Dense(1, activation = 'softmax'))

        self.model.compile(Adam(learning_rate = 0.1))