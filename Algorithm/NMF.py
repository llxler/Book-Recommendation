from sklearn.decomposition import NMF

class NMF(AlgoBase):
    def __init__(self, n_components=2):
        super().__init__()
        self.n_components = n_components
        self.model = None

    def fit(self, trainset):
        super().fit(trainset)
        users, items, ratings = zip(*trainset)
        unique_items = list(set(items))

        # Create item-user matrix
        item_index = {item: idx for idx, item in enumerate(unique_items)}
        matrix = np.zeros((len(unique_items), len(trainset)))
        for u, i, r in trainset:
            matrix[item_index[i], u] = r

        # Apply NMF
        self.model = NMF(n_components=self.n_components)
        self.model.fit(matrix)

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            # Predict using NMF
            pred = np.dot(self.model.components_[:, u], self.model.components_[i, :])
            predictions.append((u, i, pred))
        return predictions
