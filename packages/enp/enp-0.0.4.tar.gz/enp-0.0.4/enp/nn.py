import numpy as np


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


class Conv2D:
    def __init__(self, prev_layer, in_channels, out_channels, kernel_size, activation, stride=1, padding=0):
        self.prev_layer = prev_layer
        self.next_layer = None
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        k = 1 / (in_channels * kernel_size * kernel_size)
        self.b = np.random.uniform(low=-np.sqrt(k), high=np.sqrt(k), size=(1, 1, 1, out_channels))
        self.W = np.random.uniform(low=-np.sqrt(k), high=np.sqrt(k),
                                   size=(kernel_size, kernel_size, in_channels, out_channels))
        self.Z = None
        self.dW = None
        self.db = None
        self.dA = None
        self.dZ = None
        self.activation = activation
        self.A = None

    def zero_padding(self, X):
        X_pad = np.pad(X, ((0, 0), (self.padding, self.padding), (self.padding, self.padding), (0, 0)), mode='constant',
                       constant_values=(0, 0))

        return X_pad

    def conv_single_step(self, a_slice_prev, W, b):
        s = np.multiply(a_slice_prev, W)
        Z = np.sum(s)
        Z = Z + float(b)
        return Z

    def only_convolution_forward(self):
        (m, n_H_prev, n_W_prev, n_C_prev) = self.prev_layer.A.shape[0], self.prev_layer.A.shape[1], \
                                            self.prev_layer.A.shape[2], self.prev_layer.A.shape[3]

        (f, f, n_C_prev, n_C) = self.W.shape[0], self.W.shape[1], self.W.shape[2], self.W.shape[3]

        n_H = int(int(n_H_prev + 2 * self.padding - f) / self.stride + 1)
        n_W = int(int(n_W_prev + 2 * self.padding - f) / self.stride + 1)

        # Initialize the output volume Z with zeros. (≈1 line)
        self.Z = np.zeros([m, n_H, n_W, n_C])

        # Create A_prev_pad by padding A_prev
        A_prev_pad = self.zero_padding(self.prev_layer.A)

        for i in range(m):
            # a_prev_pad = A_prev_pad[i]
            for h in range(n_H):
                vert_start = self.stride * h
                vert_end = vert_start + f

                for w in range(n_W):
                    horiz_start = self.stride * w
                    horiz_end = horiz_start + f

                    for c in range(n_C):
                        a_slice_prev = A_prev_pad[i, vert_start:vert_end, horiz_start:horiz_end, :]

                        weights = self.W[:, :, :, c]
                        biases = self.b[:, :, :, c]
                        self.Z[i, h, w, c] = self.conv_single_step(a_slice_prev, weights, biases)

        assert (self.Z.shape == (m, n_H, n_W, n_C))

    def forward(self):
        if self.activation == "sigmoid":
            self.only_convolution_forward()
            self.A = sigmoid(self.Z)

        elif self.activation == "relu":
            self.only_convolution_forward()
            self.A = relu(self.Z)

    def only_convolution_backward(self):
        (m, n_H_prev, n_W_prev, n_C_prev) = self.prev_layer.A.shape
        (f, f, n_C_prev, n_C) = self.W.shape

        (m, n_H, n_W, n_C) = self.dZ.shape

        self.prev_layer.dA = np.random.randn(m, n_H_prev, n_W_prev, n_C_prev)
        self.dW = np.random.randn(f, f, n_C_prev, n_C)
        self.db = np.random.randn(f, f, n_C_prev, n_C)

        A_prev_pad = self.zero_padding(self.prev_layer.A)
        dA_prev_pad = self.zero_padding(self.prev_layer.dA)

        for i in range(m):  # loop over the training examples
            a_prev_pad = A_prev_pad[i, :, :, :]
            da_prev_pad = dA_prev_pad[i, :, :, :]

            for h in range(n_H):
                for w in range(n_W):
                    for c in range(n_C):
                        vert_start = self.stride * h
                        vert_end = self.stride * h + f
                        horiz_start = self.stride * w
                        horiz_end = self.stride * w + f

                        a_slice = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]

                        da_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :] += self.W[:, :, :, c] * self.dZ[
                            i, h, w, c]
                        self.dW[:, :, :, c] += a_slice * self.dZ[i, h, w, c]
                        self.db[:, :, :, c] += self.dZ[i, h, w, c]

            self.prev_layer.dA[i, :, :, :] = da_prev_pad[self.padding:-self.padding, self.padding:-self.padding, :]
        assert (self.prev_layer.dA.shape == (m, n_H_prev, n_W_prev, n_C_prev))

    def backward(self):
        if self.activation == "relu":
            self.dZ = relu_backward(self.dA, self.Z)
            self.only_convolution_backward()

        elif self.activation == "sigmoid":
            self.dZ = sigmoid_backward(self.dA, self.Z)
            self.only_convolution_backward()


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

    def predict(self, X):
        self.layers[0].A = X
        for l in range(1, len(self.layers) - 1):
            self.layers[l].forward()
        output = self.layers[-2].A
        return output

    def train(self, x, y, num_iterations, print_cost=True):
        costs = []
        for i in range(0, num_iterations):
            self.forward(x, y)
            self.backward(y)
            self.SGD()

            cost = self.layers[-1].A
            if print_cost and i % 100 == 0:
                print("Cost after iteration %i: %f" % (i, cost))


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
