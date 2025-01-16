from game.dice import Die
from game.turn import Turn
from game.player import Player

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play_turn(self, idx_player):
        if idx_player == 0:
            turn = Turn(self.player1)
        elif idx_player == 1:
            turn = Turn(self.player2)

