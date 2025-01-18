import tkinter as tk
from gui.player_window import PlayerWindow

class YahtzeeGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Yahtzee Main Menu")
        self.geometry("300x120")

        label = tk.Label(self, text="Welcome to 2-Player Yahtzee!", font=("Helvetica", 14))
        label.pack(pady=10)

        start_btn = tk.Button(self, text="Start Game", command=self.start_game)
        start_btn.pack(pady=5)

        quit_btn = tk.Button(self, text="Quit", command=self.quit_game)
        quit_btn.pack()

        self.player_windows = []

    def start_game(self):
        if self.game.state != "active":
            self.game.start_game()

        for player in self.game.players:
            pw = PlayerWindow(self, player, self.game)
            self.player_windows.append(pw)

    def quit_game(self):
        self.destroy()


