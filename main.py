from gui.yahtzee_gui import YahtzeeGUI
from game.play import Game
from game.human import Human
from game.bot import Bot

if __name__ == "__main__":
    p1 = Human("Player 1")
    p2 = Bot("Bot")

    yahtzee_game = Game([p1, p2])

    app = YahtzeeGUI(yahtzee_game)
    app.mainloop()