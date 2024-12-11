from readerdeleter.board import Board
from readerdeleter.gaddag import generate_GADDAG
from readerdeleter.build.dafsa import DAFSA

from .location import HORIZONTAL, VERTICAL, Location
from .board import DICTIONARY
from .gatekeeper import GateKeeper

ALPHABET_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_L = ALPHABET_U.lower()
ALPHABET_BLANK = ALPHABET_U + "_"
ALPHABET_UL = ALPHABET_U + ALPHABET_L

class BoardConverter:

    def __init__(self,
                 gatekeeper: GateKeeper|None =None,
                 gaddag: DAFSA=None,
                 board=None,
                 previous_board_data=None
                 ):
        self._gatekeeper = gatekeeper
        if gaddag is None:
            self._gaddag = generate_GADDAG(list(DICTIONARY))
        else:
            self._gaddag = gaddag
        self._board = board
        if previous_board_data is None:
            self._previous_board_data = [[" " for _ in range(15)] for _ in range(15)]
        else:
            self._previous_board_data = previous_board_data

    def _convert_hand(self, hand: list[str]) -> str:
        """ Convert Peter-style hand to readerdeleter-style """
        return ''.join(hand).upper()

    def _convert_letter(self, letter: str) -> str:
        return letter.upper() if letter in ALPHABET_UL else ' '

    def _is_blank(self, letter: str) -> bool:
        return letter in ALPHABET_U

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

    def set_gatekeeper(self, gatekeeper: GateKeeper, reset_data: bool = True) -> None:
        self._gatekeeper = gatekeeper
        if reset_data:
            self._board = Board(self._gaddag)
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


    def copy(self) -> 'BoardConverter':
        if self._board is None:
            raise ValueError("uninitialized board")
        board_copy = self._board.copy()
        prev_data_copy = [[c for c in row] for row in self._previous_board_data]
        return BoardConverter(self._gatekeeper, self._gaddag, board_copy, prev_data_copy)
