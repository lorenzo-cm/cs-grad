import csv

from optimal_granularity.optimizer import OptimizeReturn


def save_results_to_csv(result: OptimizeReturn, filename: str) -> None:
    """Save optimization results to CSV using attribute access only."""
    tradeoff_values = result.tradeoff_values

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scale', 'Uniformity', 'Robustness', 'Tradeoff'])
        for scale in sorted(tradeoff_values.keys(), key=lambda s: float(s)):
            values = tradeoff_values[scale]
            writer.writerow([scale, values.uniformity, values.robustness, values.tradeoff])
