import random

class Die:
    def __init__(self, idx):
        self.idx = idx
        self.active = True
        self.value = 0

    def get_idx(self):
        return self.idx

    def get_active(self):
        return self.active

    def get_value(self):
        return self.value

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def roll(self):
        self.value = random.randint(1,6)
