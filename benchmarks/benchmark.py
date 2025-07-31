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
from lb_kll import LBKLL
from hqs import HQS

def run_benchmark_on_data(data, dataset_name):
    print(f"\n--- Benchmarking on {dataset_name} data ---")
    
    algorithms = {
        "Greenwald-Khanna": StreamingQuantile(epsilon=0.01),
        "KLL Sketch": KLL(k=200),
        "T-Digest": PyTDigest(),
        "LB-KLL (Ours)": LBKLL(k=200),
        "HQS (Ours)": HQS(k=200)
    }
    
    results = {}

    for name, algorithm in algorithms.items():
        print(f"\n--- {name} ---")
        
        # Measure insertion time
        start_time = time.time()
        if name == "T-Digest" or name == "HQS (Ours)":
            for d in data:
                algorithm.tdigest.update(d) if name == "HQS (Ours)" else algorithm.update(d)
        else:
            for d in data:
                algorithm.insert(d)
        end_time = time.time()
        insertion_time = end_time - start_time
        
        # Measure memory usage
        mem_usage = memory_usage((lambda: algorithm, ()), interval=0.1, timeout=1)
        
        # Measure query time
        query_quantiles = [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
        start_time = time.time()
        for q in query_quantiles:
            if name == "T-Digest" or name == "HQS (Ours)":
                 algorithm.tdigest.percentile(q * 100) if name == "HQS (Ours)" else algorithm.percentile(q * 100)
            else:
                algorithm.query(q)
        end_time = time.time()
        query_time = end_time - start_time

        # Calculate accuracy
        sorted_data = sorted(data)
        errors = {}
        for q in query_quantiles:
            true_quantile = np.quantile(sorted_data, q)
            if name == "T-Digest" or name == "HQS (Ours)":
                estimated_quantile = algorithm.tdigest.percentile(q * 100) if name == "HQS (Ours)" else algorithm.percentile(q * 100)
            else:
                estimated_quantile = algorithm.query(q)
            
            if true_quantile > 0:
                error = abs(estimated_quantile - true_quantile) / true_quantile
            else:
                error = 0
            errors[q] = error

        results[name] = {
            "Insertion Time (s)": insertion_time,
            "Memory Usage (MiB)": max(mem_usage),
            "Query Time (s)": query_time,
            "Errors": errors
        }
        
        print(f"Insertion Time: {insertion_time:.4f}s")
        print(f"Memory Usage: {max(mem_usage):.2f} MiB")
        print(f"Query Time: {query_time:.4f}s")
        for q, error in errors.items():
            print(f"p{int(q*100)} Error: {error:.4f}")

    return results

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
