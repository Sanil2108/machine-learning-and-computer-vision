import pygame
from bird.Bird import Bird
from background.Background import Background
from pipe.PipeManager import PipeManager

from managers.GameManager import GameManager
from managers.StatManager import StatManager

BG_COLOR = (255, 255, 255)
SCREEN_SIZE = (360, 720)

JUMP_KEY = 32
EXIT_KEY = 101
INCREASE_FPS_KEY = 270
DECREASE_FPS_KEY = 269

DEFAULT_FPS = 60

class Game(object):
    def __init__(self):
        self.bird = None
        self.background = None
        self.pipeManager = None

        self.gameRunning = None

        self.statManager = StatManager(self)

        self.fps_counter = DEFAULT_FPS
        
    def initialize(self):
        self.gameRunning = True

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(BG_COLOR)

        self.bird = Bird()
        self.pipeManager = PipeManager(self)
        self.background = Background()

        self.gameManager = GameManager(self)

        self.bird.initialize()
        self.pipeManager.initialize()
        self.background.initialize()

        self.clock = pygame.time.Clock()

        self.score = 0
        self.fps = -1

        self.update()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY:
                    self.bird.jump()
                if (event.key == EXIT_KEY):
                    exit()
                if (event.key == INCREASE_FPS_KEY):
                    self.fps_counter += 1
                if (event.key == DECREASE_FPS_KEY):
                    self.fps_counter -= 1


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
                self.game_over()

            self.gameManager.check_increase_score()

            self.fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
            self.clock.tick(self.fps_counter)

        self.game_reset()

    def increase_score(self):
        self.score += 1

    def game_reset(self):
        self.initialize()

    def game_over(self):
        self.gameRunning = False
        self.statManager.update(
            {
                'score': self.score,
            }
        )

    def draw(self):
        self.background.draw(self.screen)
        self.bird.draw(self.screen)
        self.pipeManager.draw_all_pipes(self.screen)

        # FPS counter
        if (self.fps is not -1):
            self.screen.blit(self.fps, (5, 5))

        # Score
        font = pygame.font.Font(None, 30)
        score_font = font.render(str(self.score), True, pygame.Color('white'))
        self.screen.blit(score_font, (5, 40))

    def get_dimensions(self):
        return SCREEN_SIZE

game = Game()
game.initialize()