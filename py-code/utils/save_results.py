import csv

from optimal_granularity.optimizer import OptimizeReturn


def save_results_to_csv(result: OptimizeReturn, filename: str) -> None:
    """Save optimization results to CSV using attribute access only."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['scale', 'uniformity', 'robustness', 'tradeoff'])
        for i in range(len(result.tradeoff_values)): 
            writer.writerow([' '.join(str(x) for x in result.scales[i]), result.uniformity_values[i], result.robustness_values[i], result.tradeoff_values[i]])
