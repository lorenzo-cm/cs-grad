from time import perf_counter
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from .optimizer import OptimizeReturn, optimize
from .robustness import robustness as calculate_robustness
from .uniformity import uniformity as calculate_uniformity
from .utils import BoundingBoxBase, normalize_points_to_positive


def get_optimal_granularity(
    points: NDArray[np.float64],  # (num_points, 2)
    tradeoff_method: Literal["sum", "product"],
    size_scale: int = 10,
    signif: float = 0.99,
    uniformity_method: Literal["clark_evans", "quadrat_count"] = "quadrat_count",
    uniformity_num_random_quadrats_per_scale: int = 200,
    robustness_num_simulations: int = 200,
    robustness_num_bootstrap: int = 100,
    robustness_binning_method: Literal["auto", "sturges", "fd", "scott", "rice", "sqrt", "stone", "doane", "unique"] = "auto",
    scales_method: Literal["side", "density"] = "density",
    scales_min_points_per_square: int = 1,
    scales_max_percentage_points_per_square: int = 20,
    verbose: bool = False,
) -> OptimizeReturn:
    """
    Get the optimal granularity

    It normalizes points to positive coordinates, computes bounding box,
    generates scales, calculates uniformity and robustness, and optimizes
    to find the optimal granularity.

    Args:
        points: Array of shape (n_points, n_dims)
        tradeoff_method: Method for calculating tradeoff between robustness and uniformity
        signif: Significance level
        num_random_quadrats: Number of random quadrats generated to calculate uniformity

    Returns:
        Optimal granularity
    """
    if verbose:
        print("-" * 40)
        print("Optimal Granularity Calculation")
        print("-" * 40)

        print("Normalizing points to positive coordinates...")

    normalized_points = normalize_points_to_positive(points)

    bbox: BoundingBoxBase = BoundingBoxBase.from_points(normalized_points)
    scales = bbox.gen_scales_from_bbox(size=size_scale,
                                       num_points=len(normalized_points),
                                       min_points_per_square=scales_min_points_per_square,
                                       max_percentage_points_per_square=scales_max_percentage_points_per_square,
                                       method=scales_method)

    if verbose:
        print("Bounding box:", bbox)
        print("Starting calculating uniformity")
        time_init_unif = perf_counter()

    uniformity = calculate_uniformity(
        points=normalized_points,
        scales=scales,
        num_random_quadrats=uniformity_num_random_quadrats_per_scale,
        bbox=bbox,
        signif=signif,
        method=uniformity_method,
        verbose=verbose,
    )

    if verbose:
        print(f"Uniformity calculated in {perf_counter() - time_init_unif:.2f} seconds")

        print("Starting calculating robustness")
        time_init_robust = perf_counter()

    robustness = calculate_robustness(
        points=normalized_points,
        scales=scales,
        bbox=bbox,
        signif=signif,
        num_simulations=robustness_num_simulations,
        num_bootstrap=robustness_num_bootstrap,
        binning_method=robustness_binning_method,
        verbose=verbose,
    )

    if verbose:
        print(
            f"Robustness calculated in {perf_counter() - time_init_robust:.2f} seconds"
        )

        print("Starting optimization")

    optimal_scale: OptimizeReturn = optimize(
        scales=scales,
        uniformity=uniformity,
        robustness=robustness,
        method=tradeoff_method,
    )

    if verbose:
        print(f"Optimal scale: {optimal_scale.optimal_scale}")
        print(f"Optimal granularity: {optimal_scale.optimal_tradeoff}")

    return optimal_scale
