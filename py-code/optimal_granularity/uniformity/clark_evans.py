from math import erfc, sqrt

import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

from ..utils import BoundingSquare


def clark_evans_csr_vectorized(
    points: NDArray[np.float64],
    quadrat_positions: NDArray[np.float64],
    quadrat_size: float,
    alpha=0.05,
) -> NDArray[np.bool_]:
    """
    Vectorized Clark-Evans CSR test for multiple quadrats.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_positions: Array of shape (n_quadrats, 2) with bottom-left corners of quadrats
        quadrat_size: Size of the square quadrats
        alpha: Significance level for the hypothesis test

    Returns:
        Array of shape (n_quadrats,) with boolean values indicating CSR test results
        True if pattern is consistent with CSR (p-value >= alpha), False otherwise
    """
    n_quadrats = quadrat_positions.shape[0]
    results = np.zeros(n_quadrats, dtype=bool)

    for i in range(n_quadrats):
        # Extract points inside current quadrat
        x_min, y_min = quadrat_positions[i]
        x_max = x_min + quadrat_size
        y_max = y_min + quadrat_size

        # Find points inside quadrat
        inside_x = (points[:, 0] >= x_min) & (points[:, 0] < x_max)
        inside_y = (points[:, 1] >= y_min) & (points[:, 1] < y_max)
        inside_quadrat = inside_x & inside_y

        quadrat_points = points[inside_quadrat]

        # Skip if too few points for meaningful analysis
        if quadrat_points.shape[0] < 3:
            results[i] = False  # or True, depending on desired behavior
            continue

        # Create bounding box for this quadrat
        quadrat_bbox = BoundingSquare(
            minx=x_min,
            miny=y_min,
            maxx=x_max,
            maxy=y_max,
            area=quadrat_size * quadrat_size,
        )

        # Perform Clark-Evans test
        results[i] = clark_evans_csr(quadrat_points, quadrat_bbox, alpha)

    return results


def clark_evans_csr(
    points: NDArray[np.float64], bbox: BoundingSquare, alpha=0.05
) -> bool:
    """
    Test if point pattern follows Complete Spatial Randomness (CSR) using Clark-Evans test.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        alpha: Significance level for the hypothesis test

    Returns:
        True if pattern is consistent with CSR (p-value >= alpha), False otherwise
    """
    num_points = points.shape[0]

    r_observed = _mean_nearest_neighbor_distance(points)

    points_intensity = num_points / bbox.area
    r_expected = 0.5 / np.sqrt(points_intensity)

    std_dev = 0.26136 * np.sqrt(bbox.area) / num_points
    z = (r_observed - r_expected) / std_dev

    p_two_sided = erfc(abs(z) / sqrt(2.0))

    return p_two_sided >= alpha


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
