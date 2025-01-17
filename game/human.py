from game.player import Player
from game.turn import Turn
from game.categories import Category
from game.exceptions import *

class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def play_turn(self):
        print(f'Player {self.name} turn')
        keep_str = ""
        while self.current_turn.get_rolls() > 0:
            self.current_turn.roll()
            dice_values = self.current_turn.get_dice_values()
            for die in dice_values:
                print(f'{die}', end=' ')
            print("Enter the indexes of the dice to toggle\n")
            print("If you want to play a category type play")
            keep_str = input()
            if keep_str == "play":
                break
            keep_dice = list(map(int, keep_str.split()))
            for die in keep_dice:
                self.current_turn.dice[die].toggle()
        print("Type a category")
        cat_type = input().upper()
        if cat_type not in Category.__members__:
            raise CategoryDoesNotExistError(cat_type)
        cat = Category[cat_type]
        score = self.current_turn.get_score(cat)
        self.board.add_score(cat, score)

