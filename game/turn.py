from game.dice import Die
from game.categories import Category

class Turn:
    def __init__(self, player, yahtzee=False):
        self.player = player
        self.rolls = 3
        self.dice = []
        for idx in range (0, 5):
            curr_die = Die(idx)
            self.dice.append(curr_die)
        self.dice_values = []
        for _ in range (0, 5):
            self.dice_values.append(0)
        self.dice_values_count = []
        for _ in range (0, 6):
            self.dice_values_count.append(0)
        self.yahtzee = yahtzee

    def get_player(self):
        return self.player

    def get_rolls(self):
        return self.rolls

    def get_dice(self):
        return self.dice

    def get_dice_values(self):
        return self.dice_values

    def get_dice_values_count(self):
        return self.dice_values_count

    def get_yahtzee(self):
        return self.yahtzee

    def toggle(self, idx):
        self.dice[idx].toggle()

    def update_values(self):
        for i in range (0, 5):
            self.dice_values[i] = self.dice[i].get_value()
        for i in range (0, 6):
            self.dice_values_count[i] = self.dice_values.count(i+1)


    def roll(self):
        if self.rolls > 0:
            for die in self.dice:
                if die.get_active():
                    die.roll()
            self.rolls -= 1

        self.update_values()


    def calculate_digits(self, digit):
        return self.dice_values_count[digit-1] * digit

    def calculate_sum(self):
        result = 0
        for value in self.dice_values:
            result += value
        return result

    def calculate_xn(self, n):
        for count in self.dice_values_count:
            if count >= n:
                if n == 5:
                    return 50
                return self.calculate_sum()
        return 0

    def calculate_house(self):
        if 3 in self.dice_values_count and 2 in self.dice_values_count:
            return 25
        return 0

    def calculate_small_street(self):
        for i in range(0, 3):
            if all(self.dice_values_count[i+j] > 0 for j in range (0, 4)):
                return 30
        return 0

    def calculate_large_street(self):
        for i in range(0, 2):
            if all(self.dice_values_count[i+j] > 0 for j in range (0, 5)):
                return 40
        return 0

    def get_score(self, cat):
        add = 0
        if self.calculate_xn(5) == 50:
            add = 50
        if cat == Category.ONE:
            return self.calculate_digits(1) + add
        elif cat == Category.TWO:
            return self.calculate_digits(2) + add
        elif cat == Category.THREE:
            return self.calculate_digits(3) + add
        elif cat == Category.FOUR:
            return self.calculate_digits(4) + add
        elif cat == Category.FIVE:
            return self.calculate_digits(5) + add
        elif cat == Category.SIX:
            return self.calculate_digits(6) + add
        elif cat == Category.X3:
            return self.calculate_xn(3) + add
        elif cat == Category.X4:
            return self.calculate_xn(4) + add
        elif cat == Category.HOUSE:
            return self.calculate_house() + add
        elif cat == Category.SMALL_STREET:
            return self.calculate_small_street() + add
        elif cat == Category.LARGE_STREET:
            return self.calculate_large_street() + add
        elif cat == Category.YAHTZEE:
            return self.calculate_xn(5)
        elif cat == Category.CHANCE:
            return self.calculate_sum() + add




