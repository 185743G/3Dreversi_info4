import copy
import random
import sqlite3



from Board import Board
from Constants import WHITE, BLACK, EMPTY
from RandomPlayer import RandomPlayer
from Util import get_opponent
import pickle

from History import History
from GameResult import GameResult

dbname = 'TEST.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

# s, a, r, s2, t
def drop_table():
    cur.execute("drop table history")

def create_table():
    cur.execute('CREATE TABLE history(id INTEGER PRIMARY KEY AUTOINCREMENT,s TEXT, a INTEGER, r INTEGER, s2 TEXT, t INTEGER)')

def insert_gameResult(record):
    cur.execute('insert into history(s, a , r , s2 , t) values(?, ?, ?, ?, ?)', (record[0], record[1], record[2], record[3], record[4]))

def delete_all():
    cur.execute('delete from history')

players = [RandomPlayer(WHITE), RandomPlayer(BLACK)]
PASS = -2
L = 6
board = Board(L)
BATTLE_NUM = 2000
AI_TURN = WHITE
WIN = 1
LOSE = -1
DRAW = -0.5



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
            return WIN
        elif winner == get_opponent(AI_TURN):
            return LOSE
        else:
            return DRAW
    else:
        return 0


def generate_experience_replay():
    board_c = copy.deepcopy(board)
    board_c.turn = random.choice([WHITE, BLACK])
    is_continue = True
    while True:
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
                # t = 1
                # is_continue = False
                break
        else:  # 置けたら
            if board_c.can_put_stone(input_pos):  # 一応チェック
                a=board_c.get_flatten_point(input_pos)

                board_c.flip(input_pos)

                r=get_reward(board_c)
                if r in [WIN, LOSE, DRAW]:
                    t = 1

                board_c.change_turn()
                s2=copy.deepcopy(board_c).get_flattend_board()

                if turn == AI_TURN:
                    game_result = GameResult(s, a, r, s2, t)
                    record = game_result.to_record()
                    insert_gameResult(record)
                    # history.addGameResults(game_result)
            else:
                raise Exception




if __name__ == "__main__":
    drop_table()
    try:
        create_table()
    except:
        print("already exist")



    for _ in range(BATTLE_NUM):
        generate_experience_replay()
    conn.commit()

    cur.close()
    conn.close()
    print("hoge")
