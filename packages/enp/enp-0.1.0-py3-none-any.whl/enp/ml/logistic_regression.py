import numpy as np

"""
You can download dataset from https://www.kaggle.com/c/digit-recognizer/data
Set path_to_dataset to the path to the dataset
"""


class LogisticRegression:
    def __init__(self, penatly='l2', c=1., max_iter=100, random_state=42):
        self.penatly = penatly
        self.c = c
        self.coef_ = None
        self.intercept_ = None
        self.n_features_in_ = None
        self.max_iter = max_iter
        self.A = None
        self.learning_rate = 0.005
        self.dw = None
        self.db = None
        self.random_state = random_state

    def fit(self, x, y):
        self.n_features_in_ = x.shape[1]
        self._initialize_parameters()
        for i in range(self.max_iter):
            self.forward(x, y)
            self.backward(x, y)
            self.gradient_descent()
        return self

    def predict(self, x):
        p = self._sigmoid(np.dot(self.coef_.T, x.T) + self.intercept_)
        p = (p >= 0.5).astype(np.int32)
        return p

    def predict_proba(self, x):
        return self._sigmoid(np.dot(self.coef_.T, x.T) + self.intercept_)

    def forward(self, x, y):
        m = x.shape[0]
        self.A = self._sigmoid(np.dot(self.coef_.T, x.T) + self.intercept_)
        cost = np.sum(((- np.log(self.A)) * y + (-np.log(1 - self.A)) * (1 - y))) / m

    def backward(self, x, y):
        m = x.shape[1]
        self.dw = (np.dot(x.T, (self.A - y).T)) / m
        self.db = (np.sum(self.A - y)) / m

    def gradient_descent(self):
        self.coef_ = self.coef_ - (self.learning_rate * self.dw)
        self.intercept_ = self.intercept_ - (self.learning_rate * self.db)

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def _initialize_parameters(self):
        self.coef_ = np.zeros((self.n_features_in_, 1))
        self.intercept_ = 0
