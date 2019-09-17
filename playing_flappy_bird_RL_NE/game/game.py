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

# Interfacing variables
NEURAL_NETWORK_PLAYER_TYPE = 1
HUMAN_PLAYER_TYPE = 1

class Game(object):
    def __init__(self):
        self.bird = None
        self.background = None
        self.pipeManager = None

        self.gameRunning = None
        self.jump_enabled = True

        self.statManager = StatManager(self)

        self.fps_counter = DEFAULT_FPS

        self.current_player = None
        
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

    def start(self, player):
        self.current_player = player
        if (player == NEURAL_NETWORK_PLAYER_TYPE):
            self.jump_enabled = False
            # Do nothing right now. It is the job of the neural network to call
            # update_with_params with correct parameter values
            pass
        elif(player == HUMAN_PLAYER_TYPE):
            self.update()


    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY and self.jump_enabled:
                    self.bird.jump()
                if (event.key == EXIT_KEY):
                    exit()
                if (event.key == INCREASE_FPS_KEY):
                    self.fps_counter += 1
                if (event.key == DECREASE_FPS_KEY):
                    self.fps_counter -= 1

    def get_state(self):
        # Maybe send if the bird is already jumping
        selected_pipe = None
        for i in range(self.pipeManager.all_pipes):
            if (self.pipeManager.all_pipes[i].x > self.bird.x):
                selected_pipe = self.pipeManager.all_pipes[i]

        output_array = [
            selected_pipe.x,
            selected_pipe.bottom_pipe_end_y,
            selected_pipe.top_pipe_end_y,
            self.bird.y, 
        ]
        return output_array

    def update_with_params(self, params):
        font = pygame.font.Font(None, 30)
        
        self.screen.fill(BG_COLOR)

        self.handle_events()

        self.bird.update()
        self.pipeManager.update_all_pipes()

        self.draw()

        pygame.display.flip()

        if (self.gameManager.check_game_over()) :
            self.game_over()
            self.game_reset()

        self.gameManager.check_increase_score()

        self.fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.clock.tick(self.fps_counter)

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
                self.gameRunning = False
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

if __name__ == '__main__':
    game.start(HUMAN_PLAYER_TYPE)
else:
    game.start(NEURAL_NETWORK_PLAYER_TYPE)