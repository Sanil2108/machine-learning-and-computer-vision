from game.game import Game

from ai_players.neural_network import NeuralNetworkPlayer
from ai_players.neuro_evolutionary_player import NeuroEvolutionaryPlayer

import constants

if __name__ == '__main__':
    player = constants.HUMAN_PLAYER

    # Start the game
    game = Game()

    if (player is constants.HUMAN_PLAYER):
        game.initialize(
            {'birdCount': 1, 'jumpEnabled':True}
        )

        game.start(player)

    elif (player is constants.NEURAL_NETWORK_PLAYER):
        neural_network_player = NeuralNetworkPlayer(game.get_number_of_items_in_state())
        game.initialize(
            neural_network_player.get_initialization_params()
        )
        game.start(player)

        while True:
            neural_network_player.update()
            game_state = game.get_state()
            action = neural_network_player.get_action(game_state)
            game_response = game.update_with_params(action)
            neural_network_player.update_data(game_response, game_state, action)

    elif (player is constants.NEURO_EVOLUTIONARY_PLAYER):
        neuro_evolutionary_player = NeuroEvolutionaryPlayer(game.get_number_of_items_in_state())
        game.initialize(
            neuro_evolutionary_player.get_initialization_params()
        )
        game.start(player)

        while True:
            neuro_evolutionary_player.update()
            game_state = game.get_state()
            action = neuro_evolutionary_player.get_action(game_state)
            game_response = game.update_with_params(action)
            neuro_evolutionary_player.update_data(game_response, game_state, action)