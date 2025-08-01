
import unittest
import numpy as np
from src.qr_sketch import QRSketch

class TestQRSketch(unittest.TestCase):

    def test_initialization(self):
        sketch = QRSketch(q=0.5, batch_size=10)
        self.assertEqual(sketch.q, 0.5)
        self.assertEqual(sketch.batch_size, 10)
        self.assertEqual(len(sketch.buffer), 0)

    def test_add_data(self):
        sketch = QRSketch(q=0.5, batch_size=10)
        sketch.add(5)
        self.assertEqual(len(sketch.buffer), 1)
        self.assertEqual(sketch.buffer[0], 5)

    def test_training_trigger(self):
        sketch = QRSketch(q=0.5, batch_size=5)
        for i in range(10):
            sketch.add(i)
        
        self.assertEqual(len(sketch.buffer), 0)
        self.assertIsNotNone(sketch.model)

    def test_quantile_estimation(self):
        sketch = QRSketch(q=0.5, batch_size=100)
        np.random.seed(42)
        data = np.random.normal(100, 10, 1000)
        for x in data:
            sketch.add(x)

        estimated_quantile = sketch.quantile()
        self.assertIsNotNone(estimated_quantile)
        
        true_median = np.median(data)
        self.assertAlmostEqual(estimated_quantile, true_median, delta=1)

    def test_quantile_estimation_uniform(self):
        sketch = QRSketch(q=0.25, batch_size=100)
        np.random.seed(42)
        data = np.random.uniform(0, 100, 1000)
        for x in data:
            sketch.add(x)

        estimated_quantile = sketch.quantile()
        self.assertIsNotNone(estimated_quantile)
        
        true_quantile = np.percentile(data, 25)
        self.assertAlmostEqual(estimated_quantile, true_quantile, delta=1)

if __name__ == '__main__':
    unittest.main()
