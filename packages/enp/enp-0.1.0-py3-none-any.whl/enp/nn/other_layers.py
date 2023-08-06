import numpy as np


class InputLayer:
    def __init__(self, layer_dim):
        self.A = None
        self.layer_dim = layer_dim
        self.next_layer = None


class BCELoss:
    def __init__(self, layer_dim, prev_layer):
        self.prev_layer = prev_layer
        self.dA = None
        self.A = None

    def forward(self, Y):
        m = Y.shape[1]
        self.A = (1. / m) * (-np.dot(Y, np.log(self.prev_layer.A).T) - np.dot(1 - Y, np.log(1 - self.prev_layer.A).T))
        self.A = np.squeeze(
            self.A)  # To make sure your cost's shape is what we expect (e.g. this turns [[17]] into 17).
        assert (self.A.shape == ())

    def backward(self, Y):
        self.prev_layer.dA = - (np.divide(Y, self.prev_layer.A) - np.divide(1 - Y, 1 - self.prev_layer.A))


class Flatten:
    def __init__(self, prev_layer, layer_dim):
        self.prev_layer = prev_layer
        self.A = None
        self.layer_dim = layer_dim
        self.next_layer = None

    def forward(self):
        self.A = np.reshape(self.prev_layer.A, (self.prev_layer.A.shape[0], -1))

    def backward(self):
        pass
