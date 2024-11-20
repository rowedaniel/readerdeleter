import time

from readerdeleter.build.boardsearch import BoardSearch
from readerdeleter.gaddag import generate_GADDAG

for _ in range(100000):
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
    board = BoardSearch( board_data, "TES", gaddag)
    valid_words = list(set(board.get_valid_words()))
    print(valid_words)
    assert len(valid_words) == 5
    assert (1, 0, 14, "....S") in valid_words
    assert (0, 0, 11, "TES.") in valid_words
    assert (0, 0, 12, "SE.") in valid_words
    assert (0, 3, 11, "TES.") in valid_words
    assert (0, 3, 12, "SE.") in valid_words

#
# def print_board(b):
#     print('    ' + ''.join(str(i)[-1] for i in range(15)))
#     for i, row in enumerate(b):
#         print(f'{i:<3} ' + ''.join(row))
#
#
# with open("resources/sample_wordlist_processed.txt", "r") as file:
#     words = [word.strip() for word in file.readlines() if 'z' not in word]
#
#
# print("generating gaddag")
# t = time.time()
# gaddag = generate_GADDAG(words)
# print("took", time.time() - t)
#
# board_data = (
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("      T        "),
#             tuple("      E        "),
#             tuple("      S        "),
#             tuple("      T        "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#             tuple("               "),
#         )
#
#
# print("generating boardsearch")
# t = time.time()
# board = BoardSearch( board_data, "SIQRWXA", gaddag)
# print("took", time.time() - t)
#
#
# print("getting valid words")
# t = time.time()
# valid_words = board.get_valid_words()
# print("got", len(valid_words), "words (", len(set(valid_words)), ") without duplicates")
# print("took", time.time() - t)
#
#
# print_board(board_data)
# for (direction, r,c,word) in set(valid_words):
#     print(("horizontal", "vertical")[direction], r, c, word)
#     new_board = [[board_data[i][j] for j in range(15)] for i in range(15)]
#     dx = 1 if direction else 0
#     dy = 0 if direction else 1
#     for i in range(len(word)):
#         new_board[r+dx*i][c+dy*i] = word[i]
#     print_board(new_board)
