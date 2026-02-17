import numpy as np
from numpy.typing import NDArray

def normalize_points_to_positive(points: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Normalize point coordinates from shapefile to positive values.

    Args:
        points: Array of shape (n_points, n_dims) where n_dims can be any number of dimensions

    Returns:
        Normalized points with all positive coordinates
    """
    min_coords = points.min(axis=0)
    offsets = np.where(min_coords < 0, np.abs(min_coords), 0)

    normalized_points = points + offsets

    return normalized_points
