from Board import Board
from Constants import WHITE, BLACK, EMPTY
from DQNPlayer import DQNPlayer
from In_Out_put import In_Out_put
from RandomPlayer import RandomPlayer
import numpy as np


class Players_Osero_game:
    def __init__(self,size_val):
        self.PASS = -2
        self.passmater = 0
        self.isDpass = False
        self.reader = In_Out_put(size_val)
        self.L = self.reader.LENGTH
        self.board = Board(self.L)
#        self.print_Usage()
        self.players = [DQNPlayer(WHITE), RandomPlayer(BLACK)]

    # L = (L-2)^3 width board will crate

    def is_continue(self):
        self.board.chk_win(self.isDpass)
        if self.board.winner == EMPTY:
            return True
        else:
            return False

    def is_not_Quit(self):
        ans = not self.reader.PCQUIT
        return ans

    def update(self):
        
        if self.board.turn == WHITE:
            input_pos = self.players[0].act(self.board)
        elif self.board.turn == BLACK:
            input_pos = self.players[1].act(self.board)


        if type(input_pos) is np.int64:
            input_pos = self.board.get_unflatten_point(input_pos)
        if self.is_not_Quit() == False:
            print("Thank you for playing")
            self.passmater = 0
        elif input_pos == [self.PASS, self.PASS, self.PASS]:
            self.board.change_turn()
            self.passmater += 1
            if self.passmater == 2:
                self.isDpass = True
            
        elif self.board.can_put_stone(input_pos):
            self.board.flip(input_pos)
            self.board.change_turn()
            self.passmater = 0
        else:
            self.passmater = 0
            print("指定した座標には置けませんでした")
#        self.board.open() #ここで盤面を表示

    def print_Usage(self):
        print("---    遊び方    ---\n パス: pass \n ゲームの終了 : quit\n 座標を入れる : 1 ~ %d\n" % (self.L - 1))
