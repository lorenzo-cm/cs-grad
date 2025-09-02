import numpy as np
from numpy.typing import NDArray
from .bounding_box import BoundingBox

def create_random_points(
    bbox: BoundingBox,
    n_points: int) -> NDArray[np.float64]:
    """
    Generate random points within the bounding box.
    
    Args:
        bbox: BoundingBox object defining the sampling area
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
    bbox: BoundingBox,
    n_quadrats: int = 500) -> list[BoundingBox]:
    """
    Generate random quadrat positions for sampling within the bounding box.
    
    Args:
        quadrat_size: Size of the quadrat (assuming square quadrats)
        bbox: BoundingBox object defining the sampling area
        n_quadrats: Number of random quadrats to generate
        
    Returns:
        List of BoundingBox objects representing the quadrats
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
    
    # Create list of BoundingBox objects for each quadrat
    quadrat_bboxes = []
    for i in range(n_quadrats):
        minx = offset_x[i]
        miny = offset_y[i]
        maxx = minx + quadrat_size
        maxy = miny + quadrat_size
        area = quadrat_size * quadrat_size
        
        quadrat_bbox = BoundingBox(
            minx=minx,
            miny=miny,
            maxx=maxx,
            maxy=maxy,
            area=area
        )
        quadrat_bboxes.append(quadrat_bbox)
    
    return quadrat_bboxes


def create_contiguous_quadrats(
    quadrat_size: float,
    bbox: BoundingBox) -> list[BoundingBox]:
    """
    Generate contiguous (regular grid) quadrat positions within the bounding box.
    
    Args:
        quadrat_size: Size of the quadrat (assuming square quadrats)
        bbox: BoundingBox object defining the sampling area
        
    Returns:
        List of BoundingBox objects representing the quadrats in a regular grid
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
    
    # Create list of BoundingBox objects for each quadrat
    quadrat_bboxes = []
    for i in range(nx):
        for j in range(ny):
            minx = x_positions[i]
            miny = y_positions[j]
            maxx = minx + quadrat_size
            maxy = miny + quadrat_size
            area = quadrat_size * quadrat_size
            
            quadrat_bbox = BoundingBox(
                minx=minx,
                miny=miny,
                maxx=maxx,
                maxy=maxy,
                area=area
            )
            quadrat_bboxes.append(quadrat_bbox)
    
    return quadrat_bboxes
