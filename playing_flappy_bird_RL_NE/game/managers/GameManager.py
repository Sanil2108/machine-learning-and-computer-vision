class GameManager(object):

    def __init__(self, game):
        self.game = game

    def check_game_over(self):
        bird = self.game.bird
        bird_bounding_rect = bird.get_bounding_box()

        screen_dimensions = self.game.get_dimensions()

        if (
            (bird_bounding_rect.center[1] + bird_bounding_rect.height / 2 > screen_dimensions[1]) or
            (bird_bounding_rect.center[1] < bird_bounding_rect.height / 2)
        ):
            return True

        return False