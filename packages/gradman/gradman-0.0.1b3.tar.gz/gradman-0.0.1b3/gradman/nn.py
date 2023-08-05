import numpy as np

from gradman import Module, Tensor


class Linear(Module):
    def __init__(self, idim, odim):
        super(Linear, self).__init__()
        self.w = Tensor(np.random.randn(idim, odim))
        self.b = Tensor(np.random.randn(1, odim))

        self.params = ["w", "b"]

    def forward(self, i):
        o = (i @ self.w) + self.b
        return o


# activation functions

# loss functions
def mse(yp, yl):
    return (yl - yp).square().mean()
