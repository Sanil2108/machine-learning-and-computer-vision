from game.bird.Bird import Bird

BIRD_COUNT = 3

class BirdManager(object):

    def __init__(self, game):
        self.game = game

        self.brain = None

        self.birds = None

    def check_if_out(self):
        for bird in self.birds:
            if bird.check_if_out():
                self.birds.remove(bird)

    def initialize(self):
        self.birds = []
        for i in range(BIRD_COUNT):
            b = Bird(self.game)
            b.initialize()
            self.birds.append(b)

    def update_all_birds(self):
        for bird in self.birds:
            bird.update()

        for bird in self.birds:
            bird.decide()
        
        self.check_if_out()

    def draw_all_birds(self, screen):
        for bird in self.birds:
            bird.draw(screen)