import treenode
import mcts
import Board
import random
import operator
import copy
import state
from In_Out_put import In_Out_put

class MCTSPlayer:
    def __init__(self,root=None):
        self.reader = In_Out_put()
        self.L = self.reader.LENGTH
        s = state.State(Board.Board(self.L))
        root_node = treenode.Node(s) if root is None else root
        self.mcts = mcts.MCTS(root_node)
        self.board_before = Board.Board(self.L)

    def act(self, board_,opponent_action):
        state_before = state.State(self.board_before)
        node_before = treenode.Node(state_before)
        found_node = self.mcts.find(node_before)
        assert found_node is not None
        if opponent_action is None:
            pass
        elif opponent_action in found_node.children:
            found_node = found_node.children[opponent_action]
        else:
            found_node = found_node.expand(opponent_action)

        self.mcts.start(found_node)

        state_after = state.State(board_)
        node_after = treenode.Node(state_after)

        found_node = self.mcts.find(node_after)
        assert found_node is not None


        action = max(found_node.children, key=lambda x: found_node.children[x].ucb1())
        self.board_before = copy.deepcopy(board_)
        self.board_before.put(action)

        # self.board_before.show_board()
        return action


# p1 = "0000000000000000000000000001000000111000000000000000000000000000"
# p2 = "0000000000000000000000000000100000000000000000000000000000000000"
# p1 = Board.BoardUtil.string_to_bit(p1)
# p2 = Board.BoardUtil.string_to_bit(p2)
m = MCTSPlayer()

a = Board.Board(m.__init__())
action = 29


print(m.act(a,action))
