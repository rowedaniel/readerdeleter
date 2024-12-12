from .board_converter import BoardConverter, ALPHABET_BLANK
from .gatekeeper import GateKeeper
from .location import Location
from .move import PlayWord, ExchangeTiles
from .simulated_board import SimulatedBoard
from .simulated_gatekeeper import SimulatedGateKeeper
from .board import TILE_VALUES

from typing import Self
import numpy as np
import random
import matplotlib.pyplot as plt
from networkx import Graph, draw, bfs_layout

class MonteCarloNode:
    # TODO: need to make  a simulated scrabble board for playouts
    def __init__(self,
                 player: int,
                 state: SimulatedBoard,
                 gatekeeper: SimulatedGateKeeper,
                 converter: BoardConverter,
                 opponent_hand_likelihoods: dict[str, float],
                 width: int = 6):

        """
        Monte Carlo node with progressive widening
        """

        self.wins = 0
        self.sims = 0
        self.play = None
        self.player = player

        self.state = state
        self._gatekeeper = gatekeeper
        self.converter = converter

        self._parent = None
        self.children = {}
        self._op_hand_probs = opponent_hand_likelihoods
        self._plays = None
        self._width = width

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
        return new_node

    def set_parent(self, parent: Self, play: PlayWord|ExchangeTiles):
        self._parent = parent
        self.play = play
        parent.set_child(self, play)

    def set_child(self, child: Self, play: PlayWord|ExchangeTiles):
        self.children[play] = child

    def get_plays(self) -> list[tuple[tuple[str, Location, Location], int]]:
        if self._plays is None:
            self._plays = self.get_fresh_plays()
        return self._plays

    def get_fresh_plays(self) -> list[tuple[tuple[str, Location, Location], int]]:
        return [(play, self._gatekeeper.score(*play)) for play in self.converter.get_plays()]

    def UCB(self) -> float:
        if self.sims == 0:
            return float('inf')
        if self._parent is None:
            return 0
        exploitation = self.wins / self.sims
        exploration = np.sqrt(2*np.log(self._parent.sims) / self.sims)
        return exploitation + exploration

    def is_leaf(self) -> bool:
        return len(self.children) < self._width

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
    def __init__(self, board: BoardConverter|None = None):
        self._gatekeeper = None
        if board is None:
            self._board = BoardConverter()
        else:
            self._board = board

    def set_gatekeeper(self, gatekeeper: GateKeeper):
        self._gatekeeper = gatekeeper
        self._board.set_gatekeeper(gatekeeper)


class Greedy(BaseBot):
    def __str__(self) -> str:
        return "Greedy"
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
            return ExchangeTiles([True] * 7)
        return PlayWord(*max_move)


class GreedyExit(Greedy):
    def __str__(self):
        return "Greedy (With early exit)"
    def choose_move(self) -> PlayWord|ExchangeTiles:
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")
        if type(self._gatekeeper.get_last_move()) == ExchangeTiles:
            print("opponent passed")
            hand = self._gatekeeper.get_hand()
            tile_values = sum(TILE_VALUES[c] for c in hand)
            if self._gatekeeper.get_my_score() > self._gatekeeper.get_opponent_score() + tile_values*2:
                print("winning, so quit whilst ahead")
                high_value_tiles = [(TILE_VALUES[c] >= 5) for c in hand]
                return ExchangeTiles(high_value_tiles)
        return super().choose_move()
                # Winning by more than double hand value, so likely to win if you pass and end game




class AntiGreedy(Greedy):
    def __str__(self) -> str:
        return "Generous"
    def choose_move(self) -> PlayWord|ExchangeTiles:
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")

        # update board
        self._board.update_board()

        moves = self._board.get_plays()
        min_move = None
        min_score = 0
        for move in moves:
            score = self._gatekeeper.score(*move)
            if score < min_score or \
               min_move is None or \
               (score == min_score and move[0] < min_move[0]):
                min_move = move
                min_score = score

        if min_move is None:
            return ExchangeTiles([True] * 7)
        return PlayWord(*min_move)

class MonteCarlo(BaseBot):
    """
    Monte-Carlo using basic score as a heuristic for random play
    """

    def __str__(self) -> str:
        return f"Monte Carlo (s={self._search_count})"

    def __init__(self, search_count: int = 25, board: BoardConverter|None = None):
        super().__init__(board)
        self._root = None
        self._search_count = search_count

    def choose_play_randomly(self,
                             node: MonteCarloNode,
                             plays: list[tuple[tuple[str, Location, Location], int]]
                             ) -> PlayWord|ExchangeTiles:
        if len(plays) == 0:
            return ExchangeTiles([True] * 7)
        scores = [w for _,w in plays]
        max_score = max(scores)
        weights = [(w/max_score)**40 for _,w in plays]
        return PlayWord(*random.choices(plays, weights=weights)[0][0])

    def selection(self) -> MonteCarloNode:
        if self._root is None:
            raise ValueError("Root uninitialized")
        node = self._root
        while not node.is_leaf():
            node = max(node.children.values(), key=lambda child: child.UCB())
        return node

    def expand(self, node: MonteCarloNode) -> MonteCarloNode:
        plays = node.get_plays()
        play = self.choose_play_randomly(node, plays)
        new_node = node.get_copy_with_play(play)
        new_node.set_parent(node, play)
        return new_node

    def simulate(self, baseNode: MonteCarloNode) -> float:

        # copy node to get a fresh one for playouts
        play = self.choose_play_randomly(baseNode, baseNode.get_plays())
        node = baseNode.get_copy_with_play(play)

        # playouts
        board = node.state
        converter = node.converter
        while not board.game_is_over():
            plays = node.get_fresh_plays()
            play = self.choose_play_randomly(node, plays)
            play.play(board, node.player)
            converter.update_board()
            node.switch_player()
        scores = board.get_scores()
        # print("finished simulation. Scores are", scores)
        if scores[baseNode.player] > scores[1 - baseNode.player]:
            return 0 # win
        elif scores[baseNode.player] < scores[1 - baseNode.player]:
            return 1 # loss
        return 0.5 # draw


    def search(self) -> MonteCarloNode|None:


        for _ in range(self._search_count):
            node = self.selection()
            new_node = self.expand(node)
            win = self.simulate(new_node)
            new_node.update(win)
            self._states.append(new_node)

            # # graph
            # graph = Graph()
            # for state in self._states:
            #     graph.add_node(state)
            #     if state._parent is not None:
            #         graph.add_edge(state, state._parent)
            # labels = {n: f'{n.wins}/{n.sims}\n{n.play}' for n in self._states}
            # draw(graph, labels=labels, pos=bfs_layout(graph, self._states[0]))
            # plt.show()

        if self._root is None:
            return None

        best_node = max(self._root.children.values(), key=lambda node: node.sims)
        return best_node


    def init_root(self):
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")
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




    def choose_move(self) -> PlayWord|ExchangeTiles:
        self.init_root()
        best_node = self.search()
        if best_node is not None and best_node.play is not None:
            return best_node.play
        return ExchangeTiles([True] * 7)


class HeuristicMonteCarlo(MonteCarlo):
    def simulate(self, baseNode: MonteCarloNode) -> float:
        scores = baseNode.state.get_scores()
        p = baseNode.player
        o = 1 - baseNode.player
        win_estimate = 1/(np.exp(-(scores[p]-scores[o])/50))
        return 1-win_estimate

class HeuristicMonteCarloExit(HeuristicMonteCarlo):
    def __str__(self):
        return "Heuristic MCTS (With early exit)"
    def choose_move(self) -> PlayWord|ExchangeTiles:
        if self._gatekeeper is None:
            raise ValueError("uninitialized gatekeeper")
        if type(self._gatekeeper.get_last_move()) == ExchangeTiles:
            print("opponent passed")
            hand = self._gatekeeper.get_hand()
            tile_values = sum(TILE_VALUES[c] for c in hand)
            if self._gatekeeper.get_my_score() > self._gatekeeper.get_opponent_score() + tile_values*2:
                print("winning, so quit whilst ahead")
                high_value_tiles = [(TILE_VALUES[c] >= 5) for c in hand]
                return ExchangeTiles(high_value_tiles)
        return super().choose_move()

class ReverseMonteCarlo(MonteCarlo):
    def simulate(self, baseNode: MonteCarloNode) -> float:
        return 1 - super().simulate(baseNode)
