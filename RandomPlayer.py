import random
class RandomPlayer:
    def __init__(self, turn):
        self.name = "Random"
        self.myturn = turn

    def act(self, board):
        acts = board.can_put_stone_all()
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self, board):
        pass
