import math

class StreamingStats:
    def __init__(self):
        self.n = 0
        self.mean = 0
        self.m2 = 0

    def insert(self, x):
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        delta2 = x - self.mean
        self.m2 += delta * delta2

    def get_mean(self):
        return self.mean

    def get_variance(self):
        if self.n < 2:
            return 0
        return self.m2 / self.n

    def get_stddev(self):
        return math.sqrt(self.get_variance())
