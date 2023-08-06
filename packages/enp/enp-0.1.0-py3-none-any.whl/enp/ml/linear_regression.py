import numpy as np


class LinearRegression:
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coef_ = None
        self.intercept_ = None

    def fit(self, x, y):
        if self.fit_intercept:
            ones = np.ones((x.shape[0], 1))
            x = np.hstack((ones, x))
        weights = np.linalg.inv(x.T @ x) @ x.T @ y
        if self.fit_intercept:
            self.intercept_ = weights[0]
            self.coef_ = weights[1:]
        else:
            self.coef_ = weights
        return self

    def predict(self, x):
        if self.fit_intercept:
            return x @ self.coef_ + self.intercept_
        else:
            return x @ self.coef_
