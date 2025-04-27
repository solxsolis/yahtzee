import tkinter as tk
from gui.player_window import PlayerWindow
from gui.rules_window import RulesWindow
from game.bot import Bot
from game.play import Game
from game.human import Human

class YahtzeeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = None
        self.title("Yahtzee Main Menu")
        self.geometry("300x250")

        self.config(bg="#addbf7")

        label = tk.Label(self, text="Welcome to 2-Player Yahtzee!", font=("Helvetica", 14), bg="#addbf7")
        label.pack(pady=10)

        self.mode_var = tk.StringVar(value="hb")
        tk.Label(self, text="Choose mode:", font=("Helvetica", 12), bg = "#addbf7").pack(pady=(10, 0))
        modes = [("Human vs Human", "hh"), ("Human vs Bot", "hb")]

        for text, val in modes:
            tk.Radiobutton(self, text=text, variable=self.mode_var, value=val, bg="#addbf7").pack(anchor="w", padx=20 )

        start_btn = tk.Button(self, text="Start Game", command=self.start_game, bg='#8bd1fc')
        start_btn.pack(pady=5)

        rules_btn = tk.Button(self, text="Rules", command=self.get_rules, bg='#8bd1fc')
        rules_btn.pack(pady=5)

        quit_btn = tk.Button(self, text="Quit", command=self.quit_game, bg='#8bd1fc')
        quit_btn.pack(pady=5)


        self.player_windows = []
        self.rules_window = []

    def start_game(self):
        mode = self.mode_var.get()
        if mode == "hh":
            p1 = Human("Player 1")
            p2 = Human("Player 2")
        else:
            p1 = Human("Player")
            p2 = Bot("Bot")

        self.game = Game([p1, p2])
        self.game.start_game()


        for player in self.game.players:
            pw = PlayerWindow(self, player, self.game)
            self.player_windows.append(pw)

        self._start_current_player()

    def _start_current_player(self):
        cp = self.game.get_current_player()
        cp.start_turn()

        for w in self.player_windows:
            w.update_scoreboard()
            w.update_dice_display()
            w.update_button_states()

        if isinstance(cp, Bot):
            self.after(150, self._do_bot_move)

    def _do_bot_move(self):
        bot = self.game.get_current_player()
        bot.play_turn()

        for w in self.player_windows:
            w.update_scoreboard()
            w.update_dice_display()
            w.update_button_states()

        winner, scores = self.game.next_turn()
        if winner or self.game.get_state() == "finished":
            self.player_windows[0].show_end_game_message(winner, scores)
        else:
            self._start_current_player()



    def quit_game(self):
        self.destroy()

    def get_rules(self):
        self.rules_window = RulesWindow(self, self.game)


