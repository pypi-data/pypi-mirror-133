import numpy as np


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
