import time

from scrabble.incrementalist import Incrementalist
from scrabble.daniel_bot import Greedy, MonteCarlo
from scrabble.board import Board
from scrabble.gatekeeper import GateKeeper

class ScrabbleTournament:
    """A tournament between AIs."""
    def __init__(self, players):
        self._players = players
        self._time = 0
        self._moves = 0

    def run(self):
        """
        Plays two games between each pair of contestants, one with each going first. Prints the number of wins for each
        contestant (including 0.5 wins for each tie).
        """
        scores = [0.0] * len(players)
        for i in range(len(players)):
            for j in range(len(players)):
                if i != j:
                    i_won, j_won = self.play_game(players[i], players[j])
                    scores[i] += i_won
                    scores[j] += j_won
                    yield self._time, self._moves
        for i, player in enumerate(players):
            print(f'{str(player)}: {scores[i]}')

    def play_game(self, a, b):
        """
        Plays a game between AIs a (going first) and b. Returns their tournament scores: (1, 0) if a wins, (0, 1) if
        b wins, or (0.5, 0.5) in case of a tie.
        """
        self._time = 0
        self._moves = 0
        print(f'{a} vs {b}:')
        board = Board()
        a.set_gatekeeper(GateKeeper(board, 0))
        b.set_gatekeeper(GateKeeper(board, 1))
        while not board.game_is_over():
            self.play_move(board, a, 0)
            if not board.game_is_over():
                self.play_move(board, b, 1)
        scores = board.get_scores()
        print(f'Final score: {a} {scores[0]}, {b} {scores[1]}. Avg {self._time/self._moves} s/move ({self._time} over {self._moves}\n')
        if scores[0] > scores[1]:
            return 1, 0
        elif scores[0] < scores[1]:
            return 0, 1
        return 0.5, 0.5

    def play_move(self, board, player, player_number):
        t = time.time()
        """
        Asks player for a move and plays it on board.
        """
        move = player.choose_move()
        move.play(board, player_number)
        self._time += time.time() - t
        self._moves += 1


if __name__ == '__main__':
    players = [
            Greedy(),
            MonteCarlo(),
               ]
    total_time = 0
    total_turns = 0
    total_games = 0
    for i in range(10):
        for game_t, game_m in ScrabbleTournament(players).run():
            total_time += game_t
            total_turns += game_m
            total_games += 1

    print(f"average game took {total_time/total_games} s, with each game having an average of {total_turns/total_games} turns per game")
