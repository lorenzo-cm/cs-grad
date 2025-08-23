import numpy as np
from numpy.typing import NDArray
from .bounding_box import BoundingSquare

def create_random_points(
    bbox: BoundingSquare,
    n_points: int) -> NDArray[np.float64]:
    """
    Generate random points within the bounding box.
    
    Args:
        bbox: BoundingSquare object defining the sampling area
        n_points: Number of points to generate
        
    Returns:
        Array of shape (n_points, 2) with x, y coordinates
    """
    # Generate random x coordinates within bbox
    x_coords = np.random.uniform(bbox.minx, bbox.maxx, n_points)
    
    # Generate random y coordinates within bbox
    y_coords = np.random.uniform(bbox.miny, bbox.maxy, n_points)
    
    # Stack coordinates into (n_points, 2) array
    points = np.column_stack((x_coords, y_coords))
    
    return points


def create_random_quadrats(
    quadrat_size: float,
    bbox: BoundingSquare,
    n_quadrats: int = 500) -> NDArray[np.float64]:
    """
    Generate random quadrat positions for sampling within the bounding box.
    
    Args:
        quadrat_size: Size of the quadrat (assuming square quadrats)
        bbox: BoundingSquare object defining the sampling area
        n_quadrats: Number of random quadrats to generate
        
    Returns:
        Array of shape (n_quadrats, 2) with bottom-left corner coordinates of quadrats
    """
    # Calculate available space for quadrat placement
    # Quadrat must fit entirely within the bounding box
    max_x = bbox.maxx - quadrat_size
    max_y = bbox.maxy - quadrat_size
    
    if max_x < bbox.minx or max_y < bbox.miny:
        raise ValueError("Quadrat size is too large for the bounding box")
    
    # Generate random bottom-left corner positions
    offset_x = np.random.uniform(bbox.minx, max_x, n_quadrats)
    offset_y = np.random.uniform(bbox.miny, max_y, n_quadrats)
    
    # Stack into (n_quadrats, 2) array
    quadrat_positions = np.column_stack((offset_x, offset_y))
    
    return quadrat_positions


def create_contiguous_quadrats(
    quadrat_size: float,
    bbox: BoundingSquare) -> NDArray[np.float64]:
    """
    Generate contiguous (regular grid) quadrat positions within the bounding box.
    
    Args:
        quadrat_size: Size of the quadrat (assuming square quadrats)
        bbox: BoundingSquare object defining the sampling area
        
    Returns:
        Array of shape (nx*ny, 2) with bottom-left corner coordinates of quadrats
        where nx, ny are the number of quadrats that fit in each dimension
    """
    width = bbox.maxx - bbox.minx
    height = bbox.maxy - bbox.miny
    
    # Calculate how many quadrats fit in each dimension
    nx = int(width // quadrat_size)  # Number of quadrats in x direction
    ny = int(height // quadrat_size)  # Number of quadrats in y direction
    
    if nx == 0 or ny == 0:
        raise ValueError("Quadrat size is too large for the bounding box")
    
    # Create grid of quadrat positions starting from bbox min coordinates
    x_positions = bbox.minx + np.arange(nx) * quadrat_size
    y_positions = bbox.miny + np.arange(ny) * quadrat_size
    
    # Create meshgrid to get all combinations
    x_grid, y_grid = np.meshgrid(x_positions, y_positions)
    
    # Flatten and stack into (nx*ny, 2) array
    quadrat_positions = np.column_stack((x_grid.flatten(), y_grid.flatten()))
    
    return quadrat_positions
