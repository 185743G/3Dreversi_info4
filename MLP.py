import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F  # Functionは、パラメータを持たない関数です。
import chainer.links as L  # links パラメーターを持つ関数
import numpy as np
class MLP(chainer.Chain):
    # L.linear(input_dim_num, out_dim_num) 全結合層
    def __init__(self, n_in, n_units, n_out):
        super(MLP, self).__init__(
            l1=L.Linear(n_in, n_units),  # first layer
            l2=L.Linear(n_units, n_units),  # second layer
            l3=L.Linear(n_units, n_units),  # Third layer
            l4=L.Linear(n_units, n_out),  # output layer
        )
    """
    mean squad error = 二乗誤差
    leaky relu : reluの一つ
    L -> F -> L
    """
    def __call__(self, x, t=None, train=False):
        h = F.leaky_relu(self.l1(x))
        h = F.leaky_relu(self.l2(h))
        h = F.leaky_relu(self.l3(h))
        h = self.l4(h)

        if train:
            return F.mean_squared_error(h,t)
        else:
            return h

    def get(self,x):
        # input x as float, output float
        return self.predict(Variable(np.array([x]).astype(np.float32).reshape(1,1))).data[0][0]