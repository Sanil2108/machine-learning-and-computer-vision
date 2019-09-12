import pygame
from bird.Bird import Bird
from pipe.PipeManager import PipeManager
from managers.GameManager import GameManager

BG_COLOR = (255, 255, 255)
SCREEN_SIZE = (360, 720)

JUMP_KEY = 32

class Game(object):
    def __init__(self):
        self.bird = None
        self.pipeManager = None
        self.gameRunning = None
        
    def initialize(self):
        self.gameRunning = True

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(BG_COLOR)

        self.bird = Bird()
        self.pipeManager = PipeManager(self)

        self.gameManager = GameManager(self)

        self.bird.initialize()
        self.pipeManager.initialize()

        self.clock = pygame.time.Clock()

        self.update()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY:
                    self.bird.jump()


    def update(self):
        font = pygame.font.Font(None, 30)
        while self.gameRunning:
            self.screen.fill(BG_COLOR)

            self.handle_events()

            self.bird.update()
            self.pipeManager.update_all_pipes()

            self.draw()

            pygame.display.flip()

            if (self.gameManager.check_game_over()) :
                print("Game over")
                self.gameRunning = False

            fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('red'))
            self.screen.blit(fps, (50, 50))
            # print(int(self.clock.get_fps()))
            self.clock.tick(60)

    def draw(self):
        self.bird.draw(self.screen)
        self.pipeManager.draw_all_pipes(self.screen)

    def get_dimensions(self):
        return SCREEN_SIZE

game = Game()
game.initialize()