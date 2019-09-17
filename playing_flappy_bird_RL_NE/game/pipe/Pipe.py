import pygame
import os

IMAGE_PATH = 'pipe.png'

PIPE_SPEED = -5

DRAW_BOUNDING_BOX = False

class Pipe(object):
    def __init__(self, x, game, gap, bottom_pipe_y):
        self.x = x
        self.y = -1

        self.game = game

        self.gap = gap
        self.bottom_pipe_end_y = bottom_pipe_y

        self.crossed = False

    def initialize(self):
        script_dir = os.path.dirname(__file__)

        self.top_image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))
        self.top_image = pygame.transform.rotate(self.top_image, 180)
        self.top_image = pygame.transform.scale(self.top_image, (self.top_image.get_rect().width, int(self.top_image.get_rect().height * 1.4)))
        
        self.bottom_image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))
        self.bottom_image = pygame.transform.scale(self.bottom_image, (self.bottom_image.get_rect().width, int(self.bottom_image.get_rect().height * 1.4)))

        self.top_pipe_y = self.bottom_pipe_end_y - self.gap - self.top_image.get_rect().height
        self.bottom_pipe_y = self.bottom_pipe_end_y

    def draw(self, screen):
        screen.blit(self.top_image, (self.x, self.top_pipe_y))
        screen.blit(self.bottom_image, (self.x, self.bottom_pipe_y))

        if DRAW_BOUNDING_BOX:
            self.draw_bounding_box(screen)

    def update(self):
        self.x += PIPE_SPEED

    def get_x(self):
        return self.x

    def draw_bounding_box(self, screen):
        bounding_box = self.get_bounding_box()[0]
        rect = pygame.Rect(bounding_box['x'], bounding_box['y'], bounding_box['width'], bounding_box['height'])
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)

        bounding_box = self.get_bounding_box()[1]
        rect = pygame.Rect(bounding_box['x'], bounding_box['y'], bounding_box['width'], bounding_box['height'])
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)

    def get_bounding_box(self):
        return [{
            'x': self.x,
            'y': self.top_pipe_y,
            'height': self.top_image.get_rect().height,
            'width': self.top_image.get_rect().width,
        },{
            'x': self.x,
            'y': self.bottom_pipe_y,
            'height': self.bottom_image.get_rect().height,
            'width': self.bottom_image.get_rect().width,
        }]