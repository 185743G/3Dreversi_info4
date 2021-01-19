import random
import copy

from Constants import EMPTY
from RandomPlayer import RandomPlayer
from Util import get_opponent

import numpy as np

# 単純なモンテカルロ
# 非常に低速
class PureMonteCarloPlayer:
    def __init__(self, turn):
        self.name = "Random"
        self.myturn = turn
        self.playout_num = 20
        self.PASS = -2

    def act(self, board):
        # 自分が打てる最大の状態の盤面が与えられる

        acts = board.can_put_stone_all()
        if len(acts) == 0:
            return [self.PASS] * 3
        act = self.monte_carlo(board, acts)
        return act

    def monte_carlo(self, board, acts):
        results = [0] * len(acts)
        for i in range(len(acts)):
            for _ in range(self.playout_num):
                board_c = copy.copy(board)# playout_num回文だけplayout
                if self.playout(board_c, acts[i], RandomPlayer(get_opponent(self.myturn))) == self.myturn:
                    results[i] += 1
        j = np.argmax(results)
        return acts[j]


    def playout(self, board, act, opponent):
        board_c = copy.deepcopy(board)
        board_c.flip(act)
        board_c.change_turn()
        while board_c.winner == EMPTY:
            if board_c.turn == self.myturn:
                input_pos = self.random_choice(board_c)
            elif board_c.turn == get_opponent(self.myturn):
                input_pos = opponent.act(board_c)

            if input_pos == [self.PASS]*3:
                board_c.change_turn()
                if len(board_c.can_put_stone_all()) == 0:
                    winner = board_c.get_winner()
                    return winner
            else:
                if board_c.can_put_stone(input_pos):
                    board_c.flip(input_pos)
                    board_c.change_turn()
                else:
                    print("指定した座標には置けません")



    def random_choice(self, board):  # モンテカルロのプレイアウト用のrandom_choice。randomplayerのactとほとんど同じ
        acts = board.can_put_stone_all()
        if len(acts) == 0:
            acts.append([self.PASS, self.PASS, self.PASS])
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self, board):
        pass