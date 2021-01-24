import chainer
from chainer import serializers

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np
import random




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
from MLP import MLP
from RandomPlayer import RandomPlayer
from Util import get_opponent
import pickle
from History import History
from GameResult import GameResult

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

serializers.save_npz("mymodel.npz", model) # npz形式で書き出し


