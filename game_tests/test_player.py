import pytest
from game.player import Player

def test_init():
    player1 = Player("Player1")
    player2 = Player("Player2", 100)
    assert player1.get_name() == "Player1"
    assert player2.get_name() == "Player2"
    assert player2.get_score() == 100