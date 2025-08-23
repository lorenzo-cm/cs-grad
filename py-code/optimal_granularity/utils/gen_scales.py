import numpy as np
from numpy.typing import NDArray
from .bounding_box import BoundingSquare

def gen_scales_from_bbox(
    bbox: BoundingSquare,
    size: int = 10,
    as_int: bool = True) -> NDArray:
    """
    Generate a range of scales for spatial analysis based on bounding box.
    
    Args:
        bbox: BoundingSquare object containing the study area bounds
        size: Number of scales to generate
        as_int: If True, round scales to integers; if False, keep as floats
        
    Returns:
        Array of scales ranging from start to stop values
        
    Notes:
        - stop = 0.5 * min_side: Maximum scale at 50% of study min side to ensure coverage
        - start = 0.05 * stop: Minimum scale at 5% of maximum to avoid overly fine granularity
    """
    # 1000x1000 = 1_000_000
    # stop = 1000 * 0.5 = 500
    # start = 500 * 0.05 = 25
    min_side = min(bbox.maxx - bbox.minx, bbox.maxy - bbox.miny)
    stop = 0.5 * min_side  # Maximum scale based on the min side
    start = 0.05 * stop  # Minimum scale to avoid overly fine granularity
    scales = np.linspace(start, stop, size)
    
    if as_int:
        scales = np.round(scales).astype(int)
        # Remove duplicates that may occur after rounding
        scales = np.unique(scales)
    
    return scales
    