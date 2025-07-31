# Performance Report: Streaming Quantile Algorithms

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report details the performance of three streaming quantile estimation algorithms: the Greenwald-Khanna (GK) algorithm, the KLL (Karnin, Lang, and Liberty) sketch, and the t-digest. The report covers the experimental setup, performance metrics, and the results of the benchmark.

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

The benchmark consists of the following steps:
1.  A stream of 1,000,000 random integers is generated.
2.  The stream is processed by the GK, KLL, and t-digest algorithms.
3.  The following metrics are collected:
    *   Time to insert all items.
    *   Memory usage of the sketch.
    *   Time to query 10 different quantiles (0.1, 0.2, ..., 0.9, 0.99).
    *   Accuracy of the quantile estimates compared to the true quantiles.

## 4. Results

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p50 Error | p99 Error |
|---|---|---|---|---|---|
| Greenwald-Khanna | 7.5562 | 89.59 | 0.0003 | 0.0008 | 0.0101 |
| KLL | 0.4967 | 89.98 | 0.1074 | 0.0109 | 0.0000 |
| T-Digest | 17.4405 | 106.38 | 0.0084 | 0.0000 | 0.0000 |

## 5. Conclusion

The KLL sketch is the fastest algorithm for insertions, being significantly faster than both Greenwald-Khanna and t-digest. The t-digest has the highest insertion time, but it provides the best accuracy, with zero error for both the median and the 99th percentile in this benchmark. The Greenwald-Khanna algorithm is a good middle ground, with reasonable insertion time and accuracy.

For applications where insertion speed is critical, the KLL sketch is the best choice. For applications where accuracy is paramount, the t-digest is the clear winner, despite its slower insertion time.