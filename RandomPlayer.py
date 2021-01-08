import random
class RandomPlayer:
    def __init__(self, turn):
        self.name = "Random"
        self.myturn = turn
        self.PASS = -2

    def act(self, board):
        acts = board.can_put_stone_all()
        if len(acts) == 0:
            acts.append([self.PASS,self.PASS,self.PASS])
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self, board):
        pass
        
