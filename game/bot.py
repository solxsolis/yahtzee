from game.player import Player
from game.categories import Category

from itertools import combinations
import random

class Bot(Player):
    def __init__(self, name):
        super().__init__(name)

    def play_turn(self):
        if not self.current_turn:
            self.start_turn()

        for i in range(0, 3):
            self.get_current_turn().roll()
            self.decide_toggle_dice(self.current_turn.dice, self.current_turn.rolls)

        best_category = self.pick_best_category(self.current_turn.dice)
        score = self.get_current_turn().get_score(best_category)
        self.set_score(best_category, score)

        self.end_turn()


    def decide_toggle_dice(self, current_dice, roll_number):
        best_hold = current_dice
        best_val = self.simulate_expected_value(current_dice, roll_number)

        for hold_combination in self.get_possible_holds(current_dice):
            val = self.simulate_expected_value(hold_combination, roll_number)
            if val > best_val:
                best_val = val
                best_hold = hold_combination
        return best_hold

    def pick_best_category(self, dice):
        best_category = None
        best_score = -float('inf')
        for category in self.board.get_categories():
            if category is None:
                score = self.current_turn.get_score(category)
                if score > best_score:
                    best_score = score
                    best_category = category
        return best_category

    def simulate_expected_value(self, current_dice, simulation_count=1000):
        total_score = 0
        dice_to_roll = 5 - len(current_dice)

        for _ in range(simulation_count):
            dice = current_dice.copy()
            rolls_left = self.current_turn.rolls
            for _ in range(rolls_left):
                new_dice = [random.randint(1, 6) for _ in range(dice_to_roll)]
                dice = current_dice + new_dice

            score = self.current_turn.get_score(dice)
            total_score += score

        expected_value = total_score / simulation_count
        return expected_value

    def get_possible_holds(self, dice):
        # todo only keep "useful" rolls, not to iterate through all of them
        n = len(dice)
        holds = []

        for i in range(n+1):
            for idx in combinations(range(n), i):
                hold = [dice[j] for j in idx]
                holds.append(tuple(sorted(hold)))
        unique = list(set(holds))
        return [list(hold) for hold in unique]


