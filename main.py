# const value
import random

EMPTY = 0  # no object in acell
WHITE = 1  # white storn in a cell
BLACK = 2  # black storn in a sell
WALL = 3  # recognizer for over the board
ThreeD = 3
X = 0  # X-axis
Y = 1  # Y-axis
Z = 2  # Z-axis
symbols = ['E', '○', '●', 'W']  # provisional graphics
players = ["none", "White", "Black"]  # player name list


class Board:
    # borad control and board instance in this class.

    def setCell(self, pos1, col):  # call and set cell player stone, no wall or empty
        if col == WHITE or col == BLACK:
            self.board[pos1[X]][pos1[Y]][pos1[Z]] = col

    def __init__(self, length):  # class values initializer
        self.x = length
        self.y = length
        self.z = length
        self.L = length
        self.board = [[[0] * length for i in range(length)] for i in range(length)]
        self.initialize(length)

    def initialize(self, length):  # borad initializer
        self.turn = WHITE
        self.ENEMY = 3 - self.turn
        self.ALLY = self.turn
        self.winner = EMPTY
        init_stone1 = self.L // 2 - 1  # 盤の中央に2*2*2で初期の石を配置する
        init_stone2 = self.L // 2  # 盤の中央に2*2*2で初期の石を配置する
        for a in range(self.y):
            for b in range(self.x):
                self.board[b][a][0] = WALL  # 盤の底面を壁に置き換え
                self.board[b][a][self.z - 1] = WALL  # 上面を
                self.board[b][0][a] = WALL  # 前面を
                self.board[b][self.y - 1][a] = WALL  # 背面を
                self.board[0][b][a] = WALL  # 左側面を
                self.board[self.x - 1][b][a] = WALL  # 右側面を

        self.board[init_stone1][init_stone2][init_stone2] = WHITE  # 中心点から左後上はシロ
        self.board[init_stone2][init_stone1][init_stone2] = WHITE  # 右前上
        self.board[init_stone2][init_stone2][init_stone1] = WHITE  # 右後下
        self.board[init_stone1][init_stone1][init_stone1] = WHITE  # 左前下
        self.board[init_stone1][init_stone1][init_stone2] = BLACK  # 中心点から左前上はクロ
        self.board[init_stone2][init_stone2][init_stone2] = BLACK  # 右後上
        self.board[init_stone1][init_stone2][init_stone1] = BLACK  # 左後下
        self.board[init_stone2][init_stone1][init_stone1] = BLACK  # 右前下

        self.direction = [[0] * ThreeD for i in range(3 ** ThreeD)]
        for i in range(len(self.direction)):
            self.direction[i] = [i // (ThreeD ** 2) - 1, (i // ThreeD) % ThreeD - 1, i % ThreeD - 1]

    #       test cord for to show initial place
    #         for c in range(self.z):
    #             for d in range(self.y):
    #                 for e in range(self.x):
    #                     print(symbols[self.board[e][d][c]],end=' ')
    #                 print("")
    #             print("")

    def open(self):
        num_Stones = [0] * len(players)

        for i in range(self.z - 2):
            for j in range(self.y - 1):
                if j == 0:
                    print(i + 1, end=' ')
                    for k in range(self.x - 2):
                        print(k + 1, end=' ')
                else:
                    print(j, end=' ')
                    for k in range(self.x - 2):
                        if self.board[k + 1][j][i + 1] == EMPTY:
                            print(symbols[EMPTY], end=' ')
                            num_Stones[EMPTY] += 1
                        elif self.board[k + 1][j][i + 1] == WHITE:
                            print(symbols[WHITE], end=' ')
                            num_Stones[WHITE] += 1
                        elif self.board[k + 1][j][i + 1] == BLACK:
                            print(symbols[BLACK], end=' ')
                            num_Stones[BLACK] += 1
                print("")

    def chk_win(self):
        num_Stones = [0] * len(players)

        for i in range(self.z - 2):
            for j in range(self.y - 2):
                for k in range(self.x - 2):
                    if self.board[k + 1][j + 1][i + 1] == EMPTY:
                        num_Stones[EMPTY] += 1
                    elif self.board[k + 1][j + 1][i + 1] == WHITE:
                        num_Stones[WHITE] += 1
                    elif self.board[k + 1][j + 1][i + 1] == BLACK:
                        num_Stones[BLACK] += 1

        if num_Stones[EMPTY] == 0 or num_Stones[WHITE] == 0 or num_Stones[BLACK] == 0:
            # if game is over,select winner
            self.set_winner(num_Stones)

    def set_winner(self, num_Stones):
        if num_Stones[WHITE] < num_Stones[BLACK]:
            self.winner = BLACK
        elif num_Stones[WHITE] > num_Stones[BLACK]:
            self.winner = WHITE
        elif num_Stones[WHITE] == num_Stones[BLACK]:
            self.winner = EMPTY
        print("勝者は...%s!!!\n" % players[self.winner])
        return self.winner

    def chk_Cell_Ahead(self, pos, dirc):
        global X, Y, Z
        return self.board[pos[X] + dirc[X]][pos[Y] + dirc[Y]][pos[Z] + dirc[Z]]

    #         bの座標からDir動いた座標のcellを確認

    def change_turn(self):
        # change turn counter and show whose turn is now
        self.turn = 3 - self.turn
        self.ENEMY = 3 - self.turn
        self.ALLY = self.turn
        print("！！%sのターン！！\n" % players[self.turn])

    def set_Next_Position(self, pos, dirc):
        for i in range(len(pos)):
            pos[i] = pos[i] + dirc[i]
        return pos

    def can_put_stone_all(self):
        points = []
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    point = [x,y,z]
                    if self.can_put_stone(point):
                        points.append(point)
        return points


    def can_put_stone(self, pos):
        here = [0, 0, 0]
        result = False

        if self.chk_Cell_Ahead(pos, here) == EMPTY:
            for i in range(len(self.direction)):
                p = []
                for j in self.set_Next_Position(pos, here):
                    p.append(j)

                if self.direction[i] != here:
                    if self.chk_Cell_Ahead(p, self.direction[i]) == self.ENEMY:
                        enemies = True
                        while (enemies):

                            p = self.set_Next_Position(p, self.direction[i])
                            if self.chk_Cell_Ahead(p, self.direction[i]) == self.ALLY:
                                enemies = False
                                result = True


                            elif self.chk_Cell_Ahead(p, self.direction[i]) == WALL or self.chk_Cell_Ahead(p,
                                                                                                          self.direction[
                                                                                                              i]) == EMPTY:

                                enemies = False
                            else:
                                enemies = True

                        if result == True:
                            break

        return result

    def flip(self, pos):
        here = [0, 0, 0]

        self.setCell(pos, self.ALLY)
        for i in range(len(self.direction)):
            flip_pos_list = []
            p = []
            for j in self.set_Next_Position(pos, here):
                p.append(j)
            if self.chk_Cell_Ahead(p, self.direction[i]) == self.ENEMY:
                enemies = True
                flip_pos_list.append(p)
                while (enemies):
                    p = self.set_Next_Position(p, self.direction[i])
                    if self.chk_Cell_Ahead(p, self.direction[i]) == self.ALLY:
                        enemies = False
                        for i in flip_pos_list:
                            self.setCell(i, self.ALLY)
                    elif self.chk_Cell_Ahead(p, self.direction[i]) != self.ENEMY:
                        enemies = False


class In_Out_put:

    def __init__(self):
        self.QUIT = -1
        self.PASS = -2
        self.COMMAND = 2
        self.ONEMORE = 3
        self.PCQUIT = False
        self.LENGTH = self.select_size()

    def is_position(self, char):
        result = False
        try:
            chk_char = int(char)
        except ValueError as e:
            return result
        for i in range(self.LENGTH - 2):
            if chk_char is i + 1:
                result = True
        return result

    def read_command(self, val):
        quit_or_pass_or_command = -1  # error flag
        if val == "quit":
            quit_or_pass_or_command = self.QUIT
        elif val == "pass":
            quit_or_pass_or_command = self.PASS
        elif self.is_position(val):
            quit_or_pass_or_command = self.COMMAND
        else:
            quit_or_pass_or_command = self.ONEMORE
        return quit_or_pass_or_command

    def read(self):
        i = 0
        coordinate_input = [0] * ThreeD
        read_command_up = True
        while read_command_up:
            if i == X:
                print("x座標を入力してください")
            elif i == Y:
                print("y座標を入力してください")
            elif i == Z:
                print("z座標を入力してください")
            val = input()

            if self.read_command(val) == self.QUIT:
                self.PCQUIT = True
                break
            if self.read_command(val) == self.PASS:
                coordinate_input = [self.PASS] * ThreeD
                break
            if self.read_command(val) == self.COMMAND:
                coordinate_input[i] = int(val)
                i = i + 1
            if self.read_command(val) == self.ONEMORE:
                print("指定した数または文字は不正です。")
            if i == 3:
                read_command_up = False
        return coordinate_input

    def select_size(self):
        size = 0

        print("ゲーム盤のサイズを左記の数字より指定してください　小{1,2,3}大")
        val = input()
        while True:
            value_is_int = True
            try:
                chk_char = int(val)
            except ValueError as e:
                value_is_int = False
            if value_is_int:
                if int(val) == 3 or int(val) == 2 or int(val) == 1:
                    break
            print("不正な値です")
            val = input()

        size = (int(val) + 2) * 2
        return size


class RandomPlayer:
    def __init__(self, turn):
        self.name = "Random"
        self.myturn = turn

    def act(self, board):
        acts = board.can_put_stone_all()
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self, board):
        pass




class Players_Osero_game:
    def __init__(self):
        self.PASS = -2
        self.reader = In_Out_put()
        self.L = self.reader.LENGTH
        self.board = Board(self.L)
        self.print_Usage()
        self.players = [RandomPlayer(WHITE), RandomPlayer(BLACK)]

    # L = (L-2)^3 width board will crate

    def is_continue(self):
        self.board.chk_win()
        if self.board.winner == EMPTY:
            return True
        else:
            return False

    def is_not_Quit(self):
        ans = not self.reader.PCQUIT
        return ans

    def update(self):
        self.board.open()
        if self.board.turn == WHITE:
            input_pos = self.players[0].act(self.board)
        elif self.board.turn == BLACK:
            input_pos = self.players[1].act(self.board)

        if self.is_not_Quit() == False:
            print("Thank you for playing")
        elif input_pos == [self.PASS, self.PASS, self.PASS]:
            self.board.change_turn()
        elif self.board.can_put_stone(input_pos):
            self.board.flip(input_pos)
            self.board.change_turn()
        else:
            print("指定した座標には置けませんでした")

    def print_Usage(self):
        print("---    遊び方    ---\n パス: pass \n ゲームの終了 : quit\n 座標を入れる : 1 ~ %d\n" % (self.L - 1))


import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np
from chainer import computational_graph as c


# Network definition, Multilayer perceptron
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



if __name__ == '__main__':
    game_a = Players_Osero_game()
    while (game_a.is_continue() and game_a.is_not_Quit()):
        game_a.update()

