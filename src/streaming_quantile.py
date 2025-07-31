import math

class StreamingQuantile:
    """
    An implementation of the Greenwald-Khanna algorithm for streaming quantiles.
    """
    def __init__(self, epsilon=0.01):
        self.epsilon = epsilon
        self.n = 0
        self.summary = []

    def insert(self, v):
        self.n += 1
        if not self.summary:
            self.summary.append((v, 1, 0))
            return

        idx = 0
        while idx < len(self.summary) and self.summary[idx][0] < v:
            idx += 1

        if idx == 0 or idx == len(self.summary):
            delta = 0
        else:
            delta = math.floor(2 * self.epsilon * self.n)

        self.summary.insert(idx, (v, 1, delta))

        if self.n % int(1 / (2 * self.epsilon)) == 0:
            self.compress()

    def compress(self):
        if len(self.summary) < 2:
            return

        i = len(self.summary) - 2
        while i >= 0:
            v_i, g_i, delta_i = self.summary[i]
            v_i_plus_1, g_i_plus_1, delta_i_plus_1 = self.summary[i+1]

            if g_i + g_i_plus_1 + delta_i_plus_1 < 2 * self.epsilon * self.n:
                # Merge tuple i+1 into i
                new_v = v_i_plus_1
                new_g = g_i + g_i_plus_1
                new_delta = delta_i_plus_1
                
                self.summary[i] = (new_v, new_g, new_delta)
                self.summary.pop(i+1)

            i -= 1

    def query(self, quantile):
        if not self.summary:
            return None

        rank = math.ceil(quantile * self.n)
        rmin = 0
        
        for i in range(len(self.summary)):
            v_i, g_i, delta_i = self.summary[i]
            
            if rmin + g_i + delta_i >= rank:
                return v_i
            
            rmin += g_i
            
        return self.summary[-1][0]
