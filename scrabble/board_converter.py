import readerdeleter.board
import readerdeleter.gaddag

from .location import *
from .board import *
from .move import *
from .gatekeeper import GateKeeper

FULL_ALPHABET = readerdeleter.board.ALPHABET + readerdeleter.board.ALPHABET.lower()

class BoardConverter:

    def __init__(self):
        self._gatekeeper = None
        self._gaddag = readerdeleter.gaddag.generate_GADDAG(list(DICTIONARY))
        self._board = None
        self._previous_board_data = [[" " for _ in range(15)] for _ in range(15)]

    def _convert_hand(self, hand: list[str]) -> str:
        """ Convert Peter-style hand to readerdeleter-style """
        return ''.join(hand).upper()

    def _convert_letter(self, letter: str) -> str:
        return letter.upper() if letter in FULL_ALPHABET else ' '

    def _is_blank(self, letter: str) -> bool:
        return letter in readerdeleter.board.ALPHABET

    def _convert_play(self, play: tuple[int, int, int, str, str]) -> tuple[str, Location, Location]:
        """ Convert readerdeleter-style hand to Peter-style """
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

        return (converted_word, Location(play[1], play[2]), direction)

    def set_gatekeeper(self, gatekeeper: GateKeeper) -> None:
        self._gatekeeper = gatekeeper
        self._board = readerdeleter.board.Board(self._gaddag)
        self._previous_board_data = [[" " for _ in range(15)] for _ in range(15)]


    def update_board(self) -> None:
        if self._gatekeeper is None or self._board is None:
            raise ValueError("uninitialized gatekeeper")
        for r in range(15):
            for c in range(15):
                space = self._gatekeeper.get_square(Location(r,c))
                if self._previous_board_data[r][c] != self._convert_letter(space):
                    self._previous_board_data[r][c] = self._convert_letter(space)
                    self._board.update_tile(r,c,self._convert_letter(space), self._is_blank(space))

    def get_plays(self) -> list[tuple[str, Location, Location]]:
        if self._gatekeeper is None or self._board is None:
            raise ValueError("gatekeeper uninitialized")
        hand = self._convert_hand(self._gatekeeper.get_hand())
        plays = self._board.get_plays(hand)
        return list(map(lambda p: self._convert_play(p), plays))

