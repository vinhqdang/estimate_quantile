# Performance Report: Streaming Quantile Algorithms

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report details the performance of three streaming quantile estimation algorithms: the Greenwald-Khanna (GK) algorithm, the KLL (Karnin, Lang, and Liberty) sketch, and the t-digest. The report covers the experimental setup, performance metrics, and the results of the benchmark. The benchmark was performed on a real-world dataset of 20 years of closing prices for 20 different stocks.

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

The benchmark consists of the following steps:
1.  A stream of 20 years of closing prices for 20 stocks is downloaded.
2.  The stream is processed by the GK, KLL, and t-digest algorithms.
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

## 5. Conclusion & Next Steps

The benchmark results on the consolidated financial dataset show a clear trade-off between insertion speed and accuracy. The KLL sketch is by far the fastest, but the t-digest provides the highest accuracy, especially for the 99th percentile.

Our initial attempt at a hybrid algorithm (HRS) was unsuccessful, indicating that a more sophisticated approach is required. The project is now focused on researching a new model. The next step is to conduct a deeper review of recent literature to find a more promising architecture for a novel streaming quantile estimation algorithm.