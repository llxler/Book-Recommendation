from numpy.linalg import svd

class SVDpp(AlgoBase):
    def __init__(self, k=2):
        super().__init__()
        self.k = k
        self.U = None
        self.S = None
        self.Vt = None
        self.Y = None

    def fit(self, trainset):
        super().fit(trainset)
        users, items, ratings = zip(*trainset)
        unique_users = list(set(users))
        unique_items = list(set(items))

        # Create user-item matrix
        user_index = {user: idx for idx, user in enumerate(unique_users)}
        item_index = {item: idx for idx, item in enumerate(unique_items)}
        matrix = np.zeros((len(unique_users), len(unique_items)))

        for u, i, r in trainset:
            matrix[user_index[u], item_index[i]] = r

        # Apply SVD with implicit feedback
        self.U, self.S, self.Vt = svd(matrix, full_matrices=False)
        self.Y = np.random.rand(len(unique_users), len(unique_items))  # Placeholder for item features

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            user_idx = u  # Assume u is already an index
            item_idx = i  # Assume i is already an index

            pred = np.dot(self.U[user_idx, :self.k], np.dot(np.diag(self.S[:self.k]), self.Vt[:self.k, item_idx])) + np.dot(self.Y[user_idx, :], self.Vt[:, item_idx])
            predictions.append((u, i, pred))
        return predictions
