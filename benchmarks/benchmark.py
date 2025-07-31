import time
import random
import sys
from memory_profiler import memory_usage
import numpy as np

# Add the src directory to the Python path
sys.path.append('src')

from streaming_quantile import StreamingQuantile
from kll_sketch import KLL

def run_benchmark():
    # Experimental parameters
    n = 1000000
    quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    
    # Generate random data
    data = [random.randint(0, 100000) for _ in range(n)]
    
    # --- Greenwald-Khanna ---
    print("--- Greenwald-Khanna ---")
    gk = StreamingQuantile(epsilon=0.01)
    
    # Measure insertion time
    start_time = time.time()
    for d in data:
        gk.insert(d)
    end_time = time.time()
    
    # Measure memory usage
    mem_usage = memory_usage((lambda: gk, ()))

    print(f"Insertion Time: {end_time - start_time:.4f}s")
    print(f"Memory Usage: {mem_usage[0]:.2f} MiB")
    
    # Measure query time and accuracy
    start_time = time.time()
    for q in quantiles:
        gk.query(q)
    end_time = time.time()
    
    print(f"Query Time: {end_time - start_time:.4f}s")
    
    # Calculate accuracy
    data.sort()
    for q in [0.5, 0.99]:
        true_quantile = np.quantile(data, q)
        estimated_quantile = gk.query(q)
        error = abs(estimated_quantile - true_quantile) / true_quantile
        print(f"p{int(q*100)} Error: {error:.4f}")

    # --- KLL Sketch ---
    print("\n--- KLL Sketch ---")
    kll = KLL(k=200)
    
    # Measure insertion time
    start_time = time.time()
    for d in data:
        kll.insert(d)
    end_time = time.time()

    # Measure memory usage
    mem_usage = memory_usage((lambda: kll, ()))
    
    print(f"Insertion Time: {end_time - start_time:.4f}s")
    print(f"Memory Usage: {mem_usage[0]:.2f} MiB")
    
    # Measure query time and accuracy
    start_time = time.time()
    for q in quantiles:
        kll.query(q)
    end_time = time.time()
    
    print(f"Query Time: {end_time - start_time:.4f}s")
    
    # Calculate accuracy
    for q in [0.5, 0.99]:
        true_quantile = np.quantile(data, q)
        estimated_quantile = kll.query(q)
        error = abs(estimated_quantile - true_quantile) / true_quantile
        print(f"p{int(q*100)} Error: {error:.4f}")

if __name__ == '__main__':
    run_benchmark()
