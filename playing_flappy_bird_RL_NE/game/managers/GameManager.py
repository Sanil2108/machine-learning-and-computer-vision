class GameManager(object):

    def __init__(self, game):
        self.game = game

    def check_point_in_rect(self, point, rect):
        if (point[0] > rect['x'] and point[0] < rect['x'] + rect['width'] and point[1] < rect['y'] + rect['height'] and point[1] > rect['y']) :
            return True


    def compare_rect_intersection(self, rect1, rect2):
        if (self.check_point_in_rect([rect1['x'], rect1['y']], rect2) or self.check_point_in_rect([rect1['x'] + rect1['width'], rect1['y']], rect2) or
            self.check_point_in_rect([rect1['x'] + rect1['width'], rect1['y'] + rect1['height']], rect2) or self.check_point_in_rect([rect1['x'], rect1['y'] + rect1['height']], rect2)):
            return True

    def check_game_over(self):
        bird = self.game.bird
        bird_bounding_rect = bird.get_bounding_box()[0]

        screen_dimensions = self.game.get_dimensions()

        if (
            (bird_bounding_rect['y'] + bird_bounding_rect['height'] > screen_dimensions[1]) or
            (bird_bounding_rect['y'] < bird_bounding_rect['height'])
        ):
            return True


        for i in range(len(self.game.pipeManager.all_pipes)):
            pipe = self.game.pipeManager.all_pipes[i]
            if (self.compare_rect_intersection(bird_bounding_rect, pipe.get_bounding_box()[0]) or 
            self.compare_rect_intersection(bird_bounding_rect, pipe.get_bounding_box()[1])):
                return True

        return False

    def check_increase_score(self):
        bird = self.game.bird
        bird_bounding_rect = bird.get_bounding_box()[0]

        for i in range(len(self.game.pipeManager.all_pipes)):
            pipe = self.game.pipeManager.all_pipes[i]
            if (pipe.crossed == False and pipe.get_bounding_box()[0]['x'] < bird_bounding_rect['x']):
                self.game.increase_score()
                pipe.crossed = True

                print(self.game.score)