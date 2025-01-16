from game.dice import Die
from game.categories import Category
from game.turn import Turn
from game.exceptions import CategoryPlayedError

class Board:
    def __init__(self, categories_score=None, score = 0):
        if categories_score:
            self.categories_score = categories_score
        else:
            self.categories_score = []
            for i in range (0, 13):
                self.categories_score.append(0)
        self.score = score

    def get_categories_score(self):
        return self.categories_score

    def get_score(self):
        return self.score

    def add_score(self, category, score):
        if self.categories_score[category.value] != 0:
            raise CategoryPlayedError(category)
        self.categories_score[category.value] = score
        self.score += score




