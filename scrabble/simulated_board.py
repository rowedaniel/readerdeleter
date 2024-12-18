from .board import Board
from .board_converter import ALPHABET_U, ALPHABET_L
from .move import PlayWord, ExchangeTiles
from .location import Location
from .gatekeeper import GateKeeper

import random
from typing import Self

TOTAL_LETTERS = 'aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmmnnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz__'
LETTER_COUNT = {
        c: TOTAL_LETTERS.count(c) for c in set(TOTAL_LETTERS)
        }

class SimulatedBoard(Board):
    @classmethod
    def from_gatekeeper(cls, gatekeeper: GateKeeper) -> Self:
        squares = [[gatekeeper.get_square(Location(r, c)) for c in range(15)] for r in range(15)]
        hand = gatekeeper.get_hand()
        hands = [hand, None]
        scores = [gatekeeper.get_my_score(), gatekeeper.get_opponent_score()]
        current_player = 0
        return cls(squares, hands, scores, current_player)

    def __init__(self,
                 squares: list[list[str]],
                 hands: list[list[str]|None],
                 scores: list[int],
                 current_player: int,
                 ):
    
        # Get list of unseen letters
        unseen_letters = {c: v for c,v in LETTER_COUNT.items()}
        for row in squares:
            for square in row:
                if square in ALPHABET_U:
                    unseen_letters["_"] -= 1
                elif square in ALPHABET_L:
                    unseen_letters[square] -= 1
        for hand in hands:
            if hand is None:
                continue
            for letter in hand:
                unseen_letters[letter] -= 1
        self.known_hands = [hand is None for hand in hands]


        # for now, just deal opponent hand randomly
        self._squares = [[square for square in row] for row in squares]
        self._bag = list(''.join([c*v for c,v in unseen_letters.items()]))
        random.shuffle(self._bag)
        self._hands = [[] if hand is None else hand.copy() for hand in hands]
        for i,hand in enumerate(hands):
            if hand is None:
                self._deal(self._hands[i], 7)
        self._scores = list(scores)
        self._current_player = current_player
        self._number_of_passes = 0
        self._last_move = None

    def copy_and_play(self, move: PlayWord|ExchangeTiles) -> 'SimulatedBoard':
        hands = [None if kh and p != self._current_player else hand\
                for p,(kh, hand) in enumerate(zip(self.known_hands, self._hands))]
        new_board = SimulatedBoard(
                self._squares,
                hands,
                self._scores,
                self._current_player)
        move.play(new_board, self._current_player)
        return new_board

        
