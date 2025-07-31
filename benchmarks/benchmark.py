import time
import sys
from memory_profiler import memory_usage
import numpy as np
import yfinance as yf
from datetime import datetime

# Add the src directory to the Python path
sys.path.append('src')

from streaming_quantile import StreamingQuantile
from kll_sketch import KLL
from tdigest import TDigest as PyTDigest

def run_benchmark_on_data(data, dataset_name):
    print(f"\n--- Benchmarking on {dataset_name} data ---")
    quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]

    # --- Greenwald-Khanna ---
    print("\n--- Greenwald-Khanna ---")
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
        print(f"p{int(q*100)} Error: {float(error):.4f}")

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
    data.sort()
    for q in [0.5, 0.99]:
        true_quantile = np.quantile(data, q)
        estimated_quantile = kll.query(q)
        error = abs(estimated_quantile - true_quantile) / true_quantile
        print(f"p{int(q*100)} Error: {float(error):.4f}")

    # --- T-Digest ---
    print("\n--- T-Digest ---")
    td = PyTDigest()
    
    # Measure insertion time
    start_time = time.time()
    for d in data:
        td.update(d)
    end_time = time.time()

    # Measure memory usage
    mem_usage = memory_usage((lambda: td, ()))
    
    print(f"Insertion Time: {end_time - start_time:.4f}s")
    print(f"Memory Usage: {mem_usage[0]:.2f} MiB")
    
    # Measure query time and accuracy
    start_time = time.time()
    for q in quantiles:
        td.percentile(q * 100)
    end_time = time.time()
    
    print(f"Query Time: {end_time - start_time:.4f}s")
    
    # Calculate accuracy
    data.sort()
    for q in [0.5, 0.99]:
        true_quantile = np.quantile(data, q)
        estimated_quantile = td.percentile(q * 100)
        error = abs(estimated_quantile - true_quantile) / true_quantile
        print(f"p{int(q*100)} Error: {float(error):.4f}")

if __name__ == '__main__':
    # Get stock data
    print("Downloading stock data...")
    tickers = ["AAPL", "GOOG", "MSFT", "AMZN", "META", "TSLA", "NVDA", "JPM", "JNJ", "V", "PG", "UNH", "HD", "MA", "BAC", "DIS", "PFE", "XOM", "CSCO", "CVX"]
    stock_data = []
    for ticker in tickers:
        print(f"Downloading {ticker}...")
        stock_data.extend(yf.download(ticker, start='2005-01-01', end='2025-01-01')['Close'].values.tolist())
    
    stock_data = [item for sublist in stock_data for item in sublist if not np.isnan(item)]
    print(f"Downloaded {len(stock_data)} data points.")
    run_benchmark_on_data(stock_data, "20 Stocks")