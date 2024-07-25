import random

class NormalPredictor(AlgoBase):
    def __init__(self):
        super().__init__()

    def fit(self, trainset):
        pass

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            # Random prediction
            pred = random.uniform(1, 5)  # Assuming ratings range from 1 to 5
            predictions.append((u, i, pred))
        return predictions
