from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray


@dataclass
class OptimizeDictReturn:
    uniformity: float
    robustness: float
    tradeoff: float


@dataclass
class OptimizeReturn:
    optimal_tradeoff: float
    optimal_scale: float
    tradeoff_values: dict[str, OptimizeDictReturn]


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

    optimal_index = np.argmax(tradeoff)
    optimal_tradeoff = tradeoff[optimal_index]
    optimal_scale = scales[optimal_index]

    tradeoff_values = {}

    for i, scale in enumerate(scales):
        tradeoff_values[str(scale)] = OptimizeDictReturn(
            uniformity[i], robustness[i], tradeoff[i]
        )

    result = OptimizeReturn(
        optimal_tradeoff,
        optimal_scale,
        tradeoff_values,
    )

    return result
