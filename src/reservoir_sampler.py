import random

class ReservoirSampler:
    def __init__(self, size):
        self.size = size
        self.samples = []
        self.n = 0

    def add(self, item):
        self.n += 1
        if len(self.samples) < self.size:
            self.samples.append(item)
        else:
            r = random.randint(0, self.n - 1)
            if r < self.size:
                self.samples[r] = item
