import numpy as np


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
