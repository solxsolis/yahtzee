from gui.yahtzee_gui import YahtzeeGUI
from game.play import Game
from game.human import Human

if __name__ == "__main__":
    p1 = Human("Player 1")
    p2 = Human("Player 2")

    yahtzee_game = Game([p1, p2])

    app = YahtzeeGUI(yahtzee_game)
    app.mainloop()