import time
import sys
import json
import numpy as np
import yfinance as yf
from datetime import datetime

# Add the src directory to the Python path
sys.path.append('src')

from streaming_quantile import StreamingQuantile
from kll_sketch import KLL
from river.stats import Quantile
from lb_kll import LBKLL
from hqs import HQS
from qr_sketch import QRSketch

def run_convergence_benchmark(data, dataset_name):
    print(f"\n--- Convergence Benchmark on {dataset_name} data ---")
    
    # Calculate the single true median for the entire dataset
    true_median = np.median(sorted(data))
    print(f"True Median for the entire dataset: {true_median:.4f}")

    algorithms = {
        "Greenwald-Khanna": StreamingQuantile(epsilon=0.01),
        "KLL Sketch": KLL(k=200),
        "River Quantile": Quantile(),
        "LB-KLL (Ours)": LBKLL(k=200),
        "HQS (Ours)": HQS(k=200),
        "QRSketch (Ours)": QRSketch(q=0.5)
    }
    
    results = {}

    for name, algorithm in algorithms.items():
        print(f"\n--- {name} ---")
        
        daily_errors = []
        
        # Process the stream day by day
        for i, d in enumerate(data):
            # Insert the new data point
            if name == "River Quantile":
                algorithm.update(d)
            elif name == "HQS (Ours)":
                algorithm.insert(d)
            elif name == "QRSketch (Ours)":
                algorithm.add(d)
            else:
                algorithm.insert(d)

            # Query the current estimated median
            if name == "River Quantile":
                estimated_median = algorithm.get()
            elif name == "HQS (Ours)":
                estimated_median = algorithm.query(0.5)
            elif name == "QRSketch (Ours)":
                estimated_median = algorithm.quantile()
            else:
                estimated_median = algorithm.query(0.5)

            # Calculate and store the error for the current day
            if estimated_median is not None and true_median > 0:
                error = abs(estimated_median - true_median) / true_median
                daily_errors.append(error)

        # Calculate the average error over the lifetime of the stream
        average_error = np.mean(daily_errors) if daily_errors else 0
        results[name] = {"Average Lifetime Error": average_error}
        print(f"Average Lifetime Error (vs Final True Median): {average_error:.4f}")

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
    
    benchmark_results = run_convergence_benchmark(stock_data, "20 Stocks")
    
    with open('benchmarks/convergence_results.json', 'w') as f:
        json.dump(benchmark_results, f, indent=4)
        
    print("\nConvergence benchmark results saved to benchmarks/convergence_results.json")