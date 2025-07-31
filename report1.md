# Performance Report: Streaming Quantile Algorithms

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report details the performance of three streaming quantile estimation algorithms: the Greenwald-Khanna (GK) algorithm, the KLL (Karnin, Lang, and Liberty) sketch, and the t-digest. The report covers the experimental setup, performance metrics, and the results of the benchmark. The benchmark was performed on three datasets: a synthetic dataset of 1,000,000 random integers, a real-world dataset of 20 years of S&P 500 closing prices, and 20 years of daily average temperature data for New York City.

## 2. Algorithms

### 2.1. Greenwald-Khanna (GK)

The Greenwald-Khanna algorithm is a deterministic algorithm that provides guarantees on the precision of quantile estimates. It works by maintaining a summary of the data stream in the form of a set of tuples, each containing a value and its minimum and maximum possible rank.

*Reference: Greenwald, M., & Khanna, S. (2001). Space-efficient online computation of quantile summaries. In Proceedings of the 2001 ACM SIGMOD international conference on Management of data (pp. 58-66).*

### 2.2. KLL Sketch

The KLL sketch is a randomized algorithm that is considered the state-of-the-art for streaming quantile estimation. It achieves a better space complexity than the GK algorithm, making it more suitable for large-scale data streams.

*Reference: Karnin, Z., Lang, K., & Liberty, E. (2016). Optimal quantile approximation in streams. In 2016 IEEE 57th Annual Symposium on Foundations of Computer Science (FOCS) (pp. 71-78).*

### 2.3. T-Digest

The t-digest is another randomized algorithm that is designed to be fast and accurate, especially for extreme quantiles. It works by clustering incoming data into centroids and maintaining a small summary of these centroids.

*Reference: Dunning, T., & Ertl, O. (2019). Computing extremely accurate quantiles using t-digests. arXiv preprint arXiv:1902.04023.*

## 3. Experimental Setup

The benchmark was performed on a machine with the following specifications:

*   **CPU:** TBD
*   **Memory:** TBD
*   **OS:** TBD

The benchmark was implemented in Python 3.9 and used the following libraries:

*   `memory-profiler`
*   `tdigest`
*   `yfinance`
*   `meteostat`

The benchmark consists of the following steps:
1.  Three datasets are used:
    *   A stream of 1,000,000 random integers.
    *   A stream of 20 years of S&P 500 closing prices.
    *   A stream of 20 years of daily average temperature data for New York City.
2.  The stream is processed by the GK, KLL, and t-digest algorithms.
3.  The following metrics are collected:
    *   Time to insert all items.
    *   Memory usage of the sketch.
    *   Time to query 10 different quantiles (0.1, 0.2, ..., 0.9, 0.99).
    *   Accuracy of the quantile estimates compared to the true quantiles.

## 4. Results

### 4.1. Random Data (1,000,000 integers)

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 7.5562 | 89.59 | 0.0003 | 0.0008 | 0.0101 |
| KLL | 0.4967 | 89.98 | 0.1074 | 0.0109 | 0.0000 |
| T-Digest | 17.4405 | 106.38 | 0.0084 | 0.0000 | 0.0000 |

### 4.2. S&P 500 Data (20 years)

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 0.0846 | 113.37 | 0.0003 | 0.0125 | 0.0107 |
| KLL | 0.0017 | 113.49 | 0.0009 | 0.0024 | 0.0009 |
| T-Digest | 0.2383 | 114.24 | 0.0063 | 0.0004 | 0.0006 |

### 4.3. JFK Airport Temperature Data (20 years)

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 0.0491 | 128.74 | 0.0002 | 0.0231 | 0.0070 |
| KLL | 0.0021 | 128.74 | 0.0016 | 0.0077 | 0.0000 |
| T-Digest | 0.0726 | 128.74 | 0.0040 | 0.0005 | 0.0005 |

## 5. Conclusion

The results are consistent across all three datasets. The KLL sketch is the fastest algorithm for insertions, while the t-digest is the most accurate. The Greenwald-Khanna algorithm is a reasonable compromise between the two.

The choice of algorithm depends on the specific application. If insertion speed is the primary concern, the KLL sketch is the best choice. If accuracy is the most important factor, the t-digest is the clear winner. For a good balance of performance and accuracy, the Greenwald-Khanna algorithm is a viable option.