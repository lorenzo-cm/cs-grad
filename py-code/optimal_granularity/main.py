from time import perf_counter
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from .optimizer import OptimizeReturn, optimize
from .robustness import robustness as calculate_robustness
from .uniformity import uniformity as calculate_uniformity
from .utils import BoundingBox, gen_scales_from_bbox


def get_optimal_granularity(
    points: NDArray[np.float64],  # (num_points, 2)
    tradeoff_method: Literal["sum", "product"],
    size_scale: int = 10,
    signif: float = 0.99,
    uniformity_num_random_quadrats_per_scale: int = 200,
    robustness_num_simulations: int = 200,
    robustness_num_bootstrap: int = 100,
    verbose: bool = True,
) -> float:
    """
    Get the optimal granularity

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        tradeoff_method: Method for calculating tradeoff between robustness and uniformity
        signif: Significance level
        num_random_quadrats: Number of random quadrats generated to calculate uniformity

    Returns:
        Optimal granularity
    """

    bbox: BoundingBox = BoundingBox.from_points(points)  # not a square bounding box
    scales = gen_scales_from_bbox(bbox, size=size_scale)

    if verbose:
        print(f"Starting calculating uniformity")
        time_init_unif = perf_counter()

    uniformity = calculate_uniformity(
        points=points,
        scales=scales,
        num_random_quadrats=uniformity_num_random_quadrats_per_scale,
        bbox=bbox,
        signif=signif,
        method="quadrat_count",
        verbose=verbose,
    )

    if verbose:
        print(f"Uniformity calculated in {perf_counter() - time_init_unif:.2f} seconds")

        print(f"Starting calculating robustness")
        time_init_robust = perf_counter()

    robustness = calculate_robustness(
        points=points,
        scales=scales,
        bbox=bbox,
        signif=signif,
        num_simulations=robustness_num_simulations,
        num_bootstrap=robustness_num_bootstrap,
        verbose=verbose,
    )

    if verbose:
        print(
            f"Robustness calculated in {perf_counter() - time_init_robust:.2f} seconds"
        )

        print(f"Starting optimization")

    optimal_scale: OptimizeReturn = optimize(
        scales=scales,
        uniformity=uniformity,
        robustness=robustness,
        method=tradeoff_method
    )

    if verbose:
        print(f"Optimal scale: {optimal_scale.optimal_scale}")
        print(f"Optimal granularity: {optimal_scale.optimal_granularity}")
        
        for scale, values in optimal_scale.tradeoff_values.items():
            print(f"Scale: {scale}, Uniformity: {values.uniformity}, Robustness: {values.robustness}, Tradeoff: {values.tradeoff}")

    return optimal_scale.optimal_scale
