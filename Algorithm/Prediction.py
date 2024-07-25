class Prediction:
    def __init__(self, uid, iid, r_ui, est, details=None):
        self.uid = uid
        self.iid = iid
        self.r_ui = r_ui
        self.est = est
        self.details = details

    def __repr__(self):
        return f"Prediction(uid={self.uid}, iid={self.iid}, r_ui={self.r_ui}, est={self.est})"
