import tkinter as tk
from tkinter import messagebox, ttk
from game.categories import Category
from game.exceptions import CategoryPlayedError, NoRollsLeftError, ScoringError


class PlayerWindow(tk.Toplevel):
    def __init__(self, master, player, game):
        super().__init__(master)
        self.player = player
        self.game = game

        self.title(f"Yahtzee - {self.player.name}")
        self.dice_labels = []
        self.score_labels = {}

        self.dice_images = []
        self.category_images = {}

        self.selected_category = None
        self.previewed_score = 0

        self.left_cats = list(Category.__members__.keys())[:6]
        self.right_cats = list(Category.__members__.keys())[6:]

        self.create_widgets()
        self.update_scoreboard()
        self.update_dice_display()

    def create_widgets(self):

        for face_val in range(1, 7):
            image_file = f"images/die{face_val}.png"
            dice_img = tk.PhotoImage(file=image_file)
            self.dice_images.append(dice_img)

        self.dice_frame = tk.Frame(self)
        self.dice_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        dice_title = tk.Label(self.dice_frame, text=f"{self.player.name}'s Dice", font=("Helvetica", 14))
        dice_title.grid(row=0, column=0, columnspan=5, pady=5)

        blank_file = f"images/blank.png"
        blank_img = tk.PhotoImage(file=blank_file)
        for i in range(5):
            lbl = tk.Label(self.dice_frame, image=blank_img, bg="SystemButtonFace", relief="raised")
            lbl.grid(row=1, column=i, padx=5)
            lbl.bind("<Button-1>", lambda e, idx=i: self.toggle_die(idx))
            self.dice_labels.append(lbl)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=1, column=0, columnspan=3, pady=5)

        self.roll_btn = tk.Button(self.btn_frame, text="Roll", command=self.roll_dice)
        self.roll_btn.grid(row=0, column=0, padx=10)

        self.play_btn = tk.Button(self.btn_frame, text="Play", command=self.play_category)
        self.play_btn.grid(row=0, column=1, padx=10)

        self.rolls_left_label = tk.Label(self.btn_frame, text="Rolls Left: 3", font=("Helvetica", 10))
        self.rolls_left_label.grid(row=0, column=2, padx=10)

        self.sb_frame = tk.Frame(self, relief="groove", borderwidth=2)
        self.sb_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        sb_title = tk.Label(self.sb_frame, text=f"{self.player.name}'s Scoreboard", font=("Helvetica", 14))
        sb_title.grid(row=0, column=0, columnspan=3, pady=5)

        tk.Label(self.sb_frame, text="Category", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, sticky="w")
        tk.Label(self.sb_frame, text=self.player.name, font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=5, sticky="w")
        tk.Label(self.sb_frame, text="Opponent", font=("Helvetica", 12, "bold")).grid(row=1, column=2, padx=5, sticky="w")

        tk.Label(self.sb_frame, text="Category", font=("Helvetica", 12, "bold")).grid(row=1, column=3, padx=5, sticky="w")
        tk.Label(self.sb_frame, text=self.player.name, font=("Helvetica", 12, "bold")).grid(row=1, column=4, padx=5, sticky="w")
        tk.Label(self.sb_frame, text="Opponent", font=("Helvetica", 12, "bold")).grid(row=1, column=5, padx=5, sticky="w")

        row_index = 2
        max_rows = len(self.right_cats)
        for i in range(max_rows):
            if i < max_rows - 1:
                left_cat_name = self.left_cats[i]
                left_image_file = f"images/cat_{left_cat_name.lower()}.png"
                left_cat_img = tk.PhotoImage(file=left_image_file)
                self.category_images[left_cat_name] = left_cat_img

                left_cat_button = tk.Button(self.sb_frame, image=left_cat_img, command=lambda c=left_cat_name: self.select_category(c))
                left_cat_button.grid(row=row_index, column=0, padx=2, pady=2, sticky="w")

                left_lbl_player_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
                left_lbl_player_score.grid(row=row_index, column=1, padx=5, pady=2, sticky="e")

                left_lbl_opp_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
                left_lbl_opp_score.grid(row=row_index, column=2, padx=5, pady=2, sticky="e")

                self.score_labels[left_cat_name] = (left_cat_button, left_lbl_player_score, left_lbl_opp_score)

            right_cat_name = self.right_cats[i]
            right_image_file = f"images/cat_{right_cat_name.lower()}.png"
            right_cat_img = tk.PhotoImage(file=right_image_file)
            self.category_images[right_cat_name] = right_cat_img

            right_cat_button = tk.Button(self.sb_frame, image=right_cat_img,
                                        command=lambda c=right_cat_name: self.select_category(c))
            right_cat_button.grid(row=row_index, column=3, padx=2, pady=2, sticky="w")

            right_lbl_player_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
            right_lbl_player_score.grid(row=row_index, column=4, padx=5, pady=2, sticky="e")

            right_lbl_opp_score = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
            right_lbl_opp_score.grid(row=row_index, column=5, padx=5, pady=2, sticky="e")

            self.score_labels[right_cat_name] = (right_cat_button, right_lbl_player_score, right_lbl_opp_score)
            row_index += 1

        self.running_score_label = tk.Label(self.sb_frame, text="Score:", font=("Helvetica", 12, "bold"))
        self.running_score_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="e")

        self.running_score_player = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
        self.running_score_player.grid(row=row_index, column=1, padx=5, pady=5, sticky="e")

        self.running_score_opponent = tk.Label(self.sb_frame, text="", width=6, relief="ridge", anchor="e")
        self.running_score_opponent.grid(row=row_index, column=2, padx=5, pady=5, sticky="e")

    def select_category(self, cat_name):
        if not self.is_player_turn():
            return
        if not self.player.get_current_turn():
            return

        old_category = self.selected_category
        if old_category and old_category != cat_name:
            self.revert_old_preview(old_category)

        self.selected_category = cat_name
        self.previewed_score = 0

        try:
            chosen_cat = Category.__members__[cat_name]
            potential_score = self.player.get_current_turn().get_score(chosen_cat)
            self.previewed_score = potential_score

            _, lbl_player, _ = self.get_category_labels(cat_name)
            lbl_player.config(text=str(potential_score), fg="gray")

        except ScoringError as e:
            pass

    def revert_old_preview(self, old_cat):
        cat_list = list(Category.__members__.keys())
        old_idx = cat_list.index(old_cat)
        old_score = self.player.get_board().get_categories_score()[old_idx]

        if old_score is None:
            _, lbl_player, _ = self.score_labels[old_cat]
            lbl_player.config(text="", fg="black")

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
            rolls_left = self.player.get_current_turn().get_rolls()
            self.rolls_left_label.config(text=f"Rolls left: {rolls_left}")
        except NoRollsLeftError as e:
            messagebox.showerror("No rolls left", str(e))

    def play_category(self):

        if not self.is_player_turn():
            return

        if not self.player.current_turn:
            messagebox.showerror("Error", "No current turn. Roll first.")
            return

        if not self.selected_category:
            messagebox.showerror("Error", "No category selected.")
            return

        cat_name = self.selected_category
        chosen_cat = Category.__members__.get(cat_name, None)
        if not chosen_cat:
            messagebox.showerror("Error", f"Invalid category: {cat_name}")
            return


        try:
            self.player.set_score(chosen_cat, self.previewed_score)
        except CategoryPlayedError as e:
            messagebox.showerror("Scoring Error", str(e))
            return

        cat_button, lbl_player_score, lbl_opp_score = self.score_labels[cat_name]
        lbl_player_score.config(text=str(self.previewed_score), fg="black")
        cat_button.config(state="disabled")


        self.player.end_turn()
        self.selected_category = None
        self.previewed_score = None
        self.update_scoreboard()
        self.update_dice_display()

        winner, scores = self.game.next_turn()
        if winner or self.game.get_state() == "finished":
            self.show_end_game_message(winner, scores)

    def get_category_labels(self, cat_name):
        return self.score_labels.get(cat_name, (None, None, None))


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
        blank_file = f"images/blank.png"
        blank_img = tk.PhotoImage(file=blank_file)
        if not self.player.current_turn:
            for lbl in self.dice_labels:
                lbl.config(image=blank_img, bg="SystemButtonFace")
            return

        dice_vals = self.player.current_turn.get_dice_values()
        for i, val in enumerate(dice_vals):
            lbl = self.dice_labels[i]
            if val == 0:
                lbl.config(image=blank_img)
            else:
                lbl.config(image=self.dice_images[val-1])
            if not self.player.current_turn.dice[i].get_active():
                lbl.config(relief="sunken", bd=3)
            else:
                lbl.config(relief="raised", bd=3)

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

            _, lbl_player, lbl_opp = self.score_labels[cat_name]
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