class PredictionImpossible:
    def __init__(self, uid, iid):
        self.uid = uid
        self.iid = iid

    def __repr__(self):
        return f"PredictionImpossible(uid={self.uid}, iid={self.iid})"
