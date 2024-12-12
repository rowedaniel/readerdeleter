from tournament import ScrabbleTournament
from scrabble.mctsnn_bot import MonteCarloNN, Policy, Value
from scrabble.board import DICTIONARY
from scrabble.board_converter import BoardConverter
from readerdeleter.gaddag import generate_GADDAG
from scrabble.daniel_bot import Greedy

import torch
import torch.nn as nn
import torch.optim as optim
import threading


class TrainingTournament(ScrabbleTournament):
    def __init__(self):
        self.policy = Policy()
        self.value = Value()

        self.n_threads = 1


        self.policy_X = [[] for _ in range(2*self.n_threads)]
        self.policy_y = [[] for _ in range(2*self.n_threads)]
        self.value_X = [[] for _ in range(2*self.n_threads)]
        self.value_y = [[] for _ in range(2*self.n_threads)]

        self.gaddag = generate_GADDAG(list(DICTIONARY))
        super().__init__([
            MonteCarloNN(self.policy,
                         self.value,
                         20,
                         BoardConverter(gaddag=self.gaddag),
                         self.value_X[i],
                         self.policy_X[i],
                         self.policy_y[i],
                         )
                         for i in range(2*self.n_threads)
            ])

    def run_and_train(self,
                      games_per_batch: int,
                      n_epochs: int,
                      batch_size: int,
                      save_file_prefix: str
                      ):
        loss_fn = nn.BCELoss()  # binary cross entropy
        policy_optimizer = optim.Adam(self.policy.parameters(), lr=0.001)
        value_optimizer = optim.Adam(self.value.parameters(), lr=0.001)

        def play_thread(i: int):
            for _ in range(batch_size):
                p_num = i*2
                print("playing game")
                wins = self.play_game(self._players[p_num], self._players[p_num+1])
                for y,X,win in zip(self.value_y[p_num:p_num+2], self.value_X[p_num:p_num+2], wins):
                    y.extend([win] * (len(X)-len(y)))


        for epoch in range(n_epochs):
            print("epoch", epoch)
            for _ in range(0, games_per_batch, batch_size*self.n_threads*2):
                for i in range(2*self.n_threads):
                    self.policy_X[i].clear()
                    self.policy_y[i].clear()
                    self.value_X[i].clear()
                    self.value_y[i].clear()

                print("playing", batch_size, "games")
                threads = []
                for t in range(self.n_threads):
                    x = threading.Thread(target=play_thread, args=[t])
                    play_thread(0)
                    threads.append(x)
                    x.start()
                for thread in threads:
                    thread.join()
                print("done. Now training")
                policy_X = torch.cat([torch.cat(xs) for xs in self.policy_X])
                policy_y = torch.cat([torch.tensor(ys, dtype=torch.float32) for ys in self.policy_y]).reshape(-1, 1)
                loss = loss_fn(self.policy(policy_X), policy_y)
                policy_optimizer.zero_grad()
                loss.backward()
                policy_optimizer.step()

                value_X = torch.cat([torch.cat(xs) for xs in self.value_X])
                value_y = torch.cat([torch.tensor(ys, dtype=torch.float32) for ys in self.value_y]).reshape(-1, 1)
                loss = loss_fn(self.value(value_X), value_y)
                value_optimizer.zero_grad()
                loss.backward()
                value_optimizer.step()


            torch.save(self.policy.state_dict(), f'{save_file_prefix}_policy_{epoch}')
            torch.save(self.value.state_dict(), f'{save_file_prefix}_value_{epoch}')

            # test performance
            print('testing performance')
            test_tournament = ScrabbleTournament([
                Greedy(BoardConverter(gaddag=self.gaddag)),
                MonteCarloNN(self.policy, self.value, 20, BoardConverter(gaddag=self.gaddag))
            ])
            print(len(test_tournament._players))
            for _ in test_tournament.run():
                pass
            print("done testing")




if __name__ == "__main__":
    tt = TrainingTournament()
    tt.run_and_train(100, 100, 10, "basic_nn")
