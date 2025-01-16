import pytest
from game.board import Board
from game.categories import Category
from game.exceptions import CategoryPlayedError


def test_init():
    board1 = Board()
    assert board1.get_score() == 0
    assert len(board1.get_categories_score()) == 13
    for i in range(0, 13):
        assert board1.get_categories_score()[i] == 0

    cat_score = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board2 = Board(cat_score, 3)
    assert board2.get_score() == 3
    assert board2.get_categories_score()== cat_score

def test_add_score_valid():
    cat_score = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board = Board(cat_score, 3)
    board.add_score(Category.TWO, 4)
    assert board.get_score() == 7
    assert board.get_categories_score() == [3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def test_add_score_invalid():
    cat_score = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board = Board(cat_score, 3)
    with pytest.raises(CategoryPlayedError) as e:
        board.add_score(Category.ONE, 4)
    assert str(e.value) == "Score for category 'ONE' is already set."
    assert board.get_score() == 3
    assert board.get_categories_score() == cat_score
