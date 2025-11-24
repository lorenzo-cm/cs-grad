import csv

import numpy as np
from optimal_granularity.optimizer import OptimizeReturn


def save_results_to_csv(result: OptimizeReturn, filename: str) -> None:
    """
    Save optimization results to CSV
    
    Scales are saved as a string of space-separated values.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["scale", "uniformity", "robustness", "tradeoff"])
        for i in range(len(result.tradeoff_values)):
            writer.writerow(
                [
                    " ".join(str(x) for x in result.scales[i]),
                    result.uniformity_values[i],
                    result.robustness_values[i],
                    result.tradeoff_values[i],
                ]
            )
            

def load_results_from_csv(filename: str) -> OptimizeReturn:
    """Load optimization results from CSV."""
    scales_list = []
    uniformity_values = []
    robustness_values = []
    tradeoff_values = []

    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            scale_str = row["scale"]
            scale_values = [float(x) for x in scale_str.split()]
            scales_list.append(scale_values)

            uniformity_values.append(float(row["uniformity"]))
            robustness_values.append(float(row["robustness"]))
            tradeoff_values.append(float(row["tradeoff"]))

    scales_array = np.array(scales_list, dtype=np.float64)
    uniformity_array = np.array(uniformity_values, dtype=np.float64)
    robustness_array = np.array(robustness_values, dtype=np.float64)
    tradeoff_array = np.array(tradeoff_values, dtype=np.float64)

    optimal_index = np.argmax(tradeoff_array)
    optimal_tradeoff = tradeoff_array[optimal_index]
    optimal_scale = scales_array[optimal_index]

    return OptimizeReturn(
        optimal_tradeoff=optimal_tradeoff,
        optimal_scale=optimal_scale,
        tradeoff_values=tradeoff_array,
        uniformity_values=uniformity_array,
        robustness_values=robustness_array,
        scales=scales_array,
    )
