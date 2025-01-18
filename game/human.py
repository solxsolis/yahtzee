from game.player import Player


class Human(Player):
    def __init__(self, name, gui=None):
        super().__init__(name)
        self.gui = gui


    def play_turn(self):
        if not self.current_turn:
            self.start_turn()

        while self.current_turn.get_rolls() > 0:
            self.current_turn.roll()
            break

        pass



