# const value
from Constants import WHITE, BLACK
from Players_Osero_game import Players_Osero_game

print("reversi")

size = 1 # 1:4*4*4  2:6*6*6  3:8*8*8
result = [0, 0, 0, 0, 0]
game_a = Players_Osero_game(size)

print(result)

for _ in range(1000):
    for j in range(100):
        game_a.reset(size)
        while (game_a.is_continue() and game_a.is_not_Quit()):
            game_a.update()
        result[game_a.board.winner] += 1
    print("Whiteの勝利数: {}".format(result[WHITE]))
    print("Blackの勝利数: {}".format(result[BLACK]))



