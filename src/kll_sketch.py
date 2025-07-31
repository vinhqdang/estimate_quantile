import math
import random

class KLL:
    def __init__(self, k, c=2/3.0):
        self.k = k
        self.c = c
        self.compactors = []
        self.H = 0
        self.size = 0

    def insert(self, item):
        if len(self.compactors) == 0:
            self.compactors.append([])
        
        self.compactors[0].append(item)
        self.size += 1
        
        if len(self.compactors[0]) >= self.k:
            self.compress()

    def query(self, quantile):
        if self.size == 0:
            return None

        all_items = []
        for h in range(len(self.compactors)):
            weight = 2**h
            for item in self.compactors[h]:
                all_items.extend([item] * weight)
        
        all_items.sort()
        
        rank = int(quantile * self.size)
        if rank >= len(all_items):
            rank = len(all_items) -1

        return all_items[rank]

    def compress(self):
        for h in range(len(self.compactors)):
            if len(self.compactors[h]) >= self.k:
                # Sort and compact the current level
                self.compactors[h].sort()
                
                # Decide whether to keep odd or even elements
                if random.random() < 0.5:
                    # Keep even elements
                    new_compactor = self.compactors[h][::2]
                else:
                    # Keep odd elements
                    new_compactor = self.compactors[h][1::2]

                # Add the compacted elements to the next level
                if h + 1 >= len(self.compactors):
                    self.compactors.append([])
                
                self.compactors[h+1].extend(new_compactor)
                self.compactors[h] = [] # Clear the current level
