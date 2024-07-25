class BaselineOnly(AlgoBase):
    def __init__(self):
        super().__init__()
        self.global_mean = 0
        self.user_bias = {}
        self.item_bias = {}

    def fit(self, trainset):
        super().fit(trainset)
        # Calculate global mean
        ratings = [r for _, _, r in trainset]
        self.global_mean = np.mean(ratings)

        # Calculate user and item biases
        user_ratings = {}
        item_ratings = {}
        for u, i, r in trainset:
            if u not in user_ratings:
                user_ratings[u] = []
            if i not in item_ratings:
                item_ratings[i] = []

            user_ratings[u].append(r)
            item_ratings[i].append(r)

        for u in user_ratings:
            self.user_bias[u] = np.mean(user_ratings[u]) - self.global_mean

        for i in item_ratings:
            self.item_bias[i] = np.mean(item_ratings[i]) - self.global_mean

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            u_bias = self.user_bias.get(u, 0)
            i_bias = self.item_bias.get(i, 0)
            pred = self.global_mean + u_bias + i_bias
            predictions.append((u, i, pred))
        return predictions
