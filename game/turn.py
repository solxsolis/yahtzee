from game.dice import Die
from game.categories import Category

class Turn:
    def __init__(self, player):
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
            if all(self.dice_values_count[i+j] > 0 for j in range (0, 3)):
                return 40
        return 0



