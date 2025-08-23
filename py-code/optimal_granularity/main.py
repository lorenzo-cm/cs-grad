import numpy as np
from numpy.typing import NDArray 
from typing import Literal

from utils.bounding_box import bounding_square_from_points, BoundingSquare
from utils.gen_scales import gen_scales_from_bbox

def get_optimal_granularity(
    points: NDArray[np.float64], # (num_points, 2)
    tradeoff_method: Literal["sum", "product"],
    signif: float,
    num_random_quadrats: int,
) -> float:
    """
    Get the optimal granularity
    
    Args:
        points: Array of shape (n_points, 2) with point coordinates
        tradeoff_method: Method for calculating tradeoff between robustness and uniformity 
        signif: Significance level
        num_random_quadrats: Number of random quadrats generated to calculate uniformity 
    
    Returns:
        Optimal granularity
    """
    
    bbox: BoundingSquare = bounding_square_from_points(points)
    scales = gen_scales_from_bbox(bbox, size=10)

    # uniformity =
    # robustness =
    
    # optimal_scale = optimizer(scales, uniformity, robustness, tradeoff_method)
    
    # return optimal_scale
    
    raise NotImplementedError("Function not yet implemented.")
