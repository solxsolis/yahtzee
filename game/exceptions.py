from game.categories import Category
from game.player import Player

class CategoryPlayedError(Exception):
    def __init__(self, category):
        super().__init__(f"Score for category '{category.name}' is already set.")

class NoTurnsLeftError(Exception):
    def __init__(self, player):
        super().__init__(f"Player '{player.name}' has no turns left.")