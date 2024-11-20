from readerdeleter.board import Board
from readerdeleter.gaddag import generate_GADDAG


def test_permute_blank_one():
    board = Board(None)
    assert board.permute_blank_character('TEST', 'T', 1) == set(['_EST', 'TES_'])

def test_permute_blank_two():
    board = Board(None)
    assert board.permute_blank_character('TEST', 'T', 2) == set(['_ES_'])

def test_get_plays():
    board = Board(generate_GADDAG(["TEST", "TESTS", "TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("ED")) == set([(1, 0, 0, "....ED", "....ED")])

def test_get_plays_one_blank():
    board = Board(generate_GADDAG(["TEST", "TESTS", "TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("E_")) == set([(1, 0, 0, "....ED", "....E_"), (1, 0, 0, "....S", "...._")])

def test_get_plays_one_blank_impossible():
    board = Board(generate_GADDAG(["TEST", "TESTS", "TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("A_")) == set([(1, 0, 0, "....S", "...._")])

def test_get_plays_two_blanks():
    board = Board(generate_GADDAG(["TEST", "TESTS", "TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("__")) == set([(1, 0, 0, "....ED", "....__"), (1, 0, 0, "....S", "...._")])

def test_get_optional_blank():
    board = Board(generate_GADDAG(["TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("ED__")) == set([
        (1, 0, 0, "....ED", "....ED"),
        (1, 0, 0, "....ED", "....E_"),
        (1, 0, 0, "....ED", "...._D"),
        (1, 0, 0, "....ED", "....__"),
        ])

def test_get_mandatory_and_optional_blank():
    board = Board(generate_GADDAG(["TESTED"]))
    board.letters[0][0] = "T"
    board.letters[1][0] = "E"
    board.letters[2][0] = "S"
    board.letters[3][0] = "T"
    assert set(board.get_plays("D__")) == set([
        (1, 0, 0, "....ED", "...._D"),
        (1, 0, 0, "....ED", "....__"),
        ])
