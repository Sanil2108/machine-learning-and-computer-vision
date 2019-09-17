import pygame
import os

DEFAULT_X = 50
DEFAULT_Y = 300

DEFAULT_GRAVITY = 0.2
MAX_GRAVITY_SPEED = 16

DEFAULT_JUMP = 220
DEFAULT_JUMP_SPEED = 8

IMAGE_PATH = r'bird.png'
IMAGE_SCALE = 0.125

DRAW_BOUNDING_BOX = False

class Bird(object):
    
    def __init__(self):
        self.x = -1
        self.y = -1
        self.x_vel = 0
        self.y_vel = 0

        self.jump_distance_remaining = 0

    def initialize(self):
        self.x = DEFAULT_X
        self.y = DEFAULT_Y

        script_dir = os.path.dirname(__file__)

        self.image = pygame.image.load(os.path.join(script_dir, IMAGE_PATH))
        tempBoundingRect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(IMAGE_SCALE * tempBoundingRect.width), int(IMAGE_SCALE * tempBoundingRect.height)))

    def update(self):
        if (self.y_vel + DEFAULT_GRAVITY < MAX_GRAVITY_SPEED):
            self.y_vel += DEFAULT_GRAVITY

        if (self.jump_distance_remaining > 0):
            self.jump_distance_remaining -= DEFAULT_JUMP_SPEED
            self.y -= DEFAULT_JUMP_SPEED

        self.y += self.y_vel

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if (DRAW_BOUNDING_BOX):
            self.draw_bounding_box(screen)

    def jump(self):
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