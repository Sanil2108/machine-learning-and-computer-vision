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

        self.statManager = StatManager(self)

        self.fps_counter = DEFAULT_FPS

        self.current_player = None
        self.history = None
        
    def initialize(self, params):
        self.gameRunning = True

        self.jump_enabled = params['jumpEnabled']
        self.bird_count = params['birdCount'];

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(BG_COLOR)

        self.birds = []
        for i in range(self.bird_count):
            self.birds.push(Bird())
        self.pipeManager = PipeManager(self)
        self.background = Background()

        self.gameManager = GameManager(self)

        for i in range(self.bird_count):
            self.birds[i].initialize()
        self.pipeManager.initialize()
        self.background.initialize()

        self.clock = pygame.time.Clock()

        self.score = 0

    def start(self, player):
        self.current_player = player
        if(player == constants.HUMAN_PLAYER):
            self.update()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY and self.jump_enabled:
                    self.birds[0].jump()
                if (event.key == EXIT_KEY):
                    exit()
                if (event.key == INCREASE_FPS_KEY):
                    self.fps_counter += 1
                if (event.key == DECREASE_FPS_KEY):
                    self.fps_counter -= 1

    def get_number_of_items_in_state(self):
        return 4

    def get_state(self, index):
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
                self.birds[index].y,
            ]

        return output_array

    # Params would take an array of actions
    def update_with_params(self, params):
        actions = params['actions']
        assert len(actions) == self.bird_count

        for i in range(len(actions)):
            if actions[i] == constants.ACTION_JUMP:
                self.birds[i].jump()
        
        self.screen.fill(BG_COLOR)

        self.handle_events()

        for bird of self.birds:
            bird.update()
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

        if(self.gameManager.check_pipe_cleared()):
            self.increase_score()
            action_successful = True

        self.clock.tick(self.fps_counter)

        return {
            'action_successful': action_successful,
        }

    def update(self):
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
        # Objects
        for bird in self.birds:
            bird.draw(self.screen)
        self.background.draw(self.screen)
        self.pipeManager.draw_all_pipes(self.screen)

        font = pygame.font.Font(None, 30)

        # FPS counter
        fps_font = font.render(str(self.clock.get_fps()), True, pygame.Color('white'))
        self.screen.blit(fps_font, (5, 5))

        # Score
        score_font = font.render(str(self.score), True, pygame.Color('white'))
        self.screen.blit(score_font, (5, 40))

    def get_dimensions(self):
        return SCREEN_SIZE

if __name__ == '__main__':
    game = Game()
    game.initialize({'birdCount': 1, 'jumpEnabled':True})
    game.start(constants.HUMAN_PLAYER_TYPE)