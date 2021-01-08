# const value
from Players_Osero_game import Players_Osero_game

if __name__ == '__main__':
    size = 1 # 1:4*4*4  2:6*6*6  3:8*8*8
    game_a = Players_Osero_game(size)
    while (game_a.is_continue() and game_a.is_not_Quit()):
        game_a.update()
    

