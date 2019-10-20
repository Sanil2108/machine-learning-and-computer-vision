import random

from game.bird.Bird import Bird

BIRD_COUNT = 10

class BirdManager(object):

    def __init__(self, game):
        self.game = game

        self.brain = None

        self.birds = None

        self.deleted_birds = []

    def check_if_out(self):
        for bird in self.birds:
            if bird.check_if_out():
                self.deleted_birds.append(bird)
                self.birds.remove(bird)
        
        if len(self.birds) == 0:
            new_birds = self.next_generation()
            self.game.game_over()
            self.game.game_reset({'new_birds': new_birds})

    def normalize_scores(self):
        sum_ = 0
        for i in range(len(self.deleted_birds)):
            sum_ += self.deleted_birds[i].score

        for i in range(len(self.deleted_birds)):
            self.deleted_birds[i].score /= sum_

    def get_random_birds_on_score(self, sorted_birds):
        r = random.randrange(0, 10**6) / 10**6
        i = 0
        while True:
            r -= sorted_birds[i].score
            if (r < 0):
                break
        return sorted_birds[i]

    def get_all_random_birds_on_score(self):
        self.normalize_scores()

        sorted_birds = sorted(self.deleted_birds, key = Bird.get_bird_score, reverse=True)

        new_birds = []
        while len(new_birds) < len(self.deleted_birds):
            bird = Bird(self.game)
            bird.initialize()
            bird.copy(self.get_random_birds_on_score(sorted_birds))
            new_birds.append(bird)

        return new_birds

    def next_generation(self):
        random_birds = self.get_all_random_birds_on_score()

        # Mutate all these birds
        for bird in random_birds:
            bird.mutate()

        return random_birds

    def initialize(self, params = {}):
        if ('new_birds' in params.keys()):
            self.birds = params['new_birds']
        else:
            self.birds = []

            for i in range(BIRD_COUNT):
                b = Bird(self.game)
                b.initialize()
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