from sklearn.neighbors import NearestNeighbors

class KNNBaseline(AlgoBase):
    def __init__(self, n_neighbors=5):
        super().__init__()
        self.n_neighbors = n_neighbors
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

        # Apply KNN
        self.model = NearestNeighbors(n_neighbors=self.n_neighbors, metric='cosine')
        self.model.fit(matrix)

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            # Predict using nearest neighbors
            neighbors = self.model.kneighbors([u], return_distance=False)
            pred = np.mean([self.model.fit_predict(neighbor) for neighbor in neighbors])
            predictions.append((u, i, pred))
        return predictions
