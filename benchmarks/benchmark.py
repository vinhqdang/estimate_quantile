import time
import sys
from memory_profiler import memory_usage
import numpy as np
import yfinance as yf
from meteostat import Point, Daily
from datetime import datetime

# Add the src directory to the Python path
sys.path.append('src')

from streaming_quantile import StreamingQuantile
from kll_sketch import KLL
from tdigest import TDigest as PyTDigest
from hrs import HRS

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

    # --- HRS ---
    print("\n--- HRS ---")
    hrs = HRS(k=200, reservoir_size=1000)
    
    # Measure insertion time
    start_time = time.time()
    for d in data:
        hrs.insert(d)
    end_time = time.time()

    # Measure memory usage
    mem_usage = memory_usage((lambda: hrs, ()))
    
    print(f"Insertion Time: {end_time - start_time:.4f}s")
    print(f"Memory Usage: {mem_usage[0]:.2f} MiB")
    
    # Measure query time and accuracy
    start_time = time.time()
    for q in quantiles:
        hrs.query(q)
    end_time = time.time()
    
    print(f"Query Time: {end_time - start_time:.4f}s")
    
    # Calculate accuracy
    data.sort()
    for q in [0.5, 0.99]:
        true_quantile = np.quantile(data, q)
        estimated_quantile = hrs.query(q)
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

    # Get weather data
    print("\nDownloading weather data...")
    cities = {
        "New York": (40.7128, -74.0060), "London": (51.5074, -0.1278), "Tokyo": (35.6895, 139.6917), "Sydney": (-33.8688, 151.2093), "Cairo": (30.0444, 31.2357),
        "Moscow": (55.7558, 37.6173), "Rio de Janeiro": (-22.9068, -43.1729), "Beijing": (39.9042, 116.4074), "Johannesburg": (-26.2041, 28.0473), "Mumbai": (19.0760, 72.8777),
        "Mexico City": (19.4326, -99.1332), "Buenos Aires": (-34.6037, -58.3816), "Lagos": (6.5244, 3.3792), "Istanbul": (41.0082, 28.9784), "Karachi": (24.8607, 67.0011),
        "Shanghai": (31.2304, 121.4737), "Sao Paulo": (-23.5505, -46.6333), "Seoul": (37.5665, 126.9780), "Jakarta": (-6.2088, 106.8456), "Delhi": (28.7041, 77.1025)
    }
    weather_data = []
    start = datetime(2005, 1, 1)
    end = datetime(2025, 1, 1)
    for city, coords in cities.items():
        print(f"Downloading weather data for {city}...")
        point = Point(coords[0], coords[1])
        df = Daily(point, start, end).fetch()
        weather_data.extend(df['tavg'].dropna().tolist())
        time.sleep(1) # Add a delay to avoid throttling
    print(f"Downloaded {len(weather_data)} data points.")
    run_benchmark_on_data(weather_data, "20 Cities")
