from game.exceptions import CategoryPlayedError
from game.categories import Category

class Board:
    def __init__(self, categories_score=None, score = 0):
        if categories_score:
            self.categories_score = categories_score
        else:
            self.categories_score = [None]*13
        self.score = score
        self.yahtzee = False
        self.bonus = 0

    def get_categories_score(self):
        return self.categories_score

    def get_score(self):
        return self.score

    def get_yahtzee(self):
        return self.yahtzee

    def get_bonus(self):
        return self.bonus

    def add_score(self, category, score):
        if self.categories_score[category.value] is not None:
            raise CategoryPlayedError(category)
        self.categories_score[category.value] = score
        self.score += score
        if not self.yahtzee and category.value == "YAHTZEE" and score != 0:
            self.yahtzee = True
        if Category[category] in range (0, 6):
            self.bonus += score
        if self.bonus >= 63:
            self.score += 35




