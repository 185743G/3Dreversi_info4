import copy
import random
import sqlite3


from Board import Board
from Constants import WHITE, BLACK, EMPTY
from RandomPlayer import RandomPlayer
from Util import get_opponent
import pickle


players = [RandomPlayer(WHITE), RandomPlayer(BLACK)]
PASS = -2
L = 6
board = Board(L)
BATTLE_NUM = 100
AI_TURN = WHITE


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


history = History()


def get_reward(board):
    failed_put_stone = 0
    board_c = copy.deepcopy(board)
    for player in players:
        board_c.turn = player.myturn
        if len(board_c.can_put_stone_all()) == 0:
            failed_put_stone += 1

    if failed_put_stone == 2:  #
        winner = board_c.get_winner()
        if winner == AI_TURN:
            return 1
        elif winner == get_opponent(AI_TURN):
            return -1
        else:
            return -0.5
    else:
        return 0


def generate_experience_replay():
    board_c = copy.deepcopy(board)
    board_c.turn = random.choice([WHITE, BLACK])
    is_continue = True
    while is_continue:
        s=None
        a=None
        r=0
        s2=None
        t=0

        turn = board_c.turn

        s=copy.deepcopy(board_c).get_flattend_board()  # 現在のstate


        # プレイヤー選択
        player = None
        for i in range(len(players)):
            if players[i].myturn == turn:
                player = players[i]
                break

        # 入力処理
        input_pos = player.act(board_c)


        # 置けなかったら
        if input_pos == [PASS] * 3:
            board_c.change_turn()
            if len(board_c.can_put_stone_all()) == 0:
                t = 1
                is_continue = False
        else:  # 置けたら
            if board_c.can_put_stone(input_pos):  # 一応チェック
                a=board_c.get_flatten_point(input_pos)

                board_c.flip(input_pos)

                r=get_reward(board_c)

                board_c.change_turn()
                s2=copy.deepcopy(board_c).get_flattend_board()
            else:
                raise Exception

        if turn == AI_TURN and is_continue:
            game_result = GameResult(s, a, r, s2, t)
            history.addGameResults(game_result)


if __name__ == "__main__":

    for _ in range(BATTLE_NUM):
        generate_experience_replay()

    with open('history.pickle', 'wb') as f:
        pickle.dump(history, f)

    with open('history.pickle', 'rb') as f:
        history_p = pickle.load(f)


    print("hoge")
