import numpy as np


class Linear:
    def __init__(self, layer_dim, previous_layer, activation):
        self.layer_dim = layer_dim
        self.prev_layer = previous_layer
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

        # assert (self.prev_layer.A.shape == self.prev_layer.A.shape)
        assert (self.dW.shape == self.W.shape)
        assert (self.db.shape == self.b.shape)

    def backward(self):
        if self.activation == "relu":
            self.dZ = relu_backward(self.dA, self.Z)
            self.only_linear_backward()

        elif self.activation == "sigmoid":
            self.dZ = sigmoid_backward(self.dA, self.Z)
            self.only_linear_backward()


class InputLayer:
    def __init__(self, layer_dim):
        self.A = None
        self.layer_dim = layer_dim
        self.next_layer = None


class CostLayer:
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


class Model:
    def __init__(self, learning_rate):
        self.layers = []
        self.cost = None
        self.learning_rate = learning_rate

    def forward(self, X, Y):
        self.layers[0].A = X
        for l in range(1, len(self.layers) - 1):
            self.layers[l].forward()
        self.cost = self.layers[-1].forward(Y)

    def backward(self, Y):
        self.layers[-1].backward(Y)
        for l in reversed(range(1, len(self.layers) - 1)):
            self.layers[l].backward()

    def SGD(self):
        for l in range(1, len(self.layers) - 1):
            self.layers[l].W = self.layers[l].W - self.learning_rate * self.layers[l].dW
            self.layers[l].b = self.layers[l].b - self.learning_rate * self.layers[l].db

    def predict(self, X, y):

        m = X.shape[1]
        p = np.zeros((1, m))

        self.forward(X, y)

        probas = self.layers[-2].A
        for i in range(0, probas.shape[1]):
            if probas[0, i] > 0.5:
                p[0, i] = 1
            else:
                p[0, i] = 0

        print("Accuracy: " + str(np.sum((p == y) / m)))

        return p


def sigmoid(Z):
    A = 1 / (1 + np.exp(-Z))
    return A


def relu(Z):
    A = np.maximum(0, Z)
    assert (A.shape == Z.shape)
    return A


def relu_backward(dA, Z):
    dZ = np.array(dA, copy=True)  # just converting dz to a correct object.
    dZ[Z <= 0] = 0
    # assert (dZ.shape == Z.shape)
    return dZ


def sigmoid_backward(dA, Z):
    s = 1 / (1 + np.exp(-Z))
    dZ = dA * s * (1 - s)
    assert (dZ.shape == Z.shape)
    return dZ
