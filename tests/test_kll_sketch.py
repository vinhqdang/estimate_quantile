import unittest
import random
from src.kll_sketch import KLL

class TestKLL(unittest.TestCase):
    def test_empty_sketch(self):
        kll = KLL(k=10)
        self.assertIsNone(kll.query(0.5))

    def test_single_item_sketch(self):
        kll = KLL(k=10)
        kll.insert(42)
        self.assertEqual(kll.query(0.5), 42)

    def test_median_of_a_stream(self):
        kll = KLL(k=20)
        for i in range(1, 1001):
            kll.insert(i)

        median = kll.query(0.5)
        self.assertIsNotNone(median)
        # The error is proportional to k, so we expect a reasonable approximation
        self.assertGreaterEqual(median, 450)
        self.assertLessEqual(median, 550)

if __name__ == '__main__':
    unittest.main()

