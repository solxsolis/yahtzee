from game.play import Game
from game.human import Human

if __name__ == '__main__':
    players = [Human('player1'), Human('player2')]
    game = Game(players)
    game.start_game()