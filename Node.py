class Node:
    def __init__(self, board, parent, act=None):
        self.state = board
        self.act = act
        self.parent = parent  # nullなら自分が根
        self.reward = 0.0   # t
        self.num = 1    # playoutの回数
        self.children = []
        # self.n = 0
        # self.t = 0

    def add_child(self, child_state, act):
        child = Node(child_state, self, act)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.num += 1



