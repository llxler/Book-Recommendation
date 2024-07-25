import numpy as np

class AlgoBase:
    def __init__(self):
        self.trainset = None

    def fit(self, trainset):
        """
        Fit the algorithm on the training set.
        """
        self.trainset = trainset

    def test(self, testset):
        """
        Test the algorithm on the test set.
        """
        raise NotImplementedError
