# Streaming Quantile Estimation for Financial Data

This repository contains a research project on streaming quantile estimation algorithms, with a focus on financial data. It includes implementations of several established algorithms, as well as two novel algorithms developed as part of this research: the Logarithmic-Biased KLL (LB-KLL) and the Hybrid-Query Sketch (HQS).

## Algorithms Implemented

*   **Greenwald-Khanna (GK):** A deterministic algorithm that provides guarantees on the precision of quantile estimates.
*   **KLL Sketch:** A popular randomized algorithm known for its speed and low memory usage.
*   **T-Digest:** A randomized algorithm that provides high accuracy, especially at the tails of the distribution.
*   **LB-KLL (Ours):** A novel algorithm that uses a logarithmic transformation to improve the accuracy of the KLL sketch for financial data.
*   **HQS (Ours):** A novel hybrid algorithm that combines the KLL sketch and the t-digest to provide both speed and accuracy.

## Getting Started

### Prerequisites

*   Conda
*   Python 3.9

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/vinhqdang/estimate_quantile.git
    cd estimate_quantile
    ```
2.  Create and activate the Conda environment:
    ```bash
    conda create -n quantile-estimation python=3.9 -y
    conda activate quantile-estimation
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Benchmark

To run the benchmark and reproduce the results in the report, run the following command:

```bash
python benchmarks/benchmark.py
```

This will download the required financial data, run the benchmark, and save the results to `benchmarks/results.json`.

### Visualizing the Results

To generate the plots from the benchmark results, run the following command:

```bash
python benchmarks/visualize.py
```

This will create the following files in the `benchmarks` directory:
*   `insertion_time.png`
*   `memory_usage.png`
*   `relative_error.png`

## Final Report

The full details of our research, including the mathematical analysis of the algorithms, the benchmark results, and our conclusions, can be found in the [Final_Report.md](Final_Report.md) file.
