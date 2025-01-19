from game.board import Board
from game.turn import Turn
from game.exceptions import *

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.active = False
        self.turns = 13
        self.current_turn = None

    def get_name(self):
        return self.name

    def get_board(self):
        return self.board

    def get_active(self):
        return self.active

    def get_turns(self):
        return self.turns

    def get_current_turn(self):
        return self.current_turn

    def start_turn(self):
        if self.turns <= 0:
            raise NoTurnsLeftError(self.get_name())
        if not self.active:
            self.active = True
            self.turns -= 1
            self.current_turn = Turn(self.board.get_yahtzee())

    def end_turn(self):
        if self.active:
            self.active = False
            self.current_turn = None

    def set_score(self, category, score):
        try:
            self.board.add_score(category, score)
        except CategoryPlayedError as e:
            raise e

