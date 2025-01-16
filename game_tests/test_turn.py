import pytest
from unittest.mock import patch, MagicMock, mock_open
from game.turn import Turn
from game.dice import Die

def test_init():
    turn = Turn("human")
    assert turn.get_player() == "human"
    assert turn.get_rolls() == 3
    dice_arr = turn.get_dice()
    assert len(dice_arr) == 5
    for die in dice_arr:
        assert isinstance(die, Die)
    val_arr = turn.get_dice_values()
    assert len(val_arr) == 5
    for val in val_arr:
        assert val == 0
    count_arr = turn.get_dice_values_count()
    assert len(count_arr) == 6
    for val in count_arr:
        assert val == 0

def test_toggle():
    turn = Turn("human")
    dice_arr = turn.get_dice()
    active_status = dice_arr[0].get_active()
    turn.toggle(0)
    assert dice_arr[0].get_active() != active_status


def test_update_values():
    turn = Turn("human")

    mocked_values = [1, 2, 3, 4, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.get_dice_values() == mocked_values

    expected_counts = [1, 1, 1, 1, 1, 0]
    assert turn.get_dice_values_count() == expected_counts


def test_roll_all():
    turn = Turn("human")

    for die in turn.get_dice():
        die.roll = MagicMock()
        die.get_active = MagicMock(return_value=True)

    turn.roll()

    for die in turn.get_dice():
        die.roll.assert_called_once()

    assert turn.get_rolls() == 2

    mocked_values = [1, 2, 3, 4, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.get_dice_values() == mocked_values
    expected_counts = [1, 1, 1, 1, 1, 0]
    assert turn.get_dice_values_count() == expected_counts

def test_roll_some():
    turn = Turn("human")

    for die in turn.get_dice():
        die.roll = MagicMock()
        die.get_active = MagicMock(return_value=False)

    turn.get_dice()[0].get_active = MagicMock(return_value=True)
    turn.get_dice()[1].get_active = MagicMock(return_value=True)
    turn.get_dice()[2].get_active = MagicMock(return_value=True)

    turn.roll()

    for i, die in enumerate(turn.get_dice()):
        if i in range (0, 3):
            die.roll.assert_called_once()
        else:
            die.roll.assert_not_called()

    assert turn.get_rolls() == 2

    mocked_values = [1, 0, 3, 0, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.get_dice_values() == mocked_values
    expected_counts = [1, 0, 1, 0, 1, 0]
    assert turn.get_dice_values_count() == expected_counts

def test_roll_none():
    turn = Turn("human")

    for die in turn.get_dice():
        die.roll = MagicMock()
        die.get_active = MagicMock(return_value=False)

    turn.roll()

    for die in turn.get_dice():
        die.roll.assert_not_called()

    assert turn.get_rolls() == 2

    mocked_values = [0, 0, 0, 0, 0]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.get_dice_values() == mocked_values
    expected_counts = [0, 0, 0, 0, 0, 0]
    assert turn.get_dice_values_count() == expected_counts

def test_roll_no_rolls():
    turn = Turn("human")

    turn.rolls = 0

    for die in turn.get_dice():
        die.roll = MagicMock()
        die.get_active = MagicMock(return_value=True)

    initial_dice_values = turn.get_dice_values().copy()
    initial_dice_values_count = turn.get_dice_values_count().copy()

    turn.roll()

    for die in turn.get_dice():
        die.roll.assert_not_called()

    assert turn.get_rolls() == 0

    assert turn.get_dice_values() == initial_dice_values
    assert turn.get_dice_values_count() == initial_dice_values_count

def test_calculate_digits():
    turn = Turn("human")

    mocked_values = [1, 1, 1, 1, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_digits(1) == 4
    assert turn.calculate_digits(2) == 0
    assert turn.calculate_digits(3) == 0
    assert turn.calculate_digits(4) == 0
    assert turn.calculate_digits(5) == 5
    assert turn.calculate_digits(6) == 0

def test_calculate_sum():
    turn = Turn("human")

    mocked_values = [1, 1, 2, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_sum() == 11

def test_calculate_x3():
    turn = Turn("human")

    mocked_values = [1, 1, 2, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(3) == 11

    mocked_values = [1, 1, 1, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(3) == 10

    mocked_values = [1, 2, 2, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(3) == 0

def test_calculate_x4():
    turn = Turn("human")

    mocked_values = [1, 1, 1, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(4) == 10

    mocked_values = [1, 1, 1, 1, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(4) == 5

    mocked_values = [1, 1, 2, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(4) == 0

def test_calculate_x5():
    turn = Turn("human")

    mocked_values = [1, 1, 1, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(5) == 0

    mocked_values = [1, 1, 1, 1, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_xn(5) == 50

def test_calculate_house():
    turn = Turn("human")

    mocked_values = [1, 1, 1, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_house() == 0

    mocked_values = [1, 1, 1, 1, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_house() == 0

    mocked_values = [1, 1, 6, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_house() == 25

def test_calculate_small_street():
    turn = Turn("human")

    mocked_values = [1, 1, 1, 6, 1]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_small_street() == 0

    mocked_values = [1, 2, 3, 4, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_small_street() == 30

    mocked_values = [1, 6, 2, 3, 4]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_small_street() == 30

    mocked_values = [2, 3, 5, 4, 4]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_small_street() == 30

    mocked_values = [3, 4, 4, 5, 6]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_small_street() == 30

def test_calculate_large_street():
    turn = Turn("human")

    mocked_values = [1, 2, 3, 4, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_large_street() == 40

    mocked_values = [6, 2, 3, 4, 5]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_large_street() == 40

    mocked_values = [1, 2, 3, 4, 4]
    for i, die in enumerate(turn.get_dice()):
        die.get_value = MagicMock(return_value=mocked_values[i])

    turn.update_values()

    assert turn.calculate_large_street() == 0
