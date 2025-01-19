from game.player import Player
from game.categories import Category

class Bot(Player):
    def __init__(self, name):
        super().__init__(name)

    def play_turn(self):
        if not self.current_turn:
            self.start_turn()

        for i in range(0, 3):
            self.get_current_turn().roll()
            self.decide_toggle_dice()

        best_category = self.pick_best_category()
        score = self.get_current_turn().get_score(best_category)
        self.set_score(best_category, score)

        self.end_turn()


    def decide_toggle_dice(self):
        pass

    def pick_best_category(self):
        return 0