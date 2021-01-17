import random
import numpy as np

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

class GreedyPlayer:
    def __init__(self,turn):
        self.name = "Greedy"
        self.myturn = turn
        self.PASS = -2
        
    def act(self,board):
        acts = []
        choice = board.can_put_stone_all()
        if len(choice) == 0:
            acts.append([self.PASS,self.PASS,self.PASS])
            i = 0
        else:
            acts = board.greedy(choice)
            i = random.randrange(len(acts))
        return acts[i]
        
    def getGameResult(self, board):
        pass
        
class HumblePlayer:
    def __init__(self,turn):
        self.name = "Humble"
        self.myturn = turn
        self.PASS = -2
    def act(self,board):
        acts = []
        choice = board.can_put_stone_all()
        if len(choice) == 0:
            acts.append([self.PASS,self.PASS,self.PASS])
            i = 0
        else:
            acts = board.humble(choice)
            i = random.randrange(len(acts))
        return acts[i]
    def getGameResult(self, board):
        pass

class GenLPlayer:
    def __init__(self,turn):
        self.name = "GeneL"
        self.myturn = turn
        self.PASS = -2
        self.gene = [random.randrange(2) for i in range(1000)]
        self.readC = 0
    def act(self,board):
        acts = []
        choice = board.can_put_stone_all()
        if len(choice) == 0:
            acts.append([self.PASS,self.PASS,self.PASS])
            i = 0
        else:
            if self.gene[self.readC] ==1:
                acts = board.greedy(choice)
            else:
                acts = board.humble(choice)
            i = random.randrange(len(acts))
        self.readC += 1
        return acts[i]
    def getGameResult(self, board):
#        r = 0
#        if self.last_move is not None:
#            if board.winner is None:
#                self.learn(self.last_board, self.last_move, 0, board)
#                pass
#            else:
#                if
        pass
#    def mutation(self):
#        for i in range(5):
#            self.gene =
