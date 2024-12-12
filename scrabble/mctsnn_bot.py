from .board_converter import BoardConverter, ALPHABET_BLANK
from .daniel_bot import MonteCarlo, MonteCarloNode
from .location import Location
from .move import PlayWord, ExchangeTiles

from typing import Any

import torch
import torch.nn as nn
import numpy as np
import random

class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(15**2 + 15**2 + 1, 400)
        self.res1 = nn.ReLU()
        self.layer2 = nn.Linear(400, 400)
        self.res2 = nn.ReLU()
        self.layer3 = nn.Linear(400, 40)
        self.res3 = nn.ReLU()
        self.layer4 = nn.Linear(40, 4)
        self.res4 = nn.ReLU()
        self.layer5 = nn.Linear(4, 1)
        self.res_final = nn.Sigmoid()
 
    def forward(self, x):
        x = self.res1(self.layer1(x))
        x = self.res2(self.layer2(x))
        x = self.res3(self.layer3(x))
        x = self.res4(self.layer4(x))
        x = self.res_final(self.layer5(x))
        return x

class Value(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(15**2 + 7*len(ALPHABET_BLANK) + 2, 400)
        self.res1 = nn.ReLU()
        self.layer2 = nn.Linear(400, 40)
        self.res2 = nn.ReLU()
        self.layer3 = nn.Linear(40, 8)
        self.res3 = nn.ReLU()
        self.layer4 = nn.Linear(8, 1)
        self.res_final = nn.Sigmoid()
 
    def forward(self, x):
        x = self.res1(self.layer1(x))
        x = self.res2(self.layer2(x))
        x = self.res3(self.layer3(x))
        x = self.res_final(self.layer4(x))
        return x


class MonteCarloNN(MonteCarlo):
    def __init__(self,
                 policy: Policy,
                 value: Value,
                 search_count: int = 25,
                 board: BoardConverter|None = None,
                 train_value_data: list[Any]|None = None,
                 train_policy_data: list[Any]|None = None,
                 train_policy_labels: list[Any]|None = None,
                 ):
        super().__init__(search_count, board)
        self.value = value
        self.policy = policy
        self.train_value_data = train_value_data
        self.train_policy_data = train_policy_data
        self.train_policy_labels = train_policy_labels

    def __str__(self):
        return f'Monte Carlo with NN (n={self._search_count})'

    def build_simplified_board(self, node: MonteCarloNode):
        return np.array(
                [
                    [
                        (1 if node.state.is_occupied(Location(r,c)) else 0)
                        for c in range(15)
                    ] for r in range(15)
                ]

            )

    def build_play_board(self, node: MonteCarloNode, play: tuple[tuple[str, Location, Location], int]):
        board = self.build_simplified_board(node)
        loc = play[0][1]
        for _ in range(len(play[0][0])):
            board[loc.r, loc.c] = 1
            loc += play[0][2]
        return board

    def create_policy_features(self,
                               node: MonteCarloNode,
                               plays: list[tuple[tuple[str, Location, Location], int]]
                               ):
        board_data = np.vstack([
            np.hstack([self.build_simplified_board(node), self.build_play_board(node, play)]).reshape(1,-1) for play in plays
            ])
        scores = np.array([[w * 1.0] for _,w in plays])
        scores /= np.max(scores)
        features = np.hstack([scores, board_data])
        return torch.tensor(features, dtype=torch.float32)

    def build_hand_vector(self, node: MonteCarloNode):
        hand = node.state.get_hand(0)
        hand_len_7 = sorted((hand + [" "]*7)[:7])
        hand_vector = np.array([[(0 if c == h else 1)for c in ALPHABET_BLANK] for h in hand_len_7])
        return hand_vector.reshape(1, -1)

    def create_value_features(self, node: MonteCarloNode):
        board_simplified = self.build_simplified_board(node).reshape(1, -1)
        scores = np.array([node.state.get_scores()]).reshape(1, -1)
        hand = self.build_hand_vector(node).reshape(1, -1)
        features = np.hstack([board_simplified, hand, scores])
        return torch.tensor(features, dtype=torch.float32).reshape(1, -1)

    def choose_play_randomly(self,
                             node: MonteCarloNode,
                             plays: list[tuple[tuple[str, Location, Location], int]]
                             ) -> PlayWord|ExchangeTiles:
        """
        Choose the most commonly chosen move according to policy heuristic
        """
        if len(plays) == 0:
            return ExchangeTiles([True] * 7)
        features = self.create_policy_features(node, plays)
        weights = self.policy(features)
        # print('weights shape:', weights.shape)
        return PlayWord(*random.choices(plays, weights=weights)[0][0])

    def simulate(self, baseNode: MonteCarloNode) -> float:
        return self.value(self.create_value_features(baseNode))

    def choose_move(self) -> PlayWord|ExchangeTiles:
        self.init_root()
        if self._root is None or len(self._root.get_plays()) == 0:
            return ExchangeTiles([True] * 7)


        # populate training data
        if self.train_value_data is not None:
            self.train_value_data.append(self.create_value_features(self._root))

        best_node = self.search()
        if best_node is None or best_node.play is None:
            return ExchangeTiles([True] * 7)

        # populate policy data
        if self.train_policy_data is not None and \
           self.train_policy_labels is not None:
            self.train_policy_data.extend([
                self.create_policy_features(self._root, self._root.get_plays())
            ])
            self.train_policy_labels.extend([
                0 if play != best_node.play else 1
                for play in self._root.get_plays()
            ])

        return best_node.play

