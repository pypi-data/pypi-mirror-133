import numpy as np
from .activations import *

"""
Warning: work in progress!
"""


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
        self.Z = np.zeros([m, n_H, n_W, n_C])

        A_prev_pad = self.zero_padding(self.prev_layer.A)

        for i in range(m):
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

        for i in range(m):
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
