import random

from readerdeleter.gaddag import generate_GADDAG
from readerdeleter.build.boardsearch import BoardSearch



def test_corner1_horizontal():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("TEST           "),
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
    board = BoardSearch( board_data, "TES", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (0, 0, 0, "TESTS") in valid_words
    assert (1, 0, 0, "TEST") in valid_words
    assert (1, 0, 2, "SET") in valid_words
    assert (1, 0, 3, "TEST") in valid_words
    assert (1, 0, 4, "SET") in valid_words

def test_corner1_vertical():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("T              "),
            tuple("E              "),
            tuple("S              "),
            tuple("T              "),
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
    board = BoardSearch( board_data, "TES", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 0, "TESTS") in valid_words
    assert (0, 0, 0, "TEST") in valid_words
    assert (0, 2, 0, "SET") in valid_words
    assert (0, 3, 0, "TEST") in valid_words
    assert (0, 4, 0, "SET") in valid_words

def test_corner2_horizontal():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("           TEST"),
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
    board = BoardSearch( board_data, "TES", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 3
    assert (1, 0, 11, "TEST") in valid_words
    assert (1, 0, 13, "SET") in valid_words
    assert (1, 0, 14, "TEST") in valid_words

def test_corner2_vertical():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("              T"),
            tuple("              E"),
            tuple("              S"),
            tuple("              T"),
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
    board = BoardSearch( board_data, "TES", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 14, "TESTS") in valid_words
    assert (0, 0, 11, "TEST") in valid_words
    assert (0, 0, 12, "SET") in valid_words
    assert (0, 3, 11, "TEST") in valid_words
    assert (0, 3, 12, "SET") in valid_words

