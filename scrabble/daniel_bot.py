import readerdeleter.board
import readerdeleter.gaddag

from .location import *
from .board import *
from .move import *

class ReaderDeleter:
    """
    For now, greedy
    """

    def __init__(self):
        self._gatekeeper = None
        self._gaddag = readerdeleter.gaddag.generate_GADDAG(list(DICTIONARY))
        self._board = readerdeleter.board.Board(self._gaddag)

    def set_gatekeeper(self, gatekeeper):
        self._gatekeeper = gatekeeper


    def _convert_board(self):
        orig_board_data = [[self._gatekeeper.get_square(Location(r, c))
                            for c in range(15)]
                           for r in range(15)]
        # TODO: manage blanks
        board_data = [
                [ space.upper() if space in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' else ' '
                    for space in row
                 ] for row in orig_board_data]
        self._board = readerdeleter.board.Board(self._gaddag, board_data)


    def choose_move(self):
        # update board
        self._convert_board()

        hand = self._convert_hand(self._gatekeeper.get_hand())
        moves = self._board.get_plays(hand)
        max_move = None
        max_score = 0
        max_move_orig = None
        for move in moves:
            move_converted = self._convert_play(move)
            score = self._gatekeeper.score(move_converted._word,
                                           move_converted._location,
                                           move_converted._direction)
            if score > max_score or score == max_score and move_converted._word > max_move._word:
                max_move = move_converted
                max_score = score
                max_move_orig = move

        if max_move is None:
            return ExchangeTiles([0, 1, 2, 3, 4, 5, 6])
        return max_move

    def _convert_hand(self, hand: list[str]) -> str:
        return ''.join(hand).upper()

    def _convert_play(self, play: tuple[int, int, int, str, str]) -> PlayWord:
        """
        For now, always play
        """
        with_blanks = play[-1]

        converted_word = play[-2]
        converted_word = converted_word.lower()
        converted_word = converted_word.replace('.', ' ')
        for i in range(len(converted_word)):
            if with_blanks[i] == "_":
                converted_word = converted_word[:i] + \
                                 converted_word[i].upper() + \
                                 converted_word[i+1:]
        direction = HORIZONTAL if play[0] == 0 else VERTICAL

        return PlayWord(converted_word, Location(play[1], play[2]), direction)

