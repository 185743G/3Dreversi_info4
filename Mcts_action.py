import random
import math

class Mcts_action:
    
    def __init__(self, turn):
        self.name = "Mcts"
        self.myturn = turn
        self.PASS = -2

    def who_is_winner(self):
        winner = self.board.winner
        return winner

    # プレイアウト
    def playout(board):
        # 負けは状態価値-1
        
        if who_is_winner() == BLACK:
            return -1
        
        # 引き分けは状態価値0
        if who_is_winner() == WALL:
            return  0
        
        if who_is_winner() == WHITE:
            return 1
        # 次の状態の状態価値
        return -playout(next(random_action(board)))#今の状態からランダムを使ってゲーム終了まで進める。

    
    def next(self, action,board):
        pieces = board.state()
        #ここで実際に一個おく。
        #更新後の盤面を取得する。
        # pieces[action] = 1
        return State(pieces)


    # 最大値のインデックスを返す
    def argmax(collection, key=None):#モンテカルロ のところで2回使ってる。
        return collection.index(max(collection))


    # モンテカルロ木探索の行動選択
    def act(self,board):

        def random_action(self, board):
            acts = board.can_put_stone_all()
            if len(acts) == 0:
                acts.append([self.PASS,self.PASS,self.PASS])
            i = random.randrange(len(acts))
            return acts[i],board
        # モンテカルロ木探索のノードの定義
        class Node:
            # ノードの初期化
            def __init__(self,board):
                self.board = board
                self.state = board.state() # 状態
                self.w = 0 # 累計価値
                self.n = 0 # 試行回数
                self.child_nodes = None  # 子ノード群

            # 局面の価値の計算
            def evaluate(self):
                # ゲーム終了時
                if self.state.is_done():
                    # 勝敗結果で価値を取得
                    value = -1 if self.state.is_lose() else 0 # 負けは-1、引き分けは0

                    # 累計価値と試行回数の更新
                    self.w += value#累計価値
                    self.n += 1#試行回数
                    return value

                # 子ノードが存在しない時
                if not self.child_nodes:
                    # プレイアウトで価値を取得
                    value = playout(self.board)#playout関数に今の状態を入れてゲームを終了まで進める。returnは0 or -1

                    # 累計価値と試行回数の更新
                    self.w += value
                    self.n += 1

                    # 子ノードの展開
                    if self.n == 10: 
                        self.expand()
                    return value

                # 子ノードが存在する時
                else:
                    # UCB1が最大の子ノードの評価で価値を取得
                    value = -self.next_child_node().evaluate() 

                    # 累計価値と試行回数の更新
                    self.w += value
                    self.n += 1
                    return value

            # 子ノードの展開
            def expand(self):
                legal_actions = self.state.legal_actions()#合法手を更新
                self.child_nodes = []#次の手を用意
                for action in legal_actions:
                    self.child_nodes.append(Node(self.state.next(action)))#??

            # UCB1が最大の子ノードの取得
            def next_child_node(self):
                # 試行回数が0の子ノードを返す
                for child_node in self.child_nodes:#全ての子ノードを試行する。
                    if child_node.n == 0:
                        return child_node

                # UCB1の計算
                t = 0
                for c in self.child_nodes:
                    t += c.n
                ucb1_values = []
                for child_node in self.child_nodes:
                    ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

                # UCB1が最大の子ノードを返す
                return self.child_nodes[argmax(ucb1_values)]    
        
        # 現在の局面のノードの作成
        root_node = Node(self.state)
        root_node.expand()

        # 100回のシミュレーションを実行
        for _ in range(100):
            root_node.evaluate()

        # 試行回数の最大値を持つ行動を返す
        legal_actions = state.legal_actions()
        n_list = []
        for c in root_node.child_nodes:
            n_list.append(c.n)
        return legal_actions[argmax(n_list)]#最善手を返す。

    # モンテカルロ木探索とランダムおよびアルファベータ法、原始モンテカルロ探索の対戦

    # パラメータ
    EP_GAME_COUNT = 100  # 1評価あたりのゲーム数

    # 先手プレイヤーのポイント
    def first_player_point(ended_state):
        # 1:先手勝利, 0:先手敗北, 0.5:引き分け
        if ended_state.is_lose():
            return 0 if ended_state.is_first_player() else 1
        return 0.5

    # 1ゲームの実行
    def play(next_actions):
        # 状態の生成
        state = State()

        # ゲーム終了までループ
        while True:
            # ゲーム終了時
            if state.is_done():
                break

            # 行動の取得
            next_action = next_actions[0] if state.is_first_player() else next_actions[1]
            action = next_action(state)

            # 次の状態の取得
            state = state.next(action)

        # 先手プレイヤーのポイントを返す
        return first_player_point(state)#stateを引数に渡して、ポイントをつけてreturnする。

    # 任意のアルゴリズムの評価
    def evaluate_algorithm_of(label, next_actions):
        # 複数回の対戦を繰り返す
        total_point = 0
        for i in range(EP_GAME_COUNT):#100回まわす。
            # 1ゲームの実行
            if i % 2 == 0:
                total_point += play(next_actions)
            else:
                total_point += 1 - play(list(reversed(next_actions)))#??

            # 出力
            print('\rEvaluate {}/{}'.format(i + 1, EP_GAME_COUNT), end='')
        print('')

        # 平均ポイントの計算
        average_point = total_point / EP_GAME_COUNT
        print(label.format(average_point * 100))

    # VSランダム
    # next_actions = (mcts_action, random_action)
    # evaluate_algorithm_of('モンテカルロ木探索 VS ランダム {:.2f}%\n', next_actions)
