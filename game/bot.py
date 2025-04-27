from game.player import Player
from game.categories import Category
from game.turn import Turn

from itertools import combinations
import random

class Bot(Player):
    SIMULATIONS = 500

    def __init__(self, name):
        super().__init__(name)

    def play_turn(self):
        if not self.current_turn:
            self.start_turn()

        turn = self.get_current_turn()
        turn.roll()

        while turn.get_rolls() > 0:
            hold_idx = self.decide_toggle_dice(turn.get_dice(), turn.get_rolls())
            for die in turn.get_dice():
                should_hold = die.get_idx() in hold_idx
                if should_hold and die.get_active():
                    die.toggle()
                elif not should_hold and not die.get_active():
                    die.toggle()
            turn.roll()

        best_category = self.pick_best_category([d.get_value() for d in turn.get_dice()])
        score = turn.get_score(best_category)
        self.set_score(best_category, score)

        self.end_turn()


    def decide_toggle_dice(self, current_dice, rolls_left):
        best_hold = ()
        best_val = self.simulate_expected_value([d.get_value() for d in current_dice], best_hold, rolls_left)

        for r in range(6):
            for hold_idxs in combinations(range(5), r):
                vals = self.simulate_expected_value([d.get_value() for d in current_dice], hold_idxs, rolls_left)
                if vals > best_val:
                    best_val, best_hold = vals, hold_idxs
        return best_hold

    def pick_best_category(self, dice_vals):
        best_category = None
        best_score = -float('inf')
        for category in Category:
            if self.board.categories_score[category.value] is None:
                tmp = Turn(yahtzee=self.board.get_yahtzee())
                tmp.dice_values = dice_vals
                tmp.dice_values_count = [dice_vals.count(v) for v in range(1, 7)]
                score = tmp.get_score(category)
                if score > best_score:
                    best_score = score
                    best_category = category
        return best_category

    def simulate_expected_value(self, base_vals, hold_idxs, rolls_left):
        total_score = 0
        held = [base_vals[i] for i in hold_idxs]
        for _ in range(self.SIMULATIONS):
            dice = held[:]
            for _ in range(rolls_left):
                dice += [random.randint(1, 6) for _ in range(5-len(held))]
            sim = Turn(yahtzee=self.board.get_yahtzee())
            sim.dice_values = dice
            sim.dice_values_count = [dice.count(v) for v in range(1, 7)]
            cat = self.pick_best_category(dice)
            total_score += sim.get_score(cat)

        return total_score / self.SIMULATIONS

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


