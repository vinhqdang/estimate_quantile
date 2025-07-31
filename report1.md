# Performance Report: Streaming Quantile Algorithms

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report details the performance of four streaming quantile estimation algorithms: the Greenwald-Khanna (GK) algorithm, the KLL (Karnin, Lang, and Liberty) sketch, the t-digest, and our own Hybrid Reservoir-Sketch (HRS) algorithm. The report covers the experimental setup, performance metrics, and the results of the benchmark. The benchmark was performed on two real-world datasets: 20 years of closing prices for 20 stocks and 20 years of daily average temperature data for 20 cities.

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

### 2.4. Hybrid Reservoir-Sketch (HRS)

The HRS algorithm is a new hybrid model that we developed. It combines a KLL sketch with a reservoir sampler. The KLL sketch is used to get an approximate range for a given quantile, and then the reservoir sampler is used to refine the estimate using a small sample of true data points.

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
1.  Two datasets are used:
    *   A stream of 20 years of closing prices for 20 stocks.
    *   A stream of 20 years of daily average temperature data for 20 cities.
2.  The stream is processed by the GK, KLL, t-digest, and HRS algorithms.
3.  The following metrics are collected:
    *   Time to insert all items.
    *   Memory usage of the sketch.
    *   Time to query 10 different quantiles (0.1, 0.2, ..., 0.9, 0.99).
    *   Accuracy of the quantile estimates compared to the true quantiles.

## 4. Results

### 4.1. 20 Stocks Data

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 1.3550 | 167.03 | 0.0004 | 0.0170 | 0.1371 |
| KLL | 0.0346 | 167.88 | 0.0105 | 0.0023 | 0.0006 |
| T-Digest | 3.2549 | 167.88 | 0.0066 | 0.0001 | 0.0001 |
| HRS | 0.1281 | 167.88 | 0.0177 | 0.0088 | 0.1794 |

### 4.2. 20 Cities Temperature Data

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 1.1431 | 175.41 | 0.0003 | 0.0098 | 0.0366 |
| KLL | 0.0490 | 176.29 | 0.0103 | 0.0049 | 0.0000 |
| T-Digest | 1.5590 | 176.29 | 0.0066 | 0.0023 | 0.0001 |
| HRS | 0.2097 | 176.29 | 0.0246 | 0.0098 | 0.1128 |

## 5. Conclusion

Our attempt to create a new hybrid algorithm, HRS, was not successful in its current form. While the insertion time was competitive, the accuracy, especially at the 99th percentile, was significantly worse than the other algorithms. This is likely due to the simple refinement strategy we employed. A more sophisticated approach to combining the sketch and the reservoir is needed to improve the accuracy.

Of the existing algorithms, the KLL sketch and the t-digest are the top performers. The KLL sketch is the fastest for insertions, while the t-digest is the most accurate. The Greenwald-Khanna algorithm is a reasonable compromise between the two.

The choice of algorithm depends on the specific application. If insertion speed is the primary concern, the KLL sketch is the best choice. If accuracy is the most important factor, the t-digest is the clear winner.
