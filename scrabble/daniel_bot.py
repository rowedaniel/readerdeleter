from .board_converter import BoardConverter, ALPHABET_BLANK
from .gatekeeper import GateKeeper
from .location import Location
from .move import PlayWord, ExchangeTiles
from .simulated_board import SimulatedBoard
from .simulated_gatekeeper import SimulatedGateKeeper

from typing import Self
import numpy as np
import random

class MonteCarloNode:
    # TODO: need to make  a simulated scrabble board for playouts
    def __init__(self,
                 player: int,
                 state: SimulatedBoard,
                 gatekeeper: SimulatedGateKeeper,
                 converter: BoardConverter,
                 opponent_hand_likelihoods: dict[str, float]):
        self.wins = 0
        self.sims = 0
        self.play = None
        self.player = player

        self.state = state
        self._gatekeeper = gatekeeper
        self.converter = converter

        self._parent = None
        self._op_hand_probs = opponent_hand_likelihoods
        self._plays = None

    def switch_player(self):
        self.player = 1 - self.player
        self._gatekeeper.set_player(self.player)
        

    def get_copy_with_play(self, play: PlayWord|ExchangeTiles) -> 'MonteCarloNode':
        new_player = 1 - self.player
        new_state = self.state.copy_and_play(play)
        new_gatekeeper = SimulatedGateKeeper(new_state, new_player)
        new_converter = self.converter.copy()
        new_converter.set_gatekeeper(new_gatekeeper, False)
        new_converter.update_board()
        # TODO: handle hand likelihoods
        new_node = MonteCarloNode(new_player, new_state, new_gatekeeper, new_converter, {})
        new_node.set_parent(self, play)
        return new_node

    def set_parent(self, parent: Self, play: PlayWord|ExchangeTiles):
        self._parent = parent
        self.play = play

    def get_plays(self) -> list[tuple[tuple[str, Location, Location], int]]:
        if self._plays is None:
            self._plays = self.get_fresh_plays()
        return self._plays

    def get_fresh_plays(self) -> list[tuple[tuple[str, Location, Location], int]]:
        return [(play, self._gatekeeper.score(*play)) for play in self.converter.get_plays()]

    def UCB(self) -> float:
        if self.sims == 0:
            return float('inf')
        exploitation = self.wins / self.sims
        if self._parent is not None:
            exploration = np.sqrt(2*np.log(self._parent.sims) / self.sims)
        else:
            exploration = np.sqrt(2)
        return exploitation + exploration

    def update(self, win: float):
        """
        update this node and all parents after simulation.
        win should be 1 in event of a win, and 0 otherwise
        """
        self.sims += 1
        self.wins += win
        if self._parent is not None:
            self._parent.update(1 - win)


class BaseBot:
    def __init__(self):
        self._gatekeeper = None
        self._board = BoardConverter()

    def set_gatekeeper(self, gatekeeper: GateKeeper):
        self._gatekeeper = gatekeeper
        self._board.set_gatekeeper(gatekeeper)


class Greedy(BaseBot):
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

class MonteCarlo(BaseBot):
    """
    Monte-Carlo using basic score as a heuristic for random play
    """

    def __init__(self):
        super().__init__()
        self._root = None
        self._states = []
        self._next_turn_states = []

    def choose_play_randomly(self, plays: list[tuple[tuple[str, Location, Location], int]]) -> PlayWord|ExchangeTiles:
        if len(plays) == 0:
            return ExchangeTiles([0, 1, 2, 3, 4, 5, 6])
        scores = [w for _,w in plays]
        max_score = max(scores)
        weights = [(w/max_score)**80 for _,w in plays]
        return PlayWord(*random.choices(plays, weights=weights)[0][0])

    def selection(self) -> MonteCarloNode:
        next_node = max(self._states, key=lambda node: node.UCB())
        print("selecting node", next_node)
        return next_node

    def expand(self, node: MonteCarloNode) -> MonteCarloNode:
        plays = node.get_plays()
        play = self.choose_play_randomly(plays)
        print("expanding node", node, "with scores", node.state.get_scores(), "with play", play, "for player", node.player)
        new_node = node.get_copy_with_play(play)
        return new_node

    def simulate(self, baseNode: MonteCarloNode) -> float:

        # copy node to get a fresh one for playouts
        play = self.choose_play_randomly(baseNode.get_plays())
        print('simulating')
        node = baseNode.get_copy_with_play(play)
        print("starting playout from node", node, "with scores", node.state.get_scores(), "with play", play)

        # playouts
        board = node.state
        converter = node.converter
        while not board.game_is_over():
            plays = node.get_fresh_plays()
            play = self.choose_play_randomly(plays)
            play.play(board, node.player)
            converter.update_board()
            node.switch_player()
        scores = board.get_scores()
        if scores[baseNode.player] > scores[1 - baseNode.player]:
            print("win for", baseNode.player)
            return 1 # win
        elif scores[baseNode.player] < scores[1 - baseNode.player]:
            print("loss for", baseNode.player)
            return 0 # loss
        return 0.0 # draw


    def search(self) -> MonteCarloNode:

        print("searching")

        for _ in range(50):
            node = self.selection()
            new_node = self.expand(node)
            win = self.simulate(new_node)
            new_node.update(win)
            if node is self._root:
                self._next_turn_states.append(new_node)
            self._states.append(new_node)


        for state in self._states:
            print(f"{state.wins} / {state.sims}: {state}", end="")
            n = state
            while n._parent is not None:
                n = n._parent
                print(f" --> {n}", end="")
            print()

        best_node = max(self._next_turn_states, key=lambda node: node.sims)
        print("best node:", best_node)
        return best_node




    def choose_move(self) -> PlayWord|ExchangeTiles:
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")
        print("choosing move")
        self._root = None
        self._states = []
        self._next_turn_states = []


        # update board
        self._board.update_board()

        # TODO: be more intelligent about opponent_hand_likelihoods
        opponent_hand_likelihoods = {c: 1/len(ALPHABET_BLANK) for c in ALPHABET_BLANK}

        # init states to just the root node (i.e. current board state)
        root_board = SimulatedBoard.from_gatekeeper(self._gatekeeper)
        root_gatekeeper = SimulatedGateKeeper(root_board, 0)
        root_converter = self._board.copy()
        root_converter.set_gatekeeper(root_gatekeeper, False)
        self._root = MonteCarloNode(0, root_board, root_gatekeeper, root_converter, opponent_hand_likelihoods)
        self._states = [self._root]
        self._next_turn_states = []

        best_node = self.search()
        print("done with choosing move! chose", best_node.play)
        if best_node.play is not None:
            return best_node.play
        return ExchangeTiles([0, 1, 2, 3, 4, 5, 6])



