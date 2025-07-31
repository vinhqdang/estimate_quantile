import unittest
import random
from src.streaming_quantile import StreamingQuantile

class TestStreamingQuantile(unittest.TestCase):
    def test_median_of_a_stream(self):
        sq = StreamingQuantile(epsilon=0.1)
        for i in range(1, 1001):
            sq.insert(i)

        median = sq.query(0.5)
        self.assertIsNotNone(median)
        # With epsilon = 0.1, the error should be at most 100
        self.assertGreaterEqual(median, 400)
        self.assertLessEqual(median, 620)

    def test_empty_stream(self):
        sq = StreamingQuantile()
        self.assertIsNone(sq.query(0.5))

    def test_single_element_stream(self):
        sq = StreamingQuantile()
        sq.insert(10)
        self.assertEqual(sq.query(0.5), 10)

    def test_two_element_stream(self):
        sq = StreamingQuantile()
        sq.insert(10)
        sq.insert(20)
        self.assertEqual(sq.query(0.5), 10)
        self.assertEqual(sq.query(0.9), 20)


if __name__ == '__main__':
    unittest.main()

