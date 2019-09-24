from game.game import Game
from ai_players.neural_network import NeuralNetworkPlayer
import constants

if __name__ == '__main__':
    player = constants.HUMAN_PLAYER

    game = Game()
    game.initialize()
    game.start(player)

    if (player is constants.HUMAN_PLAYER):
        pass
    elif (player is constants.NEURAL_NETWORK_PLAYER):
        neural_network_player = NeuralNetworkPlayer(game.get_number_of_items_in_state())
        while True:
            neural_network_player.update()
            response = game.update_with_params(neural_network_player.get_action())
            neural_network_player.update_data(response)