import pygame
import os
from game.bird.BirdBrain import BirdBrain
import numpy as np

DEFAULT_X = 50
DEFAULT_Y = 300

DEFAULT_GRAVITY = 0.2
MAX_GRAVITY_SPEED = 16

DEFAULT_JUMP = 220
DEFAULT_JUMP_SPEED = 8

IMAGE_PATH = r'bird.png'
IMAGE_SCALE = 0.125

DRAW_BOUNDING_BOX = False


script_dir = os.path.dirname(__file__)
IMAGE = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))
tempBoundingRect = IMAGE.get_rect()
IMAGE = pygame.transform.scale(IMAGE, (int(IMAGE_SCALE * tempBoundingRect.width), int(IMAGE_SCALE * tempBoundingRect.height)))

def check_point_in_rect(point, rect):
    if (point[0] > rect['x'] and point[0] < rect['x'] + rect['width'] and point[1] < rect['y'] + rect['height'] and point[1] > rect['y']) :
        return True

def compare_rect_intersection(rect1, rect2):
    if (check_point_in_rect([rect1['x'], rect1['y']], rect2) or check_point_in_rect([rect1['x'] + rect1['width'], rect1['y']], rect2) or
        check_point_in_rect([rect1['x'] + rect1['width'], rect1['y'] + rect1['height']], rect2) or check_point_in_rect([rect1['x'], rect1['y'] + rect1['height']], rect2)):
        return True

class Bird(object):
    
    def __init__(self, game):
        self.x = -1
        self.y = -1
        self.x_vel = 0
        self.y_vel = 0

        self.score = 0

        self.jump_distance_remaining = 0

        self.game = game

        self.brain = None

        self.score = 0

    def copy(self, bird):
        self.brain = bird.brain

    def initialize(self):
        self.x = DEFAULT_X
        self.y = DEFAULT_Y

        self.image = IMAGE
        self.image.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)

        # tempBoundingRect = self.image.get_rect()
        # self.image = pygame.transform.scale(self.image, (int(IMAGE_SCALE * tempBoundingRect.width), int(IMAGE_SCALE * tempBoundingRect.height)))

        self.brain = BirdBrain(self.game)

    def check_pipe_cleared(self):
        bird_bounding_rect = self.get_bounding_box()[0]

        for i in range(len(self.game.pipeManager.all_pipes)):
            pipe = self.game.pipeManager.all_pipes[i]
            if (pipe.crossed == False and pipe.get_bounding_box()[0]['x'] < bird_bounding_rect['x']):
                pipe.crossed = True
                return True
        return False

    def check_if_out(self):
        bird_bounding_rect = self.get_bounding_box()[0]

        screen_dimensions = self.game.get_dimensions()

        if (
            (bird_bounding_rect['y'] + bird_bounding_rect['height'] > screen_dimensions[1]) or
            (bird_bounding_rect['y'] < bird_bounding_rect['height'])
        ):
            return True

        for i in range(len(self.game.pipeManager.all_pipes)):
            pipe = self.game.pipeManager.all_pipes[i]
            if (compare_rect_intersection(bird_bounding_rect, pipe.get_bounding_box()[0]) or 
            compare_rect_intersection(bird_bounding_rect, pipe.get_bounding_box()[1])):
                return True

        return False
    
    @staticmethod
    def get_bird_state_count():
        return 1

    @staticmethod
    def get_bird_score(bird):
        return bird.score ** 2

    def get_bird_state(self):
        return [self.y]

    def decide(self):
        params = np.array([self.game.get_game_state() + self.get_bird_state()])
        prediction = self.brain.predict(params)
        if (prediction < 0.5):
            self.jump()

    def update(self):
        if (self.y_vel + DEFAULT_GRAVITY < MAX_GRAVITY_SPEED):
            self.y_vel += DEFAULT_GRAVITY

        if (self.jump_distance_remaining > 0):
            self.jump_distance_remaining -= DEFAULT_JUMP_SPEED
            self.y -= DEFAULT_JUMP_SPEED

        self.y += self.y_vel

        self.score += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if (DRAW_BOUNDING_BOX):
            self.draw_bounding_box(screen)

    def jump(self):
        if (self.jump_distance_remaining <= 0):
            self.jump_distance_remaining = DEFAULT_JUMP
            self.y_vel = 0

    def draw_bounding_box(self, screen):
        bounding_box = self.get_bounding_box()[0]
        rect = pygame.Rect(bounding_box['x'], bounding_box['y'], bounding_box['width'], bounding_box['height'])
        pygame.draw.rect(screen, (0, 0, 255), rect, 2)

    def get_bounding_box(self):
        return [
            {
                'x': self.x,
                'y': self.y,
                'height': self.image.get_rect().height,
                'width': self.image.get_rect().width,
            }
        ]

    def mutate(self):
        self.brain.mutate()

    def __str__(self):
        print('{}'.format(self.score))