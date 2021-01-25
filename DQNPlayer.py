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
        self.enemyturn = 3-turn
        self.model = MLP(216, 864, 216) # 216(=6*6*6)じゃないとエラーが起きる
        # serializers.load_npz("mymodel.npz", self.model)

        self.optimizer = optimizers.SGD()
        self.optimizer.setup(self.model)
        self.e = e
        self.gamma = 0.95
        # self.dispPred = dispPred
        # self.last_move = None
        # self.last_board = None
        # self.last_pred = None
        # self.xp = cuda.cupy
        self.step_num = 0
        self.start_learn = 5 * 10**3
        self.batch_size = 128
        self.experience = []
        self.experience_limit = 10000
        self.totalgamecount = 0
        # self.rwin, self.rlose, self.rdraw, self.rmiss = 1, -1, 0, -1.5
        self.WIN = 10
        self.LOSE = -10
        self.DRAW = -5

    def act(self, board):
        can_put = board.can_put_stone_all()
        if len(can_put) == 0:
            return [-2, -2, -2]

        s = np.array(board.get_flattend_board(), dtype=np.float32).astype(np.float32)  #
        s_Qs = self.model(np.array([s]))
        dat = s_Qs.data[0]
        # if use_gpu:
        act = np.argmax(s_Qs.data[0])
        # else:
        #     act = np.argmax(s_Qs.data[0])
        if self.e > 0.2:  # decrement epsilon over time
            self.e -= 1 / (20000)
        if random.random() < self.e or board.get_unflatten_point(act) not in can_put:   # TODO: 違反な配置をされたら、-1の報酬を渡すようにする。ひとまずは、違反な配置があったらrandomにおける場所から選ぶ
            act = board.get_flatten_point(random.choice(can_put))

        a = act
        r, s2, t = self.step(board, act)
        s2 = np.array(s2, dtype=np.float32).astype(np.float32)  #

        self.experience.append([s, a, r, s2, t])
        if len(self.experience) >= 10000:
            self.experience.pop(0)
        self.step_num += 1
        if self.step_num > self.start_learn:
            self.replay_experience()


        # s2_Qs = self.model(s2)
        # maxQnew = np.max(s2_Qs.data[0])
        # # TODO: actを選んだときのs2の様子と報酬とそのときのQの値を得る
        # dat[act] = r + (1-t)*self.gamma*maxQnew
        # target = np.array([dat], dtype=np.float32).astype(np.float32)  # データ
        # loss = self.model(s, target, train=True)
        # # print(loss.data)
        # self.model.cleargrads()
        # loss.backward()
        # self.optimizer.update()
        # print(loss)



        return board.get_unflatten_point(act)
        # self.last_board = copy.copy(board)
        # x = np.array([board.get_flattend_board()], dtype=np.float32).astype(np.float32)  #
        #
        # pred = self.model(x)
        # if self.dispPred:
        #     print(pred.data)
        # self.last_pred = pred.data[0, :]
        # act = np.argmax(pred.data, axis=1)
        # if self.e > 0.2:  # decrement epsilon over time
        #     self.e -= 1 / (20000)
        # if random.random() < self.e:
        #     acts = [board.get_flatten_point(p) for p in board.can_put_stone_all()]
        #     if len(acts) == 0:
        #         return [-2, -2, -2]  # passを返す
        #     i = random.randrange(len(acts))
        #     act = acts[i]
        # i = 0
        # if type(act) is not int:
        #     act = act[0]
        #
        #
        # while board.get_flattend_board()[act] != EMPTY:
        #     # print("Wrong Act "+str(board.board)+" with "+str(act))
        #     self.learn(self.last_board, act, -1, self.last_board)
        #     x = np.array([board.get_flattend_board()], dtype=np.float32).astype(np.float32)
        #     pred = self.model(x)  # modelに対してデータのみを渡すと予測を行う。ここだと、盤面データから次の手の予測を行う。
        #     # print(pred.data)
        #     act = np.argmax(pred.data, axis=1)
        #     if type(act) is not int:
        #         act = act[0]
        #     i += 1
        #     if i > 10:
        #         #                print("Exceed Pos Find"+str(board.board)+" with "+str(act))
        #         acts = [board.get_flatten_point(p) for p in self.last_board.can_put_stone_all()]
        #         if len(acts) == 0:
        #             continue  # passを返す
        #         act = acts[random.randrange(len(acts))]
        #         if type(act) is not int:
        #             act = act[0]
        #
        # self.last_move = act
        # # self.last_pred=pred.data[0,:]
        # return board.get_unflatten_point(act)

    def replay_experience(self):
        # for sample in samples

        samples = random.sample(self.experience, self.batch_size)
        s=np.array([sample[0] for sample in samples])
        a=np.array([sample[1] for sample in samples])
        r=np.array([sample[2] for sample in samples])
        s2=np.array([sample[3] for sample in samples])
        t=np.array([sample[4] for sample in samples])

        s_Qs = self.model(s)
        s_Q_data = copy.deepcopy(s_Qs.data)
        s2_Qs = self.model(s2)
        maxQnew = np.max(s2_Qs.data, axis=1)
        tmp = r + (1 - t)*self.gamma*maxQnew
        for i in range(len(maxQnew)):
            s_Q_data[i, a[i]] = tmp[i]


        target = np.array(s_Q_data, dtype=np.float32).astype(np.float32)  # データ
        loss = self.model(s, target, train=True)
        self.model.cleargrads()
        loss.backward()
        self.optimizer.update()


        # if random.random() < self.e:


        # # TODO: actを選んだときのs2の様子と報酬とそのときのQの値を得る
        # dat[act] = r + (1-t)*self.gamma*maxQnew
        # target = np.array([dat], dtype=np.float32).astype(np.float32)  # データ
        # loss = self.model(s, target, train=True)
        # # print(loss.data)
        # self.model.cleargrads()
        # loss.backward()
        # self.optimizer.update()
        # print(loss)

        # pass

    def getGameResult(self, board):
        pass
        # r = 0
        # if self.last_move is not None:
        #     if board.winner is None:
        #         self.learn(self.last_board, self.last_move, 0, board)
        #         pass
        #     else:
        #         if board.get_flattend_board() == self.last_board.get_flattend_board():
        #             self.learn(self.last_board, self.last_move, self.rmiss, board)
        #         elif board.winner == self.myturn:
        #             self.learn(self.last_board, self.last_move, self.rwin, board)
        #         elif board.winner != DRAW:
        #             self.learn(self.last_board, self.last_move, self.rlose, board)
        #         else:  # DRAW
        #             self.learn(self.last_board, self.last_move, self.rdraw, board)
        #         self.totalgamecount += 1
        #         self.last_move = None
        #         self.last_board = None
        #         self.last_pred = None
    def get_next_board(self, b, act):
        pass

    def get_reward(self, board): # TODO: s2が存在するか確かめたあとが前提
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


    # def get_reward(board):
    #     failed_put_stone = 0
    #     board_c = copy.deepcopy(board)
    #     for player in players:
    #         board_c.turn = player.myturn
    #         if len(board_c.can_put_stone_all()) == 0:
    #             failed_put_stone += 1
    #
    #     if failed_put_stone == 2:  #
    #         winner = board_c.get_winner()
    #         if winner == AI_TURN:
    #             return WIN
    #         elif winner == get_opponent(AI_TURN):
    #             return LOSE
    #         else:
    #             return DRAW
    #     else:
    #         return 0

    def step(self, board, act):  # TODO: boardに対してactが有効か確かめるのが前提
        # s, a, r, s2, t
        s = None
        a = None
        r = 0
        s2 = None
        t = 0

        board_c = copy.deepcopy(board)
        s=board.board
        a=act
        board_c.flip(board_c.get_unflatten_point(act))
        board_c.change_turn()
        s2 = board_c.board
        r = self.get_reward(board_c)
        if r in [self.WIN, self.LOSE, self.DRAW]:
            t = 1
        return r, s2, t


    def learn(self, s, a, r, fs):
        pass
        # if fs.winner is not None:
        #     maxQnew = 0
        # else:
        #     x = np.array([fs.board], dtype=np.float32).astype(np.float32)
        #     maxQnew = np.max(self.model(x).data[0])
        # update = r + self.gamma * maxQnew
        # # print(('Prev Board:{} ,ACT:{}, Next Board:{}, Get Reward {}, Update {}').format(s.board,a,fs.board,r,update))
        # # print(('PREV:{}').format(self.last_pred))
        # self.last_pred[a] = update
        #
        # x = np.array([s.board], dtype=np.float32).astype(np.float32)  # データ
        # t = np.array([self.last_pred], dtype=np.float32).astype(np.float32)  # 教師
        # self.model.zerograds()
        # loss = self.model(x, t, train=True)
        # loss.backward()
        # self.optimizer.update()
