import tkinter as tk
from gui.player_window import PlayerWindow
from gui.rules_window import RulesWindow

class YahtzeeGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Yahtzee Main Menu")
        self.geometry("300x170")

        self.config(bg="#addbf7")

        label = tk.Label(self, text="Welcome to 2-Player Yahtzee!", font=("Helvetica", 14), bg="#addbf7")
        label.pack(pady=10)

        start_btn = tk.Button(self, text="Start Game", command=self.start_game, bg='#8bd1fc')
        start_btn.pack(pady=5)

        quit_btn = tk.Button(self, text="Quit", command=self.quit_game, bg='#8bd1fc')
        quit_btn.pack(pady=5)

        rules_btn = tk.Button(self, text="Rules", command=self.get_rules, bg='#8bd1fc')
        rules_btn.pack(pady=5)

        self.player_windows = []
        self.rules_window = []

    def start_game(self):
        if self.game.state != "active":
            self.game.start_game()

        for player in self.game.players:
            pw = PlayerWindow(self, player, self.game)
            self.player_windows.append(pw)

    def quit_game(self):
        self.destroy()

    def get_rules(self):
        self.rules_window = RulesWindow(self, self.game)


