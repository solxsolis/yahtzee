from game.exceptions import CategoryPlayedError

class Board:
    def __init__(self, categories_score=None, score = 0):
        if categories_score:
            self.categories_score = categories_score
        else:
            self.categories_score = [None]*13
        self.score = score

    def get_categories_score(self):
        return self.categories_score

    def get_score(self):
        return self.score

    def add_score(self, category, score):
        if self.categories_score[category.value] is not None:
            raise CategoryPlayedError(category)
        self.categories_score[category.value] = score
        self.score += score



