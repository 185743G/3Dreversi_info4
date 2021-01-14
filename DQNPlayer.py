import random
import copy

import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np

from Constants import EMPTY, DRAW
from MLP import MLP


class DQNPlayer:
    def __init__(self, turn, name="DQN", e=1, dispPred=False):
        self.name = name
        self.myturn = turn
        self.enemyturn = 3-turn
        self.model = MLP(216, 256, 216) # 216(=6*6*6)じゃないとエラーが起きる
        self.optimizer = optimizers.SGD()
        self.optimizer.setup(self.model)
        self.e = e
        self.gamma = 0.95
        self.dispPred = dispPred
        self.last_move = None
        self.last_board = None
        self.last_pred = None
        self.totalgamecount = 0
        self.rwin, self.rlose, self.rdraw, self.rmiss = 1, -1, 0, -1.5

    def act(self, board):

        self.last_board = copy.copy(board)
        x = np.array([board.get_flattend_board()], dtype=np.float32).astype(np.float32)  #

        pred = self.model(x)
        if self.dispPred:
            print(pred.data)
        self.last_pred = pred.data[0, :]
        act = np.argmax(pred.data, axis=1)
        if self.e > 0.2:  # decrement epsilon over time
            self.e -= 1 / (20000)
        if random.random() < self.e:
            acts = [board.get_flatten_point(p) for p in board.can_put_stone_all()]
            if len(acts) == 0:
                return [-2, -2, -2]  # passを返す
            i = random.randrange(len(acts))
            act = acts[i]
        i = 0
        if type(act) is not int:
            act = act[0]


        while board.get_flattend_board()[act] != EMPTY:
            # print("Wrong Act "+str(board.board)+" with "+str(act))
            self.learn(self.last_board, act, -1, self.last_board)
            x = np.array([board.get_flattend_board()], dtype=np.float32).astype(np.float32)
            pred = self.model(x)  # modelに対してデータのみを渡すと予測を行う。ここだと、盤面データから次の手の予測を行う。
            # print(pred.data)
            act = np.argmax(pred.data, axis=1)
            if type(act) is not int:
                act = act[0]
            i += 1
            if i > 10:
                #                print("Exceed Pos Find"+str(board.board)+" with "+str(act))
                acts = [board.get_flatten_point(p) for p in self.last_board.can_put_stone_all()]
                if len(acts) == 0:
                    continue  # passを返す
                act = acts[random.randrange(len(acts))]
                if type(act) is not int:
                    act = act[0]

        self.last_move = act
        # self.last_pred=pred.data[0,:]
        return board.get_unflatten_point(act)

    def getGameResult(self, board):
        r = 0
        if self.last_move is not None:
            if board.winner is None:
                self.learn(self.last_board, self.last_move, 0, board)
                pass
            else:
                if board.get_flattend_board() == self.last_board.get_flattend_board():
                    self.learn(self.last_board, self.last_move, self.rmiss, board)
                elif board.winner == self.myturn:
                    self.learn(self.last_board, self.last_move, self.rwin, board)
                elif board.winner != DRAW:
                    self.learn(self.last_board, self.last_move, self.rlose, board)
                else:  # DRAW
                    self.learn(self.last_board, self.last_move, self.rdraw, board)
                self.totalgamecount += 1
                self.last_move = None
                self.last_board = None
                self.last_pred = None

    def learn(self, s, a, r, fs):
        if fs.winner is not None:
            maxQnew = 0
        else:
            x = np.array([fs.board], dtype=np.float32).astype(np.float32)
            maxQnew = np.max(self.model(x).data[0])
        update = r + self.gamma * maxQnew
        # print(('Prev Board:{} ,ACT:{}, Next Board:{}, Get Reward {}, Update {}').format(s.board,a,fs.board,r,update))
        # print(('PREV:{}').format(self.last_pred))
        self.last_pred[a] = update

        x = np.array([s.board], dtype=np.float32).astype(np.float32)  # データ
        t = np.array([self.last_pred], dtype=np.float32).astype(np.float32)  # 教師
        self.model.zerograds()
        loss = self.model(x, t, train=True)
        loss.backward()
        self.optimizer.update()
