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
        bird_bounding_rect = bird.get_bounding_box()

        screen_dimensions = self.game.get_dimensions()

        if (
            (bird_bounding_rect.center[1] + bird_bounding_rect.height / 2 > screen_dimensions[1]) or
            (bird_bounding_rect.center[1] < bird_bounding_rect.height / 2)
        ):
            return True

        bird_image_rect = {
            'x': self.game.bird.x,
            'y': self.game.bird.y,
            'width': self.game.bird.image.get_rect().width,
            'height': self.game.bird.image.get_rect().height,
        }

        for i in range(len(self.game.pipeManager.all_pipes)):
            top_pipe = self.game.pipeManager.all_pipes[i].top_image
            bottom_pipe = self.game.pipeManager.all_pipes[i].bottom_image

            top_pipe_rect = {
                'x': self.game.pipeManager.all_pipes[i].x,
                'y': self.game.pipeManager.all_pipes[i].top_pipe_y,
                'width': top_pipe.get_rect().width,
                'height': top_pipe.get_rect().height,
            }

            bottom_pipe_rect = {
                'x': self.game.pipeManager.all_pipes[i].x,
                'y': self.game.pipeManager.all_pipes[i].bottom_pipe_y,
                'width': bottom_pipe.get_rect().width,
                'height': bottom_pipe.get_rect().height,
            }

            if (self.compare_rect_intersection(top_pipe_rect, bird_image_rect) or self.compare_rect_intersection(bottom_pipe_rect, bird_image_rect)) :
                return True


        return False