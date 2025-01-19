import tkinter as tk

class RulesWindow(tk.Tk):
    def __init__(self, master, game):
        self.game = game
        self.master = master
        super().__init__()
        self.config(bg="#addbf7")

        self.rules_file = "gui/rules.txt"

        with open(self.rules_file, "r", encoding="utf-8") as f:
            file_text = f.read()

        back_btn = tk.Button(self, text="Close", command=self.go_back, bg='#8bd1fc')
        back_btn.pack(padx=5, pady=5, anchor="w")

        tk.Label(self, text=file_text,font=("Helvetica", 12), bg="#addbf7").pack(padx=5, pady=5)

    def go_back(self):
        self.destroy()


