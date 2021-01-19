import math
import random
import numpy as np
import copy

from Constants import EMPTY, BLACK
from Node import Node
from RandomPlayer import RandomPlayer
from Util import get_opponent

# TODO: 一手打つたび(act関数にてactを決めるたび)に木が初期化されている。直すべき?従来の実装は?
class MCTSPlayer:
    def __init__(self, turn):
        self.name = "mcts"
        self.myturn = turn
        self.all_playout_num = 1   # UCTの計算用
        self.playout_limit = 20   # 木全体のplayout回数の上限
        self.PASS = -2

    def act(self, board):
        root_state = copy.deepcopy(board)
        if len(board.can_put_stone_all()) == 0:
            return [self.PASS, self.PASS, self.PASS]
        act = self.mcts(root_state)
        return act

    def getGameResult(self, board):
        pass

    def mcts(self, root_state):
        # TODO: ある程度まで広げたら終了させるようにする。selectが呼び出された回数にする?
        # 渡されたstateを根として、末端まで辿っていく
        # nodes = [Node(root, None)]
        root = Node(root_state, None)

        for _ in range(self.playout_limit):
            leaf_node = self.select(root)

            if leaf_node.num == 1:
                # reward = self.playout(leaf_node)  # 最後まで実行して見て報酬を得る
                # # leaf_nodeの先祖のnumに+1, leaf_nodeの先祖のrewardに+reward
                # # leaf_node.num += 1
                # # leaf_node.reward += reward
                # leaf_node.update(reward)
                # node = leaf_node
                # while node.parent != None:
                #     node = node.parent
                #     node.update(reward)
                self.back_propagation(leaf_node)
            else:  #拡張
                self.expand(leaf_node)
                # for node in nodes:
                #     leaf_node.add_child(node)
                if len(leaf_node.children) > 0:
                    node = leaf_node.children[0]
                    self.back_propagation(node)


        c = self.choice(root)
        return c.act

    def choice(self, root_node):
        children = root_node.children
        max_index = 0
        for i in range(len(children)):
            if (children[max_index].reward / children[max_index].num) < (children[i].reward / children[i].num):
                max_index = i
        return children[max_index]


    def select(self, root_node):
        # ルートからUCT値が最大の子ノードを順にたどる
        node = root_node
        while len(node.children) != 0:
            node = self.get_best_child(node)
        return node


    def get_best_child(self, node):
        # nodeのchildの中から、UCT値が最大のノードを選んで返す
        children = node.children
        if len(children) == 0:
            return node
        else:
            max_index = 0
            for i in range(len(children)):
                if self.get_uct(children[max_index]) < self.get_uct(children[i]):
                    max_index = i
            return children[max_index]

    def get_uct(self, node):
        return (node.reward / node.num) + (math.sqrt(2) * math.sqrt(math.log(self.all_playout_num / node.num)))

    def expand(self, leaf_node): # leaf_nodeから考えられるnodeをstateから選び追加する
        board = leaf_node.state
        points = board.can_put_stone_all()
        for point in points:
            board_c = copy.deepcopy(board)
            board_c.flip(point)
            board_c.change_turn()
            leaf_node.add_child(board_c, point)
        # node = leaf_node.children[0]
        # self.back_propagation(node)


    def back_propagation(self, leaf_node):
        reward = self.playout(leaf_node)  # 最後まで実行して見て報酬を得る
        # leaf_nodeの先祖のnumに+1, leaf_nodeの先祖のrewardに+reward
        # leaf_node.num += 1
        # leaf_node.reward += reward
        leaf_node.update(reward)
        node = leaf_node
        while node.parent != None:
            node = node.parent
            node.update(reward)


    def playout(self, leaf_node):
        self.all_playout_num += 1
        opponent = RandomPlayer(BLACK)
        board_c = copy.deepcopy(leaf_node.state)
        while board_c.winner == EMPTY:
            if board_c.turn == self.myturn:
                input_pos = self.random_choice(board_c)
            elif board_c.turn == get_opponent(self.myturn):
                input_pos = opponent.act(board_c)

            if input_pos == [self.PASS]*3:
                board_c.change_turn()
                if len(board_c.can_put_stone_all()) == 0:
                    winner = board_c.get_winner()
                    return self.evaluate(winner)
            else:
                if board_c.can_put_stone(input_pos):
                    board_c.flip(input_pos)
                    board_c.change_turn()
                else:
                    print("指定した座標には置けません")


    def evaluate(self, winner):
        if winner == self.myturn:
            return 1
        elif winner == get_opponent(self.myturn):
            return 0
        else:
            return 0.5


    def random_choice(self, board):  # モンテカルロのプレイアウト用のrandom_choice。randomplayerのactとほとんど同じ
        acts = board.can_put_stone_all()
        if len(acts) == 0:
            acts.append([self.PASS, self.PASS, self.PASS])
        i = random.randrange(len(acts))
        return acts[i]



