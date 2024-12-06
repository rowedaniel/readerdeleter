from .board_converter import BoardConverter
from .gatekeeper import GateKeeper
from .location import *
from .board import *
from .move import *

class ReaderDeleter:
    """
    For now, greedy
    """

    def __init__(self):
        self._gatekeeper = None
        self._board = BoardConverter()

    def set_gatekeeper(self, gatekeeper: GateKeeper):
        self._gatekeeper = gatekeeper
        self._board.set_gatekeeper(gatekeeper)

    def choose_move(self) -> PlayWord|ExchangeTiles:
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")

        # update board
        self._board.update_board()

        moves = self._board.get_plays()
        max_move = None
        max_score = 0
        for move in moves:
            score = self._gatekeeper.score(*move)
            if score > max_score or \
               max_move is None or \
               (score == max_score and move[0] > max_move[0]):
                max_move = move
                max_score = score

        if max_move is None:
            return ExchangeTiles([0, 1, 2, 3, 4, 5, 6])
        return PlayWord(*max_move)

