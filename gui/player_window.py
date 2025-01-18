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
        dice_frame = tk.Frame(self, relief="groove", borderwidth=2)
        dice_frame.pack(pady=5)
        tk.Label(dice_frame, text=f"{self.player.name}'s Dice", font=("Helvetica", 14)).pack()

        dice_row = tk.Frame(dice_frame)
        dice_row.pack(pady=5)
        for i in range(5):
            lbl = tk.Label(dice_row, text="0", font=("Helvetica", 16), width=4, relief="solid")
            lbl.grid(row=0, column=i, padx=5)
            lbl.bind("<Button-1>", lambda e, idx=i: self.toggle_die(idx))
            self.dice_labels.append(lbl)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        self.roll_btn = tk.Button(btn_frame, text="Roll", command=self.roll_dice)
        self.roll_btn.grid(row=0, column=0, padx=10)

        self.play_btn = tk.Button(btn_frame, text="Play", command=self.play_category)
        self.play_btn.grid(row=0, column=1, padx=10)

        cat_frame = tk.Frame(self, relief="groove", borderwidth=2)
        cat_frame.pack(pady=10, fill="x")
        tk.Label(cat_frame, text="Select Category:").pack(side="left", padx=5)
        self.cat_var = tk.StringVar(value="CHOOSE")
        self.cat_combobox = ttk.Combobox(
            cat_frame, textvariable=self.cat_var,
            values=list(Category.__members__.keys()), state="readonly"
        )
        self.cat_combobox.pack(side="left", padx=5)

        sb_frame = tk.Frame(self, relief="groove", borderwidth=2)
        sb_frame.pack(pady=5, fill="both", expand=True)
        title_label = tk.Label(sb_frame, text=f"{self.player.name}'s Scoreboard", font=("Helvetica", 14))
        title_label.pack(pady=5)

        header_row = tk.Frame(sb_frame)
        header_row.pack(fill="x")

        tk.Label(header_row, text="Category", width=12, anchor="w", font=("Helvetica", 12, "bold")).pack(side="left")
        tk.Label(header_row, text=self.player.name, width=12, anchor="center", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        opp = self.get_opponent()
        opp_name = opp.name if opp else "Opponent"
        tk.Label(header_row, text=opp_name, width=12, anchor="center", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        self.table_frame = tk.Frame(sb_frame)
        self.table_frame.pack(fill="x", padx=5, pady=5)


        for cat_name in Category.__members__.keys():
            row_frame = tk.Frame(self.table_frame)
            row_frame.pack(fill="x", pady=2)

            lbl_cat = tk.Label(row_frame, text=cat_name, width=12, anchor="w", relief="ridge")
            lbl_cat.pack(side="left")

            lbl_player_score = tk.Label(row_frame, text="", width=6, anchor="e", relief="ridge")
            lbl_player_score.pack(side="left", padx=5)

            lbl_opp_score = tk.Label(row_frame, text="", width=6, anchor="e", relief="ridge")
            lbl_opp_score.pack(side="left", padx=5)

            self.score_labels[cat_name] = (lbl_player_score, lbl_opp_score)

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
                lbl.config(text="0", bg="SystemButtonFace")
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

            pscore_str = "" if not pscore else str(pscore)
            oscore_str = "" if not oscore else str(oscore)

            lbl_player, lbl_opp = self.score_labels[cat_name]
            lbl_player.config(text=pscore_str)
            lbl_opp.config(text=oscore_str)

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