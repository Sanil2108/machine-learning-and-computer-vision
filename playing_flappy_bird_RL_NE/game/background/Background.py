import pygame
import os

IMAGE_PATH = r'background.jpg'

class Background(object):
    
    def __init__(self):
        pass

    def initialize(self):
        script_dir = os.path.dirname(__file__)

        self.image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (0, 0))