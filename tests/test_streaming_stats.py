import unittest
from src.streaming_stats import StreamingStats

class TestStreamingStats(unittest.TestCase):
    def test_mean_variance_stddev(self):
        stats = StreamingStats()
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        for x in data:
            stats.insert(x)

        self.assertAlmostEqual(stats.get_mean(), 5.0)
        self.assertAlmostEqual(stats.get_variance(), 4.0)
        self.assertAlmostEqual(stats.get_stddev(), 2.0)

if __name__ == '__main__':
    unittest.main()
