from Pipe import Pipe
import random

PIPE_GENERATION_RANGE = {
    'MIN': 50,
    'MAX': 1000
}
PIPE_PROBABILITY = 0.1

PIPE_SPEED = -10

class PipeManager(object):

    def __init__(self, game):
        self.all_pipes = []
        self.game = game
    
    def initialize(self):
        self.last_pipe_generated = -1

    def update_all_pipes(self):
        self.last_pipe_generated += 1

        for pipe in self.all_pipes:
            if (pipe.get_x() + pipe.get_bounding_box().width < 0):
                self.all_pipes.remove(pipe)
            else:
                pipe.update()

        if (self.last_pipe_generated is -1 or self.last_pipe_generated > PIPE_GENERATION_RANGE['MAX']):
            self.create_pipe()
        elif (self.last_pipe_generated > PIPE_GENERATION_RANGE['MIN']):
            random_num = random.randint(0, 10 ** 8) / float(10 ** 8)
            if (random_num < PIPE_PROBABILITY):
                self.create_pipe()

    def create_pipe(self):
        pipe = Pipe(self.game.get_dimensions()[0] + 100, self.game)
        pipe.initialize()
        self.last_pipe_generated = 0
        self.all_pipes.append(pipe)

    def draw_all_pipes(self, screen):
        for pipe in self.all_pipes:
            pipe.draw(screen)