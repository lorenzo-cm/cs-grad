from typing import Literal
import numpy as np
from numpy.typing import NDArray

from .clark_evans import clark_evans_csr_vectorized
from .quadrat_count import quadrat_count_csr_vectorized

from ..utils import BoundingBox, create_random_quadrats


def uniformity(
    points: NDArray[np.float64],
    scales: NDArray[np.float64],
    num_random_quadrats: int,
    bbox: BoundingBox,
    signif: float,
    method: Literal["clark_evans", "quadrat_count"] = "quadrat_count",
    verbose: bool = False,
) -> NDArray[np.float64]:
    """
    Calculate uniformity for each scale.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        scales: Array of scales to evaluate
        num_random_quadrats: Number of random quadrats to generate for each scale

    Returns:
        Array of uniformity values for each scale
    """
    uniformity_values = np.zeros(len(scales))

    for idx, scale in enumerate(scales):
        quadrats: list[BoundingBox] = create_random_quadrats(
            quadrat_size=scale, bbox=bbox, n_quadrats=num_random_quadrats
        )
        
        csr_passed: NDArray[np.bool_]
        
        if method == "clark_evans":
            csr_passed = clark_evans_csr_vectorized(points, quadrats, signif)
        
        elif method == "quadrat_count":
            csr_passed = quadrat_count_csr_vectorized(points, quadrats, signif)
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if verbose:
            print(f"Scale: {scale}, CSR passed: {csr_passed} out of {len(csr_passed)}")
            
        csr_passed_filtered = csr_passed[csr_passed != None]
        
        if len(csr_passed_filtered) == 0:
            uniformity_value = 0.0
        
        else: 
            uniformity_value = np.sum(csr_passed) / len(csr_passed)
            
            if verbose:
                print(f"Scale: {scale}, Uniformity: {uniformity_value}")
            

        uniformity_values[idx] = uniformity_value

    return uniformity_values
