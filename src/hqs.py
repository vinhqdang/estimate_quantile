from kll_sketch import KLL
from tdigest import TDigest

class HQS:
    def __init__(self, k):
        self.kll = KLL(k)
        self.tdigest = TDigest()

    def insert(self, item):
        self.kll.insert(item)
        self.tdigest.update(item)

    def query(self, quantile):
        if 0.1 <= quantile <= 0.9:
            return self.kll.query(quantile)
        else:
            return self.tdigest.percentile(quantile * 100)
