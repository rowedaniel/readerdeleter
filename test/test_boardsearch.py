import random

from readerdeleter.gaddag import generate_GADDAG
from readerdeleter.build.boardsearch import BoardSearch



def test_corner1_horizontal():
    gaddag = generate_GADDAG(["test", "set", "tests"])
    board_data = (
            tuple("test           "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "tes", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (0, 0, 0, "tests") in valid_words
    assert (1, 0, 0, "test") in valid_words
    assert (1, 0, 2, "set") in valid_words
    assert (1, 0, 3, "test") in valid_words
    assert (1, 0, 4, "set") in valid_words

def test_corner1_vertical():
    gaddag = generate_GADDAG(["test", "set", "tests"])
    board_data = (
            tuple("t              "),
            tuple("e              "),
            tuple("s              "),
            tuple("t              "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "tes", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 0, "tests") in valid_words
    assert (0, 0, 0, "test") in valid_words
    assert (0, 2, 0, "set") in valid_words
    assert (0, 3, 0, "test") in valid_words
    assert (0, 4, 0, "set") in valid_words

def test_corner2_horizontal():
    gaddag = generate_GADDAG(["test", "set", "tests"])
    board_data = (
            tuple("           test"),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "tes", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 3
    assert (1, 0, 11, "test") in valid_words
    assert (1, 0, 13, "set") in valid_words
    assert (1, 0, 14, "test") in valid_words

def test_corner2_vertical():
    gaddag = generate_GADDAG(["test", "set", "tests"])
    board_data = (
            tuple("              t"),
            tuple("              e"),
            tuple("              s"),
            tuple("              t"),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "tes", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 14, "tests") in valid_words
    assert (0, 0, 11, "test") in valid_words
    assert (0, 0, 12, "set") in valid_words
    assert (0, 3, 11, "test") in valid_words
    assert (0, 3, 12, "set") in valid_words

