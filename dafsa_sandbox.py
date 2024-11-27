import time

from readerdeleter.gaddag import generate_GADDAG
from readerdeleter.board import Board



with open("resources/sample_wordlist_processed.txt", "r") as file:
    words = [word.strip() for word in file.readlines() if 'z' not in word]
# words = ["TEST", "TESTS"]


print("generating gaddag")
t = time.time()
gaddag = generate_GADDAG(words)
print("took", time.time() - t)

board_data = [
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("               "),
            list("  BAGS         "),
            list("               "),
            list("   T           "),
            list("               "),
            list("               "),
        ]


print("generating boardsearch")
t = time.time()
board = Board(gaddag, board_data)
print("took", time.time() - t)


print("getting valid words")
t = time.time()
plays = board.get_plays("COO")
print("got", len(plays), "words")
print("took", time.time() - t)

print("gettings scores")
t = time.time()
scores = [board.score_play(play) for play in plays]
print("took", time.time() - t)


print(board)
for score, play in sorted(zip(scores, plays)):
    print('\nscore:', score)
    board_copy = Board(gaddag, [[c for c in row] for row in board_data])
    board_copy.play(play)
    print(board_copy)
