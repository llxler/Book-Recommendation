from sklearn.cluster import KMeans

class CoClustering(AlgoBase):
    def __init__(self, n_clusters=2):
        super().__init__()
        self.n_clusters = n_clusters
        self.user_clusters = None
        self.item_clusters = None

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

        # Apply KMeans clustering
        user_kmeans = KMeans(n_clusters=self.n_clusters)
        item_kmeans = KMeans(n_clusters=self.n_clusters)

        user_labels = user_kmeans.fit_predict(matrix)
        item_labels = item_kmeans.fit_predict(matrix.T)

        self.user_clusters = {user: user_labels[user_index[user]] for user in unique_users}
        self.item_clusters = {item: item_labels[item_index[item]] for item in unique_items}

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            user_cluster = self.user_clusters.get(u, -1)
            item_cluster = self.item_clusters.get(i, -1)

            if user_cluster == item_cluster:
                pred = 3  # Arbitrary value when clusters match
            else:
                pred = 2  # Arbitrary value when clusters don't match

            predictions.append((u, i, pred))
        return predictions
