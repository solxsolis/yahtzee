from network import GameServer
from game.play import Game
from game.human import Human

if __name__ == '__main__':
    def make_game():
        return Game([Human("Player 1"), Human("Player 2")])
    GameServer("0.0.0.0", 9999, make_game)