from network import GameServer
from game.play import Game
from game.human import Human
import time


if __name__ == '__main__':
    def make_game():
        return Game([Human("Player 1"), Human("Player 2")])
    gs = GameServer("0.0.0.0", 9999, make_game)
    print("Server started.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped.")