import itertools
from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
from numpy.typing import NDArray


@dataclass
class OptimizeReturn:
    optimal_tradeoff: float
    optimal_scale: Sequence[float]
    tradeoff_values: NDArray[np.float64]
    uniformity_values: NDArray[np.float64]
    robustness_values: NDArray[np.float64]
    scales: NDArray[np.float64] # (num_scales_combinations, num_dimensions)


def optimize(
    scales: NDArray[np.float64],
    uniformity: NDArray[np.float64],
    robustness: NDArray[np.float64],
    method: Literal["sum", "product"],
) -> OptimizeReturn:
    if method == "sum":
        tradeoff = uniformity + robustness

    elif method == "product":
        tradeoff = uniformity * robustness

    else:
        raise ValueError(f"Unknown method: {method}")
    
    scales_list = [dim_scales for dim_scales in scales]
    scales_combos = list(itertools.product(*scales_list))

    optimal_index = np.argmax(tradeoff)
    optimal_tradeoff = tradeoff[optimal_index]
    optimal_scale = scales_combos[optimal_index]

    result = OptimizeReturn(
        optimal_tradeoff,
        optimal_scale,
        tradeoff,
        uniformity,
        robustness,
        np.array(scales_combos)
    )

    return result
