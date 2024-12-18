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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TES")))
    print(valid_words)
    assert len(valid_words) == 5
    assert (0, 0, 0, "....S") in valid_words
    assert (1, 0, 0, ".EST") in valid_words
    assert (1, 0, 2, ".ET") in valid_words
    assert (1, 0, 3, ".EST") in valid_words
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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TES")))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 0, "....S") in valid_words
    assert (0, 0, 0, ".EST") in valid_words
    assert (0, 2, 0, ".ET") in valid_words
    assert (0, 3, 0, ".EST") in valid_words
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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TESR")))
    print(valid_words)
    assert len(valid_words) == 4
    assert (1, 0, 11, ".EST") in valid_words
    assert (1, 0, 13, ".ET") in valid_words
    assert (1, 0, 14, ".EST") in valid_words
    assert (0, 0, 9, "RE....") in valid_words

def test_corner2_vertical():
    # TODO: sometimes segfaults--figure out why
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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TES")))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 14, "....S") in valid_words
    assert (0, 0, 11, "TES.") in valid_words
    assert (0, 0, 12, "SE.") in valid_words
    assert (0, 3, 11, "TES.") in valid_words
    assert (0, 3, 12, "SE.") in valid_words

def test_hook_hang():
    gaddag = generate_GADDAG(["AAAA", "AB", "BA", "BBCB"])
    board_data = (
            tuple("               "),
            tuple("AAAA           "),
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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("BBBC")))
    print(valid_words)
    assert len(valid_words) == 12
    assert (0, 0, 2, "BBCB") in valid_words
    assert (0, 0, 3, "BBCB") in valid_words
    assert (0, 2, 2, "BBCB") in valid_words
    assert (0, 2, 3, "BBCB") in valid_words
    assert (1, 0, 0, "B.") in valid_words
    assert (1, 0, 1, "B.") in valid_words
    assert (1, 0, 2, "B.") in valid_words
    assert (1, 0, 3, "B.") in valid_words
    assert (1, 1, 0, ".B") in valid_words
    assert (1, 1, 1, ".B") in valid_words
    assert (1, 1, 2, ".B") in valid_words
    assert (1, 1, 3, ".B") in valid_words

def test_hook_stop():
    gaddag = generate_GADDAG(["AAAC", "AB", "BA", "CC", "BBC"])
    board_data = (
            tuple("               "),
            tuple("AAAC           "),
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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("BBC")))
    print(valid_words)
    assert len(valid_words) == 10
    assert (0, 0, 1, "BBC") in valid_words
    assert (0, 2, 1, "BBC") in valid_words
    assert (1, 0, 0, "B.") in valid_words
    assert (1, 0, 1, "B.") in valid_words
    assert (1, 0, 2, "B.") in valid_words
    assert (1, 0, 3, "C.") in valid_words
    assert (1, 1, 0, ".B") in valid_words
    assert (1, 1, 1, ".B") in valid_words
    assert (1, 1, 2, ".B") in valid_words
    assert (1, 1, 3, ".C") in valid_words

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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TES")))
    print(valid_words)
    assert len(valid_words) == 10
    assert (0, 3, 4, "SE.") in valid_words
    assert (0, 3, 3, "TES.") in valid_words
    assert (0, 3, 6, ".EST") in valid_words
    assert (0, 4, 5, "S.T") in valid_words
    assert (0, 5, 6, ".ET") in valid_words
    assert (0, 6, 4, "SE.") in valid_words
    assert (0, 6, 3, "TES.") in valid_words
    assert (0, 6, 6, ".EST") in valid_words
    assert (0, 7, 6, "SET") in valid_words
    assert (1, 3, 6, "....S") in valid_words

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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("_")))
    print(valid_words)
    assert len(valid_words) == 1
    assert (1, 3, 6, "....S") in valid_words

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
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("TE_")))
    print(valid_words)
    assert len(valid_words) == 11
    assert (0, 3, 4, "SE.") in valid_words
    assert (0, 3, 3, "TES.") in valid_words
    assert (0, 3, 6, ".EST") in valid_words
    assert (0, 4, 5, "S.T") in valid_words
    assert (0, 5, 6, ".ET") in valid_words
    assert (0, 5, 4, "TE.T") in valid_words
    assert (0, 6, 4, "SE.") in valid_words
    assert (0, 6, 3, "TES.") in valid_words
    assert (0, 6, 6, ".EST") in valid_words
    assert (0, 7, 6, "SET") in valid_words
    assert (1, 3, 6, "....S") in valid_words


def test_empty_firstturn():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data = (
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
            tuple("               "),
        )
    board = BoardSearch( board_data, gaddag)
    valid_words = list(set(board.get_valid_words("SET")))
    print(valid_words)
    assert len(valid_words) == 6


def test_update_vert():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data_pre = (
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
            tuple("               "),
        )

    board_data_post = (
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("       S       "),
            tuple("       E       "),
            tuple("       T       "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    pre = BoardSearch(board_data_pre, gaddag);
    post = BoardSearch(board_data_post, gaddag);

    pre.update_cross_check(6, 7, 'S')
    pre.update_cross_check(7, 7, 'E')
    pre.update_cross_check(8, 7, 'T')
    assert set(pre.get_valid_words("TEST")) == set(post.get_valid_words("TEST"))

def test_update_hori():
    gaddag = generate_GADDAG(["TEST", "SET", "TESTS"])
    board_data_pre = (
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
            tuple("               "),
        )

    board_data_post = (
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("      SET      "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
            tuple("               "),
        )
    pre = BoardSearch(board_data_pre, gaddag);
    post = BoardSearch(board_data_post, gaddag);

    pre.update_cross_check(7, 6, 'S')
    pre.update_cross_check(7, 7, 'E')
    pre.update_cross_check(7, 8, 'T')
    assert set(pre.get_valid_words("TEST")) == set(post.get_valid_words("TEST"))


