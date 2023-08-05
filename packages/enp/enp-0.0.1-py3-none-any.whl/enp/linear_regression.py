import numpy as np


class LinearRegression:
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, x, y):
        ones = np.ones(x.shape[0])
        x = np.hstack((ones, x))
        weights = np.linalg.inv(x.T @ x) @ x.T @ y
        self.intercept_ = weights[0]
        self.coef_ = weights[1:]
