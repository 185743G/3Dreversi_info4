import random
import copy

import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils, Chain, cuda
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np
# import cupy as cp


from Constants import EMPTY, DRAW, use_gpu
from MLP import MLP
from Util import get_opponent


class DQNPlayer:
    def __init__(self, turn, name="DQN", e=1.0, dispPred=False):
        self.name = name
        self.myturn = turn
        self.enemyturn = 3 - turn
        self.model = MLP(128, 256, 64)

        self.optimizer = optimizers.SGD()
        self.optimizer.setup(self.model)
        self.e = e
        self.bottom_e = 0.05
        self.gamma = 0.95
        self.step_num = 0
        self.start_learn = 5 * 10 ** 3
        self.batch_size = 128
        self.experience = []   # 直近の1万回分の盤面状態s, 置き場所a, 報酬r, 置いた後の盤面状態s2, 終了フラグtを保存するためのリスト
        self.experience_limit = 10000
        self.totalgamecount = 0
        self.WIN = 1
        self.LOSE = -1
        self.DRAW = -0.5

    def act(self, board):     # 配置処理
        can_put = board.can_put_stone_all()
        if len(can_put) == 0:
            return [-2, -2, -2]

        s = np.array(board.get_flattend_board(), dtype=np.float32).astype(np.float32)  #
        s_Qs = self.model(np.array([s]))
        dat = s_Qs.data[0]
        act = np.argmax(s_Qs.data[0])
        if self.e > self.bottom_e:  # decrement epsilon over time
            self.e -= 1 / (200)
        if random.random() < self.e:
            act = board.get_act_point(random.choice(can_put))

        a = act
        if board.get_board_point(act) not in can_put:
            r = self.LOSE
            s2 = copy.deepcopy(s)
            t = 1
            act = board.get_act_point(random.choice(can_put))
        else:
            r, s2, t = self.step(board, act)
            s2 = np.array(s2, dtype=np.float32).astype(np.float32)  #

        self.experience.append([s, a, r, s2, t])
        if len(self.experience) >= 10000:
            self.experience.pop(0)
        self.step_num += 1
        if self.step_num > self.start_learn:
            self.replay_experience()


        return board.get_board_point(act)

    def replay_experience(self):    # experienceからランダムにbatch_size分データをとって学習する
        samples = random.sample(self.experience, self.batch_size)
        s=[]
        a=[]
        r=[]
        s2=[]
        t=[]
        for sample in samples:
            s.append(sample[0])
            a.append(sample[1])
            r.append(sample[2])
            s2.append(sample[3])
            t.append(sample[4])

        s = np.array(s)
        a = np.array(a)
        r = np.array(r)
        s2 = np.array(s2)
        t = np.array(t)

        s_Qs = self.model(s)
        s_Q_data = copy.deepcopy(s_Qs.data)
        s2_Qs = self.model(s2)
        maxQnew = np.max(s2_Qs.data, axis=1)
        tmp = r + (1 - t) * self.gamma * maxQnew
        for i in range(len(maxQnew)):
            s_Q_data[i, a[i]] = tmp[i]

        target = np.array(s_Q_data, dtype=np.float32).astype(np.float32)  # データ
        loss = self.model(s, target, train=True)
        self.model.cleargrads()
        loss.backward()
        self.optimizer.update()

    def getGameResult(self, board):
        pass


    def get_reward(self, board):    # 報酬を返す
        failed_put_stone = 0
        board_c = copy.deepcopy(board)
        turns = [self.myturn, get_opponent(self.myturn)]
        for turn in turns:
            board_c.turn = turn
            if len(board_c.can_put_stone_all()) == 0:
                failed_put_stone += 1
        if failed_put_stone == 2:  #
            winner = board_c.get_winner()
            if winner == self.myturn:
                return self.WIN
            elif winner == get_opponent(self.myturn):
                return self.LOSE
            else:
                return self.DRAW
        else:
            return 0


    def step(self, board, act):  # 盤面boardにactを配置した時の報酬r, 次の盤面状態s2, 終了フラグtを返す
        # s, a, r, s2, t
        s = None
        a = None
        r = 0
        s2 = None
        t = 0

        board_c = copy.deepcopy(board)
        s = board.get_flattend_board()
        a = act
        board_c.flip(board_c.get_board_point(act))
        board_c.change_turn()
        s2 = board_c.get_flattend_board()
        r = self.get_reward(board_c)
        if r in [self.WIN, self.LOSE, self.DRAW]:
            t = 1
        return r, s2, t

