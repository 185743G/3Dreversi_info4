# const value
from Players_Osero_game import Players_Osero_game

if __name__ == '__main__':
    result = []
    for _ in range(20):
        game_a = Players_Osero_game()
        while (game_a.is_continue() and game_a.is_not_Quit()):
            game_a.update()
        result.append(game_a.board.winner)

    print("Whiteの勝利数: {}".format(result.count(1)))
    print("Blackの勝利数: {}".format(result.count(2)))


