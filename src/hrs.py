import numpy as np
from kll_sketch import KLL
from reservoir_sampler import ReservoirSampler

class HRS:
    def __init__(self, k, reservoir_size):
        self.kll = KLL(k)
        self.reservoir = ReservoirSampler(reservoir_size)

    def insert(self, item):
        self.kll.insert(item)
        self.reservoir.add(item)

    def query(self, quantile, range_factor=0.2):
        # Step 1: Get an approximate range from the KLL sketch
        q_low = max(0, quantile - range_factor)
        q_high = min(1, quantile + range_factor)
        
        v_low = self.kll.query(q_low)
        v_high = self.kll.query(q_high)

        if v_low is None or v_high is None:
            return self.kll.query(quantile)

        # Step 2: Filter the true samples from the reservoir
        refined_samples = [s for s in self.reservoir.samples if v_low <= s <= v_high]

        # Step 3: Calculate the refined estimate
        if not refined_samples:
            # If no samples in the range, fall back to the KLL estimate
            return self.kll.query(quantile)

        refined_samples.sort()
        
        # Return the sample at the requested quantile
        if len(refined_samples) < 2:
            return self.kll.query(quantile)
        
        return refined_samples[int(len(refined_samples) * quantile)]
