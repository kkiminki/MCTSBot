
from random import choice


def think(state):
    """ Returns a random move. """
    move = choice(state.legal_moves)
    print("random bot move = "+str(move))
    return move
