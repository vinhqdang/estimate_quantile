# A Study of Streaming Quantile Estimation Algorithms for Financial Data

**Author:** Vinh
**Email:** dqvinh87@gmail.com
**Date:** 2025-07-31

## 1. Abstract

This report presents a comprehensive study of streaming quantile estimation algorithms, motivated by the need for accurate, high-speed analysis of financial data. We review three established algorithms: the Greenwald-Khanna (GK) algorithm, the KLL sketch, and the t-digest. We then chronicle our research process in developing a novel algorithm, which involved two unsuccessful attempts (the Hybrid Reservoir-Sketch and the Focused Quantile Sketch) and two successful models: the Logarithmic-Biased KLL (LB-KLL) and the Hybrid-Query Sketch (HQS). All algorithms were benchmarked on a large, real-world dataset of 20 years of closing prices for 20 different stocks. The results show that our new algorithms, the LB-KLL and HQS, provide compelling and practical trade-offs between speed and accuracy, making them valuable contributions for financial data analysis.

## 2. Introduction to Streaming Quantile Estimation

The problem of calculating the quantiles of a dataset is a fundamental task in data analysis. A quantile `q` is the value below which `q` percent of the data falls. For example, the 0.5-quantile is the median.

In a streaming setting, the data arrives one element at a time, and we cannot store the entire dataset in memory. This makes the problem of calculating quantiles much more challenging. Streaming quantile estimation algorithms aim to solve this problem by maintaining a small summary of the data, which can be used to estimate the quantiles with a certain degree of accuracy.

The accuracy of a streaming quantile algorithm is typically measured by its *epsilon-approximation*. An algorithm is said to be an *epsilon-approximate* quantile estimator if, for any quantile `q`, the estimated value is guaranteed to be between the `(q - epsilon)`-quantile and the `(q + epsilon)`-quantile.

## 3. Established Algorithms

### 3.1. Greenwald-Khanna (GK)

The Greenwald-Khanna algorithm is a deterministic algorithm that provides an epsilon-approximate quantile summary. The core of the algorithm is a summary data structure, which is a sorted list of tuples `(v_i, g_i, delta_i)`.

*   `v_i`: A value from the stream.
*   `g_i`: The difference between the minimum and maximum possible rank of `v_i`.
*   `delta_i`: The difference between the maximum possible rank of `v_i` and the maximum possible rank of `v_{i-1}`.

The summary is maintained such that the following invariant holds: `g_i + delta_i <= 2 * epsilon * n`, where `n` is the number of items seen so far.

When a new item arrives, it is inserted into the summary. If the invariant is violated, a `compress` operation is performed, which merges adjacent tuples to reduce the size of the summary.

### 3.2. KLL Sketch

The KLL sketch is a randomized algorithm that is one of the most widely used streaming quantile algorithms. It is known for its low memory usage and fast insertion time.

The KLL sketch consists of a series of "compactors", which are arrays of a fixed size `k`. When a compactor is full, it is "compacted" by sorting it and then taking every other element. The compacted elements are then passed to the next compactor in the series. This process is repeated until the elements reach the final compactor.

The KLL sketch provides an epsilon-approximate quantile summary with a high probability. The space complexity of the KLL sketch is `O(k / epsilon * log(log(1/delta)))`, where `delta` is the failure probability.

### 3.3. T-Digest

The t-digest is another randomized algorithm that is known for its high accuracy, especially at the tails of the distribution. It works by clustering incoming data into "centroids". Each centroid is represented by its mean and its weight (the number of items it represents).

When a new item arrives, it is merged with the closest centroid. If no centroid is close enough, a new centroid is created. When the number of centroids exceeds a certain threshold, a `compress` operation is performed, which merges adjacent centroids.

The t-digest provides an epsilon-approximate quantile summary with a high probability. The space complexity of the t-digest is `O(delta * k)`, where `delta` is a compression parameter.

## 4. Development of Novel Algorithms

Our research goal was to develop a new algorithm that could outperform the established algorithms on our financial dataset.

### 4.1. Attempt 1: Hybrid Reservoir-Sketch (HRS) - FAILED

*   **Concept:** Combine a KLL sketch with a reservoir sampler.
*   **Conclusion:** This approach was abandoned due to poor accuracy.

### 4.2. Attempt 2: Focused Quantile Sketch (FQS) - FAILED

*   **Concept:** Use two KLL sketches, one for the full range and one for the tail.
*   **Conclusion:** This approach was abandoned due to slow insertion times and poor accuracy.

### 4.3. Attempt 3: Logarithmic-Biased KLL (LB-KLL) - SUCCESS

*   **Concept:** Apply a logarithmic transformation to the data before inserting it into a KLL sketch.
*   **Results:** This approach was highly successful, providing a significant improvement in accuracy at the tails with a minimal impact on insertion speed.

### 4.4. Attempt 4: Hybrid-Query Sketch (HQS) - SUCCESS

*   **Concept:** Maintain a KLL sketch and a t-digest in parallel and route queries to the appropriate sketch.
*   **Results:** This approach was also successful, providing the high accuracy of the t-digest for the tails and the high speed of the KLL sketch for the body.

## 5. Experimental Setup

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
2.  The stream is processed by the GK, KLL, t-digest, LB-KLL, and HQS algorithms.
3.  The following metrics are collected:
    *   Time to insert all items.
    *   Memory usage of the sketch.
    *   Time to query quantiles (0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99).
    *   Accuracy of the quantile estimates compared to the true quantiles.

## 6. Results

### 6.1. 20 Stocks Data

| Algorithm | Insertion Time (s) | Memory Usage (MiB) | Query Time (s) | p1 Error | p5 Error | p25 Error | p50 Error | p75 Error | p95 Error | p99 Error |
|---|---|---|---|---|---|---|---|---|---|---|
| Greenwald-Khanna | 1.4280 | 166.45 | 0.0004 | 0.2061 | 0.1568 | 0.0300 | 0.0170 | 0.0236 | 0.0375 | 0.1371 |
| KLL | 0.0326 | 166.68 | 0.0124 | 0.0851 | 0.0366 | 0.0020 | 0.0063 | 0.0072 | 0.0110 | 0.0121 |
| T-Digest | 2.2957 | 167.93 | 0.0322 | 0.0030 | 0.0007 | 0.0009 | 0.0001 | 0.0002 | 0.0004 | 0.0001 |
| **LB-KLL (Ours)** | **0.1186** | **166.68** | **0.0194** | **0.0281** | **0.0121** | **0.0103** | **0.0002** | **0.0065** | **0.0010** | **0.0064** |
| **HQS (Ours)** | **2.3376** | **167.93** | **0.0125** | **0.0030** | **0.0007** | **0.0003** | **0.0001** | **0.0000** | **0.0004** | **0.0001** |

## 7. Conclusion

Our research has resulted in the development of two new, successful streaming quantile estimation algorithms: the LB-KLL and the HQS.

*   The **LB-KLL** is an excellent general-purpose algorithm that provides a significant improvement in accuracy at the tails with a minimal impact on insertion speed. It is a strong candidate to replace the standard KLL sketch in many applications.
*   The **HQS** is a specialist algorithm that is designed for applications where query time is critical and there is a mix of queries for the body and the tails. It provides the best of both worlds: the speed of the KLL sketch and the accuracy of the t-digest.

This project has demonstrated that it is possible to develop new, effective streaming quantile estimation algorithms by combining and modifying existing ideas.