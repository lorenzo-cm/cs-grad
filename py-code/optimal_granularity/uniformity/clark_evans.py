import numpy as np
from scipy.spatial import cKDTree
from math import sqrt, erfc

from utils import bounding_square_from_points, BoundingSquare

def clark_evans_csr(points: np.ndarray, alpha=0.05) -> bool:
    num_points = points.shape[0]

    bbox: BoundingSquare = bounding_square_from_points(points)

    r_observed = _mean_nearest_neighbor_distance(points)

    points_intensity = num_points / bbox.area
    r_expected = 0.5 / np.sqrt(points_intensity)

    std_dev = 0.26136 * np.sqrt(bbox.area) / num_points
    z = (r_observed - r_expected) / std_dev

    p_two_sided = erfc(abs(z) / sqrt(2.0))

    return p_two_sided >= alpha

def _mean_nearest_neighbor_distance(points: np.ndarray) -> float:
    """
    Mean nearest-neighbor distance for a 2D point set.
    Uses scipy.spatial.cKDTree if available; otherwise, a NumPy O(n^2) fallback.
    """
    tree = cKDTree(points)
    dists, _ = tree.query(points, k=2) # k=2: the nearest neighbor of each point, excluding the point itself
    nn = dists[:, 1]
    return float(nn.mean())

def _two_sided_p_from_z(z: float) -> float:
    """
    Two-sided p-value from z without SciPy (uses erfc).
    p = 2 * (1 - Phi(|z|)) = erfc(|z| / sqrt(2))
    """
    return erfc(abs(z) / sqrt(2.0))