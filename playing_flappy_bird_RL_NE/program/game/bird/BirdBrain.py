import keras
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

class BirdBrain(object):
    
    def __init__(self):
        self.actualBrain = Sequential()
        self.actualBrain.add(Dense(10, input_shape = (4, ), activation='relu'))
        self.actualBrain.add(Dense(1, activation='sigmoid'))
        self.actualBrain.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.1), metrics=['accuracy'])

    def mutate(self):
        pass

    def predict(self, params):
        prediction = self.actualBrain.predict(params)
        print(prediction)
        return prediction