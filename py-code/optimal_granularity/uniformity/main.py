from random import uniform
import numpy as np
from numpy.typing import NDArray

from .clark_evans import clark_evans_csr_vectorized

from ..utils import BoundingSquare, create_random_quadrats


def uniformity(
    points: NDArray[np.float64],
    scales: NDArray[np.float64],
    num_random_quadrats: int,
    bbox: BoundingSquare,
    signif: float,
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
        quadrats = create_random_quadrats(
            quadrat_size=scale, bbox=bbox, n_quadrats=num_random_quadrats
        )

        csr_passed = clark_evans_csr_vectorized(points, quadrats, scale, alpha=signif)

        uniformity_value = np.sum(csr_passed) / num_random_quadrats

        uniformity_values[idx] = uniformity_value

    return uniformity_values
