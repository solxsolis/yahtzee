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
        self.category_labels = []

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

        score_frame = tk.Frame(self, relief="groove", borderwidth=2)
        score_frame.pack(pady=5, fill="both", expand=True)
        tk.Label(score_frame, text=f"{self.player.name}'s Scoreboard", font=("Helvetica", 14)).pack()

        self.sb_list_frame = tk.Frame(score_frame)
        self.sb_list_frame.pack(padx=5, pady=5, fill="x")

        for idx, cat_name in enumerate(Category.__members__.keys()):
            row_frame = tk.Frame(self.sb_list_frame)
            row_frame.pack(fill="x")

            lbl_cat = tk.Label(row_frame, text=cat_name, width=12, anchor="w")
            lbl_cat.pack(side="left")

            lbl_score = tk.Label(row_frame, text="0", width=4, anchor="e")
            lbl_score.pack(side="right", padx=10)

            self.category_labels.append(lbl_score)

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

        self.game.next_turn()
        messagebox.showinfo("Turn Over", f"{self.player.name} finished. Now it's {self.game.current_player.name}'s turn.")

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
        scores = self.player.board.categories_score
        for i, lbl in enumerate(self.category_labels):
            if i < len(scores):
                lbl.config(text=str(scores[i]))

    def is_player_turn(self):
        if self.game.current_player != self.player:
            messagebox.showerror("Not Your Turn", f"Wait for {self.game.current_player.name} to finish.")
            return False
        return True