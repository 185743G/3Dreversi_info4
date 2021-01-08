# const value
from Players_Osero_game import Players_Osero_game

if __name__ == '__main__':
    game_a = Players_Osero_game()
    while (game_a.is_continue() and game_a.is_not_Quit()):
        game_a.update()
    

