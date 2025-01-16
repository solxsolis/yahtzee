from game.board import Board
from game.categories import Category
from game.exceptions import *

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.active = False
        self.turns = 13

    def get_name(self):
        return self.name

    def get_board(self):
        return self.board

    def get_active(self):
        return self.active

    def get_turns(self):
        return self.turns

    def start_turn(self):
        if self.turns <= 0:
            raise NoTurnsLeftError(self)
        if not self.active:
            self.active = True
            self.turns -= 1

    def end_turn(self):
        if self.active:
            self.active = False

    def set_score(self, category, score):
        try:
            self.board.add_score(category, score)
        except CategoryPlayedError as e:
            print(e)




