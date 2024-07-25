from collections import defaultdict
import numpy as np

class SlopeOne(AlgoBase):
    def __init__(self):
        super().__init__()
        self.diffs = defaultdict(lambda: defaultdict(float))
        self.counts = defaultdict(lambda: defaultdict(int))

    def fit(self, trainset):
        super().fit(trainset)
        for u, i, r in trainset:
            for i2, r2 in trainset:
                if i != i2:
                    self.diffs[i][i2] += r - r2
                    self.counts[i][i2] += 1

    def test(self, testset):
        predictions = []
        for u, i, _ in testset:
            total = 0
            count = 0
            for i2 in self.diffs[i]:
                if self.counts[i][i2] > 0:
                    total += self.diffs[i][i2] / self.counts[i][i2]
                    count += 1
            pred = total / count if count > 0 else 3  # Default prediction value
            predictions.append((u, i, pred))
        return predictions
