import pytest
from unittest.mock import patch
from game.dice import Die

def test_die_initialization():
    die = Die(idx=1)
    assert die.get_idx() == 1
    assert die.get_active() is True
    assert die.get_value() == 0

def test_die_toggle():
    die = Die(idx=1)
    assert die.get_active() is True
    die.toggle()
    assert die.get_active() is False
    die.toggle()
    assert die.get_active() is True

def test_roll():
    die = Die(idx=1)
    with patch("random.randint", return_value=5):
        die.roll()
        assert die.get_value() == 5

def test_roll_range():
    die = Die(idx=1)
    for _ in range(100):
        die.roll()
        assert 1 <= die.get_value() <= 6





