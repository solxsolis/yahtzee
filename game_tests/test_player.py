import pytest
from game.player import Player

def test_init():
    player1 = Player("Player1")
    player2 = Player("Player2", 100)
    assert player1.name == "Player1"
    assert player2.name == "Player2"
    assert player2.score == 100