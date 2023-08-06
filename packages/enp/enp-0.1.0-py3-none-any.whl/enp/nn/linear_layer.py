import numpy as np
from .activations import *


class Linear:
    def __init__(self, layer_dim, prev_layer, activation):
        self.layer_dim = layer_dim
        self.prev_layer = prev_layer
        self.next_layer = None
        self.W = np.random.randn(self.layer_dim, self.prev_layer.layer_dim) / np.sqrt(self.prev_layer.layer_dim)
        self.b = np.zeros((self.layer_dim, 1))
        self.Z = None
        self.dW = None
        self.db = None
        self.dA = None
        self.dZ = None
        self.activation = activation
        self.A = None

    def only_linear_forward(self):
        self.Z = self.W.dot(self.prev_layer.A) + self.b

    def forward(self):
        if self.activation == "sigmoid":
            self.only_linear_forward()
            self.A = sigmoid(self.Z)

        elif self.activation == "relu":
            self.only_linear_forward()
            self.A = relu(self.Z)

        assert (self.A.shape == (self.W.shape[0], self.prev_layer.A.shape[1]))

    def only_linear_backward(self):
        m = self.prev_layer.A.shape[1]

        self.dW = 1. / m * np.dot(self.dZ, self.prev_layer.A.T)
        self.db = 1. / m * np.sum(self.dZ, axis=1, keepdims=True)
        self.prev_layer.dA = np.dot(self.W.T, self.dZ)

        assert (self.dW.shape == self.W.shape)
        assert (self.db.shape == self.b.shape)

    def backward(self):
        if self.activation == "relu":
            self.dZ = relu_backward(self.dA, self.Z)
            self.only_linear_backward()

        elif self.activation == "sigmoid":
            self.dZ = sigmoid_backward(self.dA, self.Z)
            self.only_linear_backward()
