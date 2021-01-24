import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np
import random


class MLP(chainer.Chain):
    # L.linear(input_dim_num, out_dim_num) 全結合層
    def __init__(self, n_in, n_units, n_out):
        super(MLP, self).__init__(
            l1=L.Linear(n_in, n_units),  # first layer
            l2=L.Linear(n_units, n_units),  # second layer
            l3=L.Linear(n_units, n_units),  # Third layer
            l4=L.Linear(n_units, n_out),  # output layer
        )

    """
    mean squad error = 二乗誤差
    leaky relu : reluの一つ
    L -> F -> L
    """

    def __call__(self, x, t=None, train=False):
        h = F.leaky_relu(self.l1(x))
        h = F.leaky_relu(self.l2(h))
        h = F.leaky_relu(self.l3(h))
        h = self.l4(h)

        if train:
            return F.mean_squared_error(h, t)
        else:
            return h

    def get(self, x):
        # input x as float, output float
        return self.predict(Variable(np.array([x]).astype(np.float32).reshape(1, 1))).data[0][0]



# model = MLP(12, 20, 12)

# optimizer = optimizers.SGD()
# optimizer.setup(model)

# for _ in range(100):
#     for j in range(100):
#         x = np.array([[random.random() for i in range(12)]], dtype=np.float32)
#         t = x+1.0
#         loss = model(x, t, train=True)
#         model.cleargrads()
#         loss.backward()
#         optimizer.update()
#         pred = model(x)
#         print(loss)


import pickle
import copy
import random
import sqlite3


from Board import Board
from Constants import WHITE, BLACK, EMPTY
from RandomPlayer import RandomPlayer
from Util import get_opponent
import pickle

class History(object):
    def __init__(self):
        self.gameResults = []

    def addGameResults(self, gameResult):
        self.gameResults.append(gameResult)

    def setGameResults(self, gameResults):
        self.gameResults = gameResults


class GameResult(object):
    def __init__(self, s, a, r, s2, t):
        self.s = s
        self.a = a
        self.r = r
        self.s2 = s2
        self.t = t

with open('history.pickle', 'rb') as f:
    history_p = pickle.load(f)

print(history_p)

model = MLP(216, 260, 216)
optimizer = optimizers.SGD()
optimizer.setup(model)

gameResults = copy.deepcopy(history_p.gameResults)
# random.shuffle(gameResults)

GAMMA = 0.95

for gameResult in gameResults:
    s = gameResult.s
    a = gameResult.a
    r = gameResult.r
    s2 = gameResult.s2
    t = gameResult.t
    s = np.array([s], dtype=np.float32).astype(np.float32)  # データ
    s2 = np.array([s2], dtype=np.float32).astype(np.float32)  # データ
    if s2.shape == (1, 216) and s.shape == (1, 216) and a != None:
        s_Qs = model(s)
        s2_Qs = model(s2)
        dat = s_Qs.data[0]
        maxQnew = max(s2_Qs.data[0])
        tmp = r + (1-t)*GAMMA*maxQnew
        dat[a] = tmp
        target = np.array([dat], dtype=np.float32).astype(np.float32)  # データ
        loss = model(s, target, train=True)
        print(loss.data)
        model.cleargrads()
        loss.backward()
        optimizer.update()
        #         pred = model(x)
        print(loss)
