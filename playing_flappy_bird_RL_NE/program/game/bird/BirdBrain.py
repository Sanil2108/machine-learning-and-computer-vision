import keras
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

class BirdBrain(object):
    
    def __init__(self, game):
        self.actualBrain = Sequential()
        self.actualBrain.add(Dense(10, input_shape = (game.get_number_of_items_in_state(), ), activation='relu'))
        self.actualBrain.add(Dense(4, activation='relu'))
        self.actualBrain.add(Dense(1, activation='sigmoid'))
        self.actualBrain.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.1), metrics=['accuracy'])

    def mutate(self):
        # Select a random weight. Change the weight by some arbitrary amount
        pass

    def predict(self, params):
        prediction = self.actualBrain.predict(params)
        return prediction