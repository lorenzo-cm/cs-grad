import numpy as np
from numpy.typing import NDArray

from ..utils import BoundingBoxBase


def quadrat_count_csr_vectorized(
    points: NDArray[np.float64],
    list_bboxes: list[BoundingBoxBase],
    signif: float,
    num_simulations: int,
) -> NDArray[np.bool_]:
    """
    Vectorized quadrat count CSR test for multiple regions.
    
    Args:
        points: Array of shape (n_points, n_dims)
        list_bboxes: List of quadrat bboxes (each can be 2D, 3D, ...)
        signif: Significance level (e.g., 0.95)
        num_simulations: Number of Monte Carlo simulations
        number_of_quadrats_per_side: Subdivisions per axis for each bbox grid
    """

    list_passed = []
    for bbox in list_bboxes:

        points_inside: BoundingBoxBase.PointsInside = bbox.points_inside(points)
        quadrat_points = points_inside.points

        passed = quadrat_count_monte_carlo_csr(
            points=quadrat_points,
            bbox=bbox,
            signif=signif,
            num_simulations=num_simulations,
        )

        list_passed.append(passed)

    return np.array(list_passed)


def quadrat_count_monte_carlo_csr(
    points: NDArray[np.float64],
    bbox: BoundingBoxBase,
    signif,
    num_simulations,
    number_of_quadrats_per_side: int = 5,
) -> bool | None:
    """
    Monte Carlo quadrat count CSR test.

    Method Idea:
    - We want to check if the point distribution is consistent with Complete Spatial Randomness (CSR).
    - Divide the bbox into a regular grid of quadrats (voxels in 3D, hyper-rectangles in nD)
    - We expect, under CSR, that points are uniformly distributed across these quadrats
    - Hence, the number of points in each quadrat should be TOTAL_POINTS / TOTAL_QUADRATS
    - We then compare the point counts in each quadrat to this expected count using a chi-square statistic.
    - In normal quadrat counts, this is enough, but in Monte Carlo, we go further:
        - We simulate many random point patterns under CSR
        - We compute the chi-square statistic for each simulated pattern
        - We then compare these chi-square stastistics from the random patterns to the original pattern's chi-square statistic
        - If the new chi-squares are often larger than the original, we fail to reject the null hypothesis of CSR
        - Otherwise, if the new chi-squares are rarely larger, we reject the null hypothesis of CSR

    Args:
    points: Array of shape (n_points, n_dims)
    bbox: BoundingBox defining the study region (2D, 3D, ...)
        signif: Significance level for the hypothesis test (default 0.95)
    number_of_quadrats_per_side: Number of quadrats along each axis of the bounding box (default 5)
        num_simulations: Number of Monte Carlo simulations to perform (default 999)

    Returns:
        True if the point pattern is consistent with CSR (p-value >= signif), False otherwise
    """
    if bbox.ndim >= 3:
        # Keep grids modest in higher dimensions to combat combinatorial explosion
        number_of_quadrats_per_side = 2

    # Get the number of points
    points_inside: BoundingBoxBase.PointsInside = bbox.points_inside(points)

    # If number of pointes is less than 5, we cannot perform the test reliably
    if points_inside.count < 5:
        return True

    # Calculate the expected number of points per quadrat in nD
    total_quadrats = number_of_quadrats_per_side ** bbox.ndim
    expected_count = points_inside.count / total_quadrats

    # Divide in quadrats
    bboxes = bbox.divide_into_quadrats(number_of_quadrats_per_side)

    # Count points in each quadrat
    observed_counts = []
    for quadrat in bboxes:
        points_in_input: BoundingBoxBase.PointsInside = quadrat.points_inside(points)
        observed_counts.append(points_in_input.count)

    observed_counts_np = np.array(observed_counts)

    # Chi-square statistic from observed and expected counts
    chi_square_og = np.sum((observed_counts_np - expected_count) ** 2 / expected_count)

    # Monte Carlo simulations
    chi_squares_sims = []
    for i in range(num_simulations):
        points_random = bbox.create_random_points(points_inside.count)
        counts_random = []
        for quadrat in bboxes:
            points_in_random: BoundingBoxBase.PointsInside = quadrat.points_inside(
                points_random
            )
            counts_random.append(points_in_random.count)
        counts_random_np = np.array(counts_random)
        chi_square_sim = np.sum(
            (counts_random_np - expected_count) ** 2 / expected_count
        )
        chi_squares_sims.append(chi_square_sim)

    chi_square_sims_np = np.array(chi_squares_sims)

    # Calculate p-value
    p_value = (np.sum(chi_square_sims_np >= chi_square_og) + 1) / (num_simulations + 1)

    # Determine if we reject the null hypothesis
    return p_value >= (1 - signif)
