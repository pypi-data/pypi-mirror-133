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


class LogisticRegression:
    def __init__(self, penatly='l2', c=1., max_iter=100):
        self.penatly = penatly
        self.c = c
        self.coef_ = None
        self.intercept_ = None
        self.n_features_in_ = None

    def fit(self, x):
        pass

    def predict(self):
        pass

    def _calculate_loss_and_grad(self, x, y):
        m = y.size  # number of training examples
        J = 0
        theta = np.concatenate((self.intercept_, self.coef_))
        lambda_ = 1 / self.c

        grad = np.zeros(theta.shape)

        h = self._sigmoid(x.dot(theta.T))

        temp = theta
        temp[0] = 0

        J = (1 / m) * ((-y.dot(np.log(h))) - (1 - y).dot(np.log(1 - h))) + (
                (lambda_ / (2 * m)) * np.sum(np.square(temp)))
        grad = (1 / m) * (h - y).dot(x)
        grad = grad + (lambda_ / m) * temp

        return J, grad

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-z))


class KMeans:
    def __init__(self, n_clusters, max_iter, random_state=42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.cluster_centers_ = None
        self.labels_ = None
        self.random_state = random_state

    def fit(self, x):
        self._initialize_cluster_centers(x)
        for iteration in range(self.max_iter):
            self._find_closest_cluster_centers(x)
            self._compute_cluster_centers(x)
        return self

    def predict(self, x):
        x = np.array(x)
        labels_ = np.zeros(x.shape[0], dtype=int)
        n_samples = x.shape[0]
        for sample_id in range(n_samples):
            min_distance = float("inf")
            for cluster_center_id in range(self.n_clusters):
                distance = np.linalg.norm(x[sample_id, :] - self.cluster_centers_[cluster_center_id, :])
                if distance < min_distance:
                    min_distance = distance
                    labels_[sample_id] = cluster_center_id
        return labels_

    def _initialize_cluster_centers(self, x):
        np.random.seed(self.random_state)
        randidx = np.random.permutation(x.shape[0])
        self.cluster_centers_ = x[randidx[:self.n_clusters], :]

    def _find_closest_cluster_centers(self, x):
        self.labels_ = np.zeros(x.shape[0], dtype=int)
        n_samples = x.shape[0]
        for sample_id in range(n_samples):
            min_distance = float("inf")
            for cluster_center_id in range(self.n_clusters):
                distance = np.linalg.norm(x[sample_id, :] - self.cluster_centers_[cluster_center_id, :])
                if distance < min_distance:
                    min_distance = distance
                    self.labels_[sample_id] = cluster_center_id

    def _compute_cluster_centers(self, x):
        m, n = x.shape
        self.cluster_centers_ = np.zeros((self.n_clusters, n))
        coordinates_sums = np.zeros((self.n_clusters, n))
        number_of_examples = np.zeros(self.n_clusters)
        for sample_id in range(m):
            coordinates_sums[self.labels_[sample_id], :] = coordinates_sums[self.labels_[sample_id], :] + x[sample_id,
                                                                                                          :]
            number_of_examples[self.labels_[sample_id]] = number_of_examples[self.labels_[sample_id]] + 1
        for cluster_center_id in range(self.n_clusters):
            self.cluster_centers_[cluster_center_id, :] = coordinates_sums[cluster_center_id, :] / number_of_examples[
                cluster_center_id]
