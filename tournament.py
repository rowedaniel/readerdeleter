import time

from scrabble.incrementalist import Incrementalist
from scrabble.daniel_bot import Greedy, MonteCarlo, ReverseMonteCarlo
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
        scores = [0.0] * len(self._players)
        for i in range(len(self._players)):
            for j in range(len(self._players)):
                if i != j:
                    i_won, j_won = self.play_game(self._players[i], self._players[j])
                    scores[i] += i_won
                    scores[j] += j_won
                    yield self._time, self._moves
        for i, player in enumerate(self._players):
            print(f'{str(player)}: {scores[i]}')

    def run_n_games(self, n: int):
        """
        play n games between each pair
        """
        scores = [0.0] * len(self._players)
        for _ in range(n):
            for i in range(len(self._players)):
                for j in range(len(self._players)):
                    if i != j:
                        i_won, j_won = self.play_game(self._players[i], self._players[j])
                        scores[i] += i_won
                        scores[j] += j_won
                        print("finished game,", scores)
        for i, player in enumerate(self._players):
            print(f'{str(player)}: {scores[i]}')
        return scores

    def play_game(self, a, b):
        """
        Plays a game between AIs a (going first) and b. Returns their tournament scores: (1, 0) if a wins, (0, 1) if
        b wins, or (0.5, 0.5) in case of a tie.
        """
        self._time = 0
        self._moves = 0
        # print(f'{a} vs {b}:')
        board = Board()
        a.set_gatekeeper(GateKeeper(board, 0))
        b.set_gatekeeper(GateKeeper(board, 1))
        while not board.game_is_over():
            self.play_move(board, a, 0)
            if not board.game_is_over():
                self.play_move(board, b, 1)
        scores = board.get_scores()
        print(f'Final score: {a} {scores[0]}, {b} {scores[1]}. Avg {self._time/self._moves} s/move ({self._time} over {self._moves})\n')
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
    from scrabble.board_converter import BoardConverter
    from scrabble.board import DICTIONARY
    from readerdeleter.gaddag import generate_GADDAG
    import threading
    total_games = 8
    threads = 4
    game_threads = []
    scores = [[] for _ in range(threads)]

    gaddag = generate_GADDAG(list(DICTIONARY))
    print("generating players")
    players = [
            [
                # ReverseMonteCarlo(20, BoardConverter(gaddag=gaddag)),
                Greedy(),
                MonteCarlo(20, BoardConverter(gaddag=gaddag)),
           ] for _ in range(threads)]
    print("generated players")


    def run_game(i: int):
        print("running game", i)
        scores[i] = ScrabbleTournament(players[i]).run_n_games(total_games // threads)

    total_time = time.time()
    for i in range(threads):
        x = threading.Thread(target=run_game, args=[i])
        game_threads.append(x)
        x.start()

    for thread in game_threads:
        thread.join()
    total_time = time.time() - total_time
    total_scores = [sum(score[i] for score in scores) for i in range(2)]
    print(f"took {total_time}s for {total_games} games on {threads} threads. Final score was {total_scores}")
