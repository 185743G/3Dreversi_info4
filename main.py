# const value
from Constants import WHITE, BLACK
from Players_Osero_game import Players_Osero_game

if __name__ == '__main__':
    size = 1 # 1:4*4*4  2:6*6*6  3:8*8*8
    result = [0, 0, 0, 0, 0]
    for _ in range(100):
        for j in range(100):
            game_a = Players_Osero_game(size)
            while (game_a.is_continue() and game_a.is_not_Quit()):
                game_a.update()
            result[game_a.board.winner] += 1
        print("Whiteの勝利数: {}".format(result[WHITE]))
        print("Blackの勝利数: {}".format(result[BLACK]))



