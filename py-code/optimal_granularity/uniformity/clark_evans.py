from math import erfc, sqrt

import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

from ..utils import BoundingBox


def clark_evans_csr_vectorized(
    points: NDArray[np.float64],
    list_bboxes: list[BoundingBox],
    signif=0.95,
) -> NDArray[np.bool_]:
    """
    Vectorized Clark-Evans CSR test for multiple quadrats.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        list_bboxes: List of BoundingBox objects representing the quadrats
        signif: Significance level for the hypothesis test

    Returns:
        Array of shape (n_quadrats,) with boolean values indicating CSR test results
        True if pattern is consistent with CSR (p-value >= alpha), False otherwise
    """
    n_quadrats = len(list_bboxes)
    results = np.zeros(n_quadrats, dtype=bool)

    for i in range(n_quadrats):
        # Get current quadrat bounding box
        quadrat_bbox = list_bboxes[i]
        
        # Find points inside quadrat
        inside_x = (points[:, 0] >= quadrat_bbox.minx) & (points[:, 0] < quadrat_bbox.maxx)
        inside_y = (points[:, 1] >= quadrat_bbox.miny) & (points[:, 1] < quadrat_bbox.maxy)
        inside_quadrat = inside_x & inside_y

        quadrat_points = points[inside_quadrat]

        # Skip if too few points for meaningful analysis
        if quadrat_points.shape[0] < 3:
            results[i] = False  # or True, depending on desired behavior
            continue

        # Perform Clark-Evans test using the existing bounding box
        results[i] = clark_evans_csr(quadrat_points, quadrat_bbox, signif)

    return results


def clark_evans_csr(
    points: NDArray[np.float64], bbox: BoundingBox, signif=0.95
) -> bool | None:
    """
    Test if point pattern follows Complete Spatial Randomness (CSR) using Clark-Evans test.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        bbox: BoundingBox defining the area of interest
        alpha: Significance level for the hypothesis test

    Returns:
        True if pattern is consistent with CSR (p-value >= alpha), False otherwise
        None if there are fewer than 3 points (test not applicable)
    """
    num_points = points.shape[0]
    
    if num_points < 3:
        return None
    
    if num_points < 20:
        return clark_evans_csr_monte_carlo(points, bbox, signif)

    r_observed = _mean_nearest_neighbor_distance(points)

    points_intensity = num_points / bbox.area
    r_expected = 0.5 / np.sqrt(points_intensity)

    std_dev = 0.26136 * np.sqrt(bbox.area) / num_points
    z = (r_observed - r_expected) / std_dev

    p_two_sided = erfc(abs(z) / sqrt(2.0))

    return p_two_sided >= (1-signif)


def clark_evans_csr_monte_carlo(
    points: NDArray[np.float64], bbox: BoundingBox,
    signif: float = 0.95, num_simulations: int = 100
) -> bool:
    """
    Two-sided Monte Carlo Clark-Evans test (binomial CSR, conditional on n).
    Returns True iff p >= alpha (= 1 - signif), i.e., consistent with CSR.
    """
    n = points.shape[0]
    area = bbox.area

    r_obs = _mean_nearest_neighbor_distance(points)
    r_exp = 0.5 / np.sqrt(n / area)
    R_obs = r_obs / r_exp
    T_obs = abs(R_obs - 1.0)

    extreme = 0
    for _ in range(num_simulations):
        rand_x = np.random.uniform(bbox.minx, bbox.maxx, n)
        rand_y = np.random.uniform(bbox.miny, bbox.maxy, n)
        sim = np.column_stack((rand_x, rand_y))
        r_sim = _mean_nearest_neighbor_distance(sim)
        R_sim = r_sim / r_exp
        T_sim = abs(R_sim - 1.0)
        if T_sim >= T_obs:
            extreme += 1

    p_value = (extreme + 1.0) / (num_simulations + 1.0)
    return p_value >= (1.0 - signif)



def _mean_nearest_neighbor_distance(points: np.ndarray) -> float:
    """
    Calculate mean nearest-neighbor distance for a 2D point set.

    Args:
        points: Array of shape (n_points, 2) with point coordinates

    Returns:
        Mean distance to nearest neighbor for all points

    Notes:
        Uses scipy.spatial.cKDTree for efficient computation.
        Query with k=2 to get nearest neighbor excluding the point itself.
    """
    tree = cKDTree(points)
    dists, _ = tree.query(
        points, k=2
    )  # k=2: the nearest neighbor of each point, excluding the point itself
    nn = dists[:, 1]
    return float(nn.mean())
