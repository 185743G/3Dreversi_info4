from Constants import WHITE, BLACK, EMPTY, WALL, ThreeD, players, symbols, X, Y, Z
import numpy as np

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

    def get_flattend_board(self):#リスト形式でboard情報を得る
        return np.array(self.board).flatten()

    # unflattenなインデックスをflattenにして返す.
    def get_flatten_point(self, flatten_point):
        a = flatten_point[0] * self.L*self.L
        b = a + flatten_point[1] * self.L
        ret = b + flatten_point[2]
        return ret

    # flattenなインデックスをunflatternなポイントに返す
    def get_unflatten_point(self, i):
        z = i // (self.L*self.L)
        mod = i % (self.L*self.L)
        y = mod // self.L
        mod = mod % self.L
        x = mod
        return [z, y, x]

    def initialize(self, length):  # boardにオセロ の初期配置をする関数
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

#           test cord for to show initial place
#        for c in range(self.z):
#            for d in range(self.y):
#                for e in range(self.x):
#                    print(symbols[self.board[e][d][c]],end=' ')
#                print("")
#            print("")

    def open(self):#ボードをターミナル上に表示する
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

    def chk_win(self,isDpass):#勝利判定
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

        if num_Stones[EMPTY] == 0 or num_Stones[WHITE] == 0 or num_Stones[BLACK] == 0 or isDpass:
            # if game is over,select winner
            self.set_winner(num_Stones)

    # def get_winner(self):


    def set_winner(self, num_Stones):#勝利判定できる盤面になればこの関数で勝者を調べる
    # test cord for to show final place
#        for c in range(self.z):
#            for d in range(self.y):
#                for e in range(self.x):
#                    print(symbols[self.board[e][d][c]],end=' ')
#                print("")
#            print("")
#
        if num_Stones[WHITE] < num_Stones[BLACK]:
            self.winner = BLACK
        elif num_Stones[WHITE] > num_Stones[BLACK]:
            self.winner = WHITE
        elif num_Stones[WHITE] == num_Stones[BLACK]:
            self.winner = WALL
#        print("%d　対　%d　勝者は...%s!!!\n" %( num_Stones[WHITE],num_Stones[BLACK],players[self.winner]))
        return self.winner

    def get_possible_pos(self):
        pos=[]
        # for i in range(64):
        #     if self.board[i]==EMPTY:
        #         pos.append(i)
        for z in range(self.z-2):
            for y in range(self.y-2):
                for x in range(self.x-2):
                    point = [x+1,y+1,z+1]
                    if self.board[z+1][y+1][x+1]==EMPTY:
                        pos.append(point)
        return pos


    def chk_Cell_Ahead(self, pos, dirc):#位置pos+周囲一マスのうちのどこか(dirc)のマスを調べる
        global X, Y, Z
        return self.board[pos[X] + dirc[X]][pos[Y] + dirc[Y]][pos[Z] + dirc[Z]]

    def change_turn(self):
        # change turn counter and show whose turn is now
        self.turn = 3 - self.turn
        self.ENEMY = 3 - self.turn
        self.ALLY = self.turn
#        print("！！%sのターン！！\n" % players[self.turn])

    def set_Next_Position(self, pos, dirc):
        pos = [pos[X] + dirc[X],pos[Y] + dirc[Y],pos[Z] + dirc[Z]]
        return pos
    
    def greedy(self,choice):
        num_stone_get = []
        greedychoices = []
        for i in choice:
            num_stone_get.append(len(self.get_flip_list(i)))
        for j in range(len(choice)):
            if num_stone_get[j] == max(num_stone_get):
                greedychoices.append(choice[j])
        return greedychoices
        
    def humble(self,choice):
        num_stone_get = []
        humblechoices = []
        for i in choice:
            num_stone_get.append(len(self.get_flip_list(i)))
        for j in range(len(choice)):
            if num_stone_get[j] == min(num_stone_get):
                humblechoices.append(choice[j])
        return humblechoices
            
            
    
    def can_put_stone_all(self):
        points = []
        for z in range(self.z-2):
            for y in range(self.y-2):
                for x in range(self.x-2):
                    point = [x+1,y+1,z+1]
                    if self.can_put_stone(point):
                        points.append(point)
        return points


    def can_put_stone(self, pos):
        here = [0, 0, 0]
        result = False

        if self.chk_Cell_Ahead(pos, here) == EMPTY:
            for i in range(len(self.direction)):
                if self.direction[i] != here:
                    p = self.set_Next_Position(pos, here)
                    while (self.chk_Cell_Ahead(p, self.direction[i]) == self.ENEMY):
                        p = self.set_Next_Position(p, self.direction[i])
                        if self.chk_Cell_Ahead(p, self.direction[i]) == self.ALLY:
                            result = True
                if result == True:
                    break

        return result

    def flip(self, pos):
        here = [0, 0, 0]
        self.setCell(pos, self.ALLY)
        
        flip_pos_list = [pos]
        for i in range(len(self.direction)):
            if self.direction[i] != here:
                p = self.set_Next_Position(pos, here)
                pos_list = []
                while (self.chk_Cell_Ahead(p, self.direction[i]) == self.ENEMY):
                    p = self.set_Next_Position(p, self.direction[i])
                    pos_list.append(p)
                    if self.chk_Cell_Ahead(p, self.direction[i]) == self.ALLY:
                        for j in pos_list:
                            flip_pos_list.append(j)
        for k in flip_pos_list:
            self.setCell(k, self.ALLY)

    def get_flip_list(self, pos):
        here = [0, 0, 0]
#        self.setCell(pos, self.ALLY)
        flip_pos_list = [pos]
        for i in range(len(self.direction)):
            if self.direction[i] != here:
                p = self.set_Next_Position(pos, here)
                pos_list = []
                while (self.chk_Cell_Ahead(p, self.direction[i]) == self.ENEMY):
                    p = self.set_Next_Position(p, self.direction[i])
                    pos_list.append(p)
                    if self.chk_Cell_Ahead(p, self.direction[i]) == self.ALLY:
                        for j in pos_list:
                            flip_pos_list.append(j)
                            
        return flip_pos_list

