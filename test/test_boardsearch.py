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
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS", "RETEST"])
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
    board = BoardSearch( board_data, "TESR", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 4
    assert (1, 0, 11, "TEST") in valid_words
    assert (1, 0, 13, "SET") in valid_words
    assert (1, 0, 14, "TEST") in valid_words
    assert (0, 0, 9, "RETEST") in valid_words

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

def test_central():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("      T        "),
            tuple("      E        "),
            tuple("      S        "),
            tuple("      T        "),
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
    assert len(valid_words) == 10
    assert (0, 3, 4, "SET") in valid_words
    assert (0, 3, 3, "TEST") in valid_words
    assert (0, 3, 6, "TEST") in valid_words
    assert (0, 4, 5, "SET") in valid_words
    assert (0, 5, 6, "SET") in valid_words
    assert (0, 6, 4, "SET") in valid_words
    assert (0, 6, 3, "TEST") in valid_words
    assert (0, 6, 6, "TEST") in valid_words
    assert (0, 7, 6, "SET") in valid_words
    assert (1, 3, 6, "TESTS") in valid_words

def test_blank_small():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("      T        "),
            tuple("      E        "),
            tuple("      S        "),
            tuple("      T        "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "_", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 1
    assert (1, 3, 6, "TESTS") in valid_words

def test_blank_big():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("      T        "),
            tuple("      E        "),
            tuple("      S        "),
            tuple("      T        "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    board = BoardSearch( board_data, "TE_", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 11
    assert (0, 3, 4, "SET") in valid_words
    assert (0, 3, 3, "TEST") in valid_words
    assert (0, 3, 6, "TEST") in valid_words
    assert (0, 4, 5, "SET") in valid_words
    assert (0, 5, 6, "SET") in valid_words
    assert (0, 5, 4, "TEST") in valid_words
    assert (0, 6, 4, "SET") in valid_words
    assert (0, 6, 3, "TEST") in valid_words
    assert (0, 6, 6, "TEST") in valid_words
    assert (0, 7, 6, "SET") in valid_words
    assert (1, 3, 6, "TESTS") in valid_words
