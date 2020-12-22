from Board import Board
from Constants import WHITE, BLACK, EMPTY
from In_Out_put import In_Out_put
from RandomPlayer import RandomPlayer


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
