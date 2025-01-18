import tkinter as tk
from tkinter import messagebox, ttk
from game.categories import Category
from game.exceptions import CategoryPlayedError, NoRollsLeftError


class PlayerWindow(tk.Toplevel):
    def __init__(self, master, player, game):
        super().__init__(master)
        self.player = player
        self.game = game

        self.title(f"Yahtzee - {self.player.name}")
        self.dice_labels = []
        self.score_labels = {}

        self.create_widgets()
        self.update_scoreboard()
        self.update_dice_display()

    def create_widgets(self):
        self.dice_frame = tk.Frame(self)
        self.dice_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        dice_title = tk.Label(self.dice_frame, text=f"{self.player.name}'s Dice", font=("Helvetica", 14))
        dice_title.grid(row=0, column=0, columnspan=5, pady=5)

        for i in range(5):
            lbl = tk.Label(self.dice_frame, text="", width=4, relief="solid", font=("Helvetica", 16))
            lbl.grid(row=1, column=i, padx=5)
            lbl.bind("<Button-1>", lambda e, idx=i: self.toggle_die(idx))
            self.dice_labels.append(lbl)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=1, column=0, columnspan=3, pady=5)

        self.roll_btn = tk.Button(self.btn_frame, text="Roll", command=self.roll_dice)
        self.roll_btn.grid(row=0, column=0, padx=10)

        self.play_btn = tk.Button(self.btn_frame, text="Play", command=self.play_category)
        self.play_btn.grid(row=0, column=1, padx=10)

        cat_label = tk.Label(self.btn_frame, text="Select Category:")
        cat_label.grid(row=1, column=0, sticky="e")

        self.cat_var = tk.StringVar(value="CHOOSE")
        cat_options = list(Category.__members__.keys())
        self.cat_cb = ttk.Combobox(self.btn_frame, textvariable=self.cat_var, values=cat_options, state="readonly")
        self.cat_cb.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.sb_frame = tk.Frame(self, relief="groove", borderwidth=2)
        self.sb_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        sb_title = tk.Label(self.sb_frame, text=f"{self.player.name}'s Scoreboard", font=("Helvetica", 14))
        sb_title.grid(row=0, column=0, columnspan=3, pady=5)

        tk.Label(self.sb_frame, text="Category", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, sticky="w")
        tk.Label(self.sb_frame, text=self.player.name, font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=5, sticky="w")

        opponent = self.get_opponent()
        opponent_name = opponent.name if opponent else "Opponent"
        tk.Label(self.sb_frame, text=opponent_name, font=("Helvetica", 12, "bold")).grid(row=1, column=2, padx=5, sticky="w")

        categories = list(Category.__members__.keys())

        row_index = 2
        for cat_name in categories:
            cat_label = tk.Label(self.sb_frame, text=cat_name, width=12, relief="ridge")
            cat_label.grid(row=row_index, column=0, padx=5, pady=2, sticky="w")

            lbl_player_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
            lbl_player_score.grid(row=row_index, column=1, padx=5, pady=2, sticky="e")

            lbl_opp_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
            lbl_opp_score.grid(row=row_index, column=2, padx=5, pady=2, sticky="e")

            self.score_labels[cat_name] = (lbl_player_score, lbl_opp_score)
            row_index += 1

        self.running_score_label = tk.Label(self.sb_frame, text="Score:", font=("Helvetica", 12, "bold"))
        self.running_score_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="e")

        self.running_score_player = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
        self.running_score_player.grid(row=row_index, column=1, padx=5, pady=5, sticky="e")

        self.running_score_opponent = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
        self.running_score_opponent.grid(row=row_index, column=2, padx=5, pady=5, sticky="e")

    def toggle_die(self, idx):
        if not self.is_player_turn():
            return

        if self.player.current_turn:
            self.player.current_turn.dice[idx].toggle()
            self.update_dice_display()

    def roll_dice(self):
        if not self.is_player_turn():
            return

        if not self.player.current_turn:
            self.player.start_turn()
        try:
            self.player.current_turn.roll()
            self.update_dice_display()
        except NoRollsLeftError as e:
            messagebox.showerror("No rolls left", str(e))

    def play_category(self):

        if not self.is_player_turn():
            return

        if not self.player.current_turn:
            messagebox.showerror("Error", "No current turn. Roll first.")
            return

        cat_name = self.cat_var.get()
        if cat_name not in Category.__members__:
            messagebox.showerror("Error", f"Invalid category: {cat_name}")
            return

        chosen_cat = Category.__members__[cat_name]

        try:
            score = self.player.current_turn.get_score(chosen_cat)
        except Exception as e:
            messagebox.showerror("Scoring Error", str(e))
            return

        try:
            self.player.set_score(chosen_cat, score)
            messagebox.showinfo("Category Played", f"You scored {score} in {cat_name}!")
        except CategoryPlayedError as ce:
            messagebox.showerror("Category Error", str(ce))
            return

        self.player.end_turn()
        self.update_scoreboard()
        self.update_dice_display()

        winner, scores = self.game.next_turn()
        if winner or self.game.get_state() == "finished":
            self.show_end_game_message(winner, scores)
        else:
            messagebox.showinfo("Turn Over", f"{self.player.name} finished. Now it's {self.game.current_player.name}'s turn.")

    def show_end_game_message(self, winner, scores):
        lines = ["Final Scores: \n"]
        for i in range(0,2):
            lines.append(f"{self.game.get_players()[i].get_name()}: {scores[i]}")
        if winner:
            lines.append(f"Winner: {winner.get_name()}")
        else:
            lines.append(f"Draw")

        messagebox.showinfo("Game Over", "\n".join(lines))

        for w in self.master.player_windows:
            w.destroy()
        self.master.destroy()


    def update_dice_display(self):
        if not self.player.current_turn:
            for lbl in self.dice_labels:
                lbl.config(text="", bg="SystemButtonFace")
            return

        dice_vals = self.player.current_turn.get_dice_values()
        for i, val in enumerate(dice_vals):
            lbl = self.dice_labels[i]
            lbl.config(text=str(val))
            if not self.player.current_turn.dice[i].get_active():
                lbl.config(bg="lightgray")
            else:
                lbl.config(bg="white")

    def update_scoreboard(self):
        player_scores = self.player.board.categories_score
        opponent = self.get_opponent()
        opp_scores = opponent.board.categories_score if opponent else []

        cat_list = list(Category.__members__.keys())
        for i, cat_name in enumerate(cat_list):
            pscore = player_scores[i]
            oscore = opp_scores[i] if i < len(opp_scores) else 0

            pscore_str = "" if pscore is None else str(pscore)
            oscore_str = "" if oscore is None else str(oscore)

            lbl_player, lbl_opp = self.score_labels[cat_name]
            lbl_player.config(text=pscore_str)
            lbl_opp.config(text=oscore_str)

        player_total = sum(s for s in player_scores if s is not None)
        opp_total = sum(s for s in opp_scores if s is not None)

        self.running_score_player.config(text=str(player_total) if player_total else "0")
        self.running_score_opponent.config(text=str(opp_total) if opp_total else "0")

    def get_opponent(self):
        for p in self.game.get_players():
            if p != self.player:
                return p
        return None

    def is_player_turn(self):
        if self.game.current_player != self.player:
            messagebox.showerror("Not Your Turn", f"Wait for {self.game.current_player.name} to finish.")
            return False
        return True