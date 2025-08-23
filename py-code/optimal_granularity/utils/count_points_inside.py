import numpy as np
from numpy.typing import NDArray

def count_points_in_quadrat(
    points: NDArray[np.float64],
    quadrat_position: NDArray[np.float64],
    quadrat_size: float) -> int:
    """
    Count how many points are inside a given square quadrat.
    
    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_position: Array of shape (2,) with bottom-left corner of quadrat
        quadrat_size: Size of the square quadrat
        
    Returns:
        Number of points inside the quadrat
    """
    x_min, y_min = quadrat_position
    x_max = x_min + quadrat_size
    y_max = y_min + quadrat_size
    
    # Method 1: Using boolean indexing (most efficient)
    inside_x = (points[:, 0] >= x_min) & (points[:, 0] < x_max)
    inside_y = (points[:, 1] >= y_min) & (points[:, 1] < y_max)
    inside_quadrat = inside_x & inside_y
    
    return np.sum(inside_quadrat)


def count_points_in_quadrat_vectorized(
    points: NDArray[np.float64],
    quadrat_positions: NDArray[np.float64],
    quadrat_size: float) -> NDArray[np.int64]:
    """
    Count points in multiple quadrats at once (vectorized version).
    
    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_positions: Array of shape (n_quadrats, 2) with bottom-left corners
        quadrat_size: Size of the square quadrats
        
    Returns:
        Array of shape (n_quadrats,) with counts for each quadrat
    """
    n_quadrats = quadrat_positions.shape[0]
    counts = np.zeros(n_quadrats, dtype=np.int64)
    
    for i in range(n_quadrats):
        quadrat_pos = quadrat_positions[i]
        counts[i] = count_points_in_quadrat(points, quadrat_pos, quadrat_size)
    
    return counts


def count_points_in_quadrat_broadcast(
    points: NDArray[np.float64],
    quadrat_positions: NDArray[np.float64],
    quadrat_size: float) -> NDArray[np.int64]:
    """
    Fast vectorized version using broadcasting (for large datasets).
    If there is not much data, it can be slower.
    
    Comparable performance case example: 1000 quadrats and 1_000_000 points
    Better performance case example: 1000 quadrats and 2_000_000 points
    Be careful because the broadcast consumes too much memory
    
    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_positions: Array of shape (n_quadrats, 2) with bottom-left corners
        quadrat_size: Size of the square quadrats
        
    Returns:
        Array of shape (n_quadrats,) with counts for each quadrat
    """
    # Expand dimensions for broadcasting
    # points: (n_points, 1, 2)
    # quadrat_positions: (1, n_quadrats, 2)
    points_expanded = points[:, np.newaxis, :]
    quadrats_expanded = quadrat_positions[np.newaxis, :, :]
    
    # Calculate boundaries
    x_min = quadrats_expanded[:, :, 0]  # (1, n_quadrats)
    y_min = quadrats_expanded[:, :, 1]  # (1, n_quadrats)
    x_max = x_min + quadrat_size
    y_max = y_min + quadrat_size
    
    # Check if points are inside each quadrat
    # Result shape: (n_points, n_quadrats)
    inside_x = (points_expanded[:, :, 0] >= x_min) & (points_expanded[:, :, 0] < x_max)
    inside_y = (points_expanded[:, :, 1] >= y_min) & (points_expanded[:, :, 1] < y_max)
    inside_quadrats = inside_x & inside_y
    
    # Count points in each quadrat
    counts = np.sum(inside_quadrats, axis=0)
    
    return counts
