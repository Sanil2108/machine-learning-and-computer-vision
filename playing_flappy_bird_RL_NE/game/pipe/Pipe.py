import pygame
import os

IMAGE_PATH = 'pipe.png'

PIPE_SPEED = -10

class Pipe(object):
    def __init__(self, x, game):
        self.x = x
        self.y = -1

        self.game = game

    def initialize(self):
        script_dir = os.path.dirname(__file__)

        self.top_image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))
        self.top_image = pygame.transform.rotate(self.top_image, 180)
        
        self.bottom_image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))

    def draw(self, screen):
        screen.blit(self.top_image, (self.x, 0))
        screen.blit(self.bottom_image, (self.x, self.game.get_dimensions()[1] - self.bottom_image.get_rect().height))

    def update(self):
        self.x += PIPE_SPEED

    def get_x(self):
        return self.x

    def get_bounding_box(self):
        return self.top_image.get_rect()