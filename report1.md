# Performance Report: Streaming Quantile Algorithms

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report details the performance of two streaming quantile estimation algorithms: the Greenwald-Khanna (GK) algorithm and the KLL (Karnin, Lang, and Liberty) sketch. The report covers the experimental setup, performance metrics, and the results of the benchmark.

## 2. Algorithms

### 2.1. Greenwald-Khanna (GK)

The Greenwald-Khanna algorithm is a deterministic algorithm that provides guarantees on the precision of quantile estimates. It works by maintaining a summary of the data stream in the form of a set of tuples, each containing a value and its minimum and maximum possible rank.

*Reference: Greenwald, M., & Khanna, S. (2001). Space-efficient online computation of quantile summaries. In Proceedings of the 2001 ACM SIGMOD international conference on Management of data (pp. 58-66).*

### 2.2. KLL Sketch

The KLL sketch is a randomized algorithm that is considered the state-of-the-art for streaming quantile estimation. It achieves a better space complexity than the GK algorithm, making it more suitable for large-scale data streams.

*Reference: Karnin, Z., Lang, K., & Liberty, E. (2016). Optimal quantile approximation in streams. In 2016 IEEE 57th Annual Symposium on Foundations of Computer Science (FOCS) (pp. 71-78).*

## 3. Experimental Setup

The benchmark was performed on a machine with the following specifications:

*   **CPU:** TBD
*   **Memory:** TBD
*   **OS:** TBD

The benchmark was implemented in Python 3.9 and used the following libraries:

*   `memory-profiler`

The benchmark consists of the following steps:
1.  A stream of 1,000,000 random integers is generated.
2.  The stream is processed by both the GK and KLL algorithms.
3.  The following metrics are collected:
    *   Time to insert all items.
    *   Memory usage of the sketch.
    *   Time to query 10 different quantiles (0.1, 0.2, ..., 0.9, 0.99).
    *   Accuracy of the quantile estimates compared to the true quantiles.

## 4. Results

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 7.3452 | 89.18 | 0.0003 | 0.0064 | 0.0102 |
| KLL | 0.5389 | 89.80 | 0.0899 | 0.0127 | 0.0001 |

## 5. Conclusion

The KLL sketch significantly outperforms the Greenwald-Khanna algorithm in terms of insertion time, being over 13 times faster. Both algorithms have similar memory usage. The Greenwald-Khanna algorithm is faster for queries, but the KLL sketch provides better accuracy for the 99th percentile. For general-purpose streaming quantile estimation, the KLL sketch appears to be the superior choice due to its much faster insertion time and better accuracy at the tails of the distribution.
