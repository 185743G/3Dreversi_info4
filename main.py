# const value
from Constants import WHITE, BLACK
from Players_Osero_game import Players_Osero_game

if __name__ == '__main__':
    size = 1 # 1:4*4*4  2:6*6*6  3:8*8*8
    result = [0, 0, 0, 0, 0]
    white_sum = 0
    black_sum = 0

    step = 100

    with open("logs/battle.log", "w") as f:
        f.write("")

    game_a = Players_Osero_game(size)

    for i in range(1000):
        for j in range(step):
            game_a.reset(size)
            while (game_a.is_continue() and game_a.is_not_Quit()):
                game_a.update()
            result[game_a.board.winner] += 1
        print("Whiteの勝利数: {}".format(result[WHITE]))
        print("Blackの勝利数: {}".format(result[BLACK]))

        w_step = result[WHITE] - white_sum
        b_step = result[BLACK] - black_sum
        d_step = step - (w_step + b_step)

        white_sum = result[WHITE]
        black_sum = result[BLACK]

        xy_str = "{} {}\n".format(i*step, w_step/step)
        with open("logs/battle.log", "a") as f:
            f.write(xy_str)



    # win_rate = [white_step/step for white_step in white_steps]
    #
    # x = [i * step for i in range(len(win_rate))]
    # y = win_rate
    #
    # xy_str = ""
    # for x_i, y_i in zip(x, y):
    #     row = "{} {}".format(x_i, y_i)
    #     xy_str += row + "¥n"
    #
    # with open("logs/battle.log", "w") as f:
    #     f.write(xy_str)


