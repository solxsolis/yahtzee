from game.categories import Category

class CategoryPlayedError(Exception):
    def __init__(self, category):
        super().__init__(f"Score for category '{category.name}' is already set.")

class NoTurnsLeftError(Exception):
    def __init__(self, player):
        super().__init__(f"Player '{player}' has no turns left.")

class CategoryDoesNotExistError(Exception):
    def __init__(self, category):
        super().__init__(f"Category '{category}' does not exist.")

class NoRollsLeftError(Exception):
    def __init__(self, message="No rolls left."):
        super().__init__(message)

class ScoringError(Exception):
    def __init__(self, message = "Scoring error"):
        super().__init__(message)