import tkinter as tk
from tkinter import messagebox
from gui.player_window import PlayerWindow
from gui.rules_window import RulesWindow
from game.bot import Bot
from game.play import Game
from game.human import Human
from connection.network import NetworkClient, GameServer
from game.network_player import NetworkPlayer

class YahtzeeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = None

        self.title("Yahtzee Main Menu")
        self.geometry("300x300")

        self.config(bg="#addbf7")

        label = tk.Label(self, text="Welcome to 2-Player Yahtzee!", font=("Helvetica", 14), bg="#addbf7")
        label.pack(pady=10)

        self.mode_var = tk.StringVar(value="hb")
        tk.Label(self, text="Choose mode:", font=("Helvetica", 12), bg = "#addbf7").pack(pady=(10, 0))
        modes = [("Human vs Bot", "hb"), ("Local Human vs Human", "hh_local"), ("Host Human vs Human", "hh_host"), ("Join Human vs Human", "hh_join")]

        for text, val in modes:
            tk.Radiobutton(self, text=text, variable=self.mode_var, value=val, bg="#addbf7").pack(anchor="w", padx=20 )

        start_btn = tk.Button(self, text="Start Game", command=self.start_game, bg='#8bd1fc')
        start_btn.pack(pady=5)

        rules_btn = tk.Button(self, text="Rules", command=self.get_rules, bg='#8bd1fc')
        rules_btn.pack(pady=5)

        quit_btn = tk.Button(self, text="Quit", command=self.quit_game, bg='#8bd1fc')
        quit_btn.pack(pady=5)


        self.player_windows = []
        self.rules_window = None
        self.net_client = None

        # if self.mode == "local":
        #     pass
        # else:
        #     self.net_client = NetworkClient(self.host, self.port, self._on_state)
        #     player = NetworkPlayer(self.player_id, self.net_client)
        #     pw = PlayerWindow(self, player, game=None)
        #     self.player_windows.append(pw)

    def start_game(self):
        mode = self.mode_var.get()
        if mode == "hh_local":
            players = [Human("Player 1"),
            Human("Player 2")]
        elif mode == "hb":
            players = [Human("Player"),
            Bot("Bot")]
        elif mode == "hh_host":
            def make_game():
                return Game([Human("Player 1", Human("Player 2"))])
            GameServer("0.0.0.0", 9999, make_game)
            self.net_client = NetworkClient("127.0.0.1", 9999, self._on_state)
            players = [NetworkPlayer(0, self.net_client), NetworkPlayer(1, self.net_client)]
        elif mode == "hh_join":
            host, port = self.ask_host_port(default = "127.0.0.1", default_port = 9999)
            self.net_client = NetworkClient(host, port, self._on_state)
            players = [NetworkPlayer(0, self.net_client), NetworkPlayer(1, self.net_client)]
        else:
            messagebox.showerror("Error", f"Invalid mode: {mode}")
            return

        if self.net_client is None:
            self.game = Game(players)
            self.game.start_game()
        else:
            self.game = None


        for player in players:
            pw = PlayerWindow(self, player, self.game)
            self.player_windows.append(pw)

        if self.net_client is None:
            self._start_current_player()

    def ask_host_port(self, default, default_port):
        dlg = tk.Toplevel(self)
        dlg.title("Connect to host")
        tk.Label(dlg, text="Host:").grid(row=0, column=0, padx=5, pady=5)
        hvar = tk.StringVar(value=default)
        tk.Entry(dlg, textvariable=hvar).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dlg, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        pvar = tk.StringVar(value=default_port)
        tk.Entry(dlg, textvariable=pvar).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(dlg, text="OK", command=dlg.destroy).grid(row=2, column=0, columnspan=2, pady=10)
        self.wait_window(dlg)
        return hvar.get(), int(pvar.get())

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

    def _on_state(self, msg):
        if msg["type"] == "state":
            for w in self.player_windows:
                w.render_state(msg)
        elif msg["type"] == "game_over":
            self.player_windows[0].show_end_game_message(msg["winner"], msg.get("scores"))



    def quit_game(self):
        self.destroy()

    def get_rules(self):
        self.rules_window = RulesWindow(self, self.game)


