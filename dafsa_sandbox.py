import time

from readerdeleter.build.boardsearch import BoardSearch
from readerdeleter.gaddag import generate_GADDAG

def print_board(b):
    print('   ' + ''.join(str(i)[-1] for i in range(15)))
    for i, row in enumerate(b):
        print(f'{i:<3} ' + ''.join(row))


words = ["hunch", "hunched"]


print("generating gaddag")
t = time.time()
gaddag = generate_GADDAG(words)
print("took", time.time() - t)

board_data = (
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("   HUNCH       "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
        tuple("               "),
    )


print("generating boardsearch")
t = time.time()
board = BoardSearch( board_data, "ED", gaddag)
print("took", time.time() - t)


print("getting valid words")
t = time.time()
valid_words = board.get_valid_words()
print("took", time.time() - t)


print_board(board_data)
for (direction, r,c,word) in set(valid_words):
    print(("horizontal", "vertical")[direction], r, c, word)
    new_board = [[board_data[i][j] for j in range(15)] for i in range(15)]
    dx = 1 if direction else 0
    dy = 0 if direction else 1
    for i in range(len(word)):
        new_board[r+dx*i][c+dy*i] = word[i]
    print_board(new_board)
