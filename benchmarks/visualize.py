import json
import matplotlib.pyplot as plt
import numpy as np

def plot_results():
    with open('benchmarks/results.json', 'r') as f:
        results = json.load(f)

    algorithms = list(results.keys())
    
    # --- Plot Insertion Time ---
    insertion_times = [results[alg]['Insertion Time (s)'] for alg in algorithms]
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, insertion_times)
    plt.ylabel('Time (s)')
    plt.title('Insertion Time Comparison')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('benchmarks/insertion_time.png')
    
    # --- Plot Memory Usage ---
    memory_usages = [results[alg]['Memory Usage (MiB)'] for alg in algorithms]
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, memory_usages)
    plt.ylabel('Memory (MiB)')
    plt.title('Memory Usage Comparison')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('benchmarks/memory_usage.png')

    # --- Plot Relative Error ---
    quantiles = sorted([float(q) for q in results[algorithms[0]]['Errors'].keys()])
    plt.figure(figsize=(12, 8))
    for alg in algorithms:
        errors = [results[alg]['Errors'][str(q)] for q in quantiles]
        plt.plot(quantiles, errors, marker='o', linestyle='-', label=alg)
    
    plt.yscale('log')
    plt.xlabel('Quantile')
    plt.ylabel('Relative Error (log scale)')
    plt.title('Relative Error Across Quantiles')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.savefig('benchmarks/relative_error.png')
    
    print("Plots saved to benchmarks/insertion_time.png, benchmarks/memory_usage.png, and benchmarks/relative_error.png")

if __name__ == '__main__':
    plot_results()
