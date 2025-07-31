import numpy as np
from kll_sketch import KLL

class LBKLL:
    def __init__(self, k):
        self.kll = KLL(k)

    def insert(self, item):
        # To handle zero or negative values, we'll use a log-shift.
        # We'll add 1 to all values before taking the log.
        if item >= 0:
            self.kll.insert(np.log1p(item))

    def query(self, quantile):
        log_quantile = self.kll.query(quantile)
        if log_quantile is None:
            return None
        
        # Inverse transform
        return np.expm1(log_quantile)
