import pygame
from game.bird.Bird import Bird
from game.background.Background import Background
from game.pipe.PipeManager import PipeManager

from game.managers.GameManager import GameManager
from game.managers.StatManager import StatManager

import constants

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
        self.jump_enabled = True

        self.statManager = StatManager(self)

        self.fps_counter = DEFAULT_FPS

        self.current_player = None
        self.history = None
        
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
        if (player == constants.NEURAL_NETWORK_PLAYER):
            self.jump_enabled = False
            # Do nothing right now. It is the job of the neural network to call
            # update_with_params with correct parameter values
            pass
        elif(player == constants.HUMAN_PLAYER):
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

    def get_number_of_items_in_state(self):
        return 4

    def get_state(self):
        # Maybe send if the bird is already jumping
        selected_pipe = None
        for i in range(len(self.pipeManager.all_pipes)):
            if (self.pipeManager.all_pipes[i].x > self.bird.x):
                selected_pipe = self.pipeManager.all_pipes[i]

        if (selected_pipe == None):
            output_array = [
                -1, -1, -1, self.bird.y,
            ]
        else:
            output_array = [
                selected_pipe.x,
                selected_pipe.bottom_pipe_y,
                selected_pipe.top_pipe_y,
                self.bird.y, 
            ]

        return output_array

    def update_with_params(self, params):
        # TODO: Maybe not the right place for it
        action = params['action']
        if (action == constants.ACTION_JUMP):
            self.bird.jump()
        elif (action == constants.ACTION_DO_NOTHING):
            pass

        font = pygame.font.Font(None, 30)
        
        self.screen.fill(BG_COLOR)

        self.handle_events()

        self.bird.update()
        self.pipeManager.update_all_pipes()

        self.draw()

        pygame.display.flip()
        action_successful = False

        if (self.gameManager.check_game_over()) :
            self.game_over()
            self.game_reset()
        elif (action == constants.ACTION_DO_NOTHING and self.bird.jump_distance_remaining <= 0):
            self.increase_score()
            action_successful = True

        pipe_cleared = False
        if(self.gameManager.check_pipe_cleared()):
            self.increase_score()
            action_successful = True

        self.fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.clock.tick(self.fps_counter)

        return {
            'action_successful': action_successful,
        }

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

            if(self.gameManager.check_pipe_cleared()):
                self.increase_score()

            self.fps = font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
            self.clock.tick(self.fps_counter)

        self.game_reset()

    def increase_score(self):
        self.score += 1

    def game_reset(self):
        self.initialize()
        self.start(self.current_player)

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

if __name__ == '__main__':
    game = Game()
    game.initialize()
    game.start(HUMAN_PLAYER_TYPE)