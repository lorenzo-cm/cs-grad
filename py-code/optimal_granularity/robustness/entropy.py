from typing import Sequence
import numpy as np
from dataclasses import dataclass
from typing import Literal
from numpy.typing import NDArray
from collections import Counter

from ..utils import BoundingBoxBase


@dataclass
class EntropyResult:
    """
    **Relative entropy** is the points entropy divided by the uniform entropy.

    **Uniform entropy** is the entropy of a uniform distribution over the bounding box.

    **Points entropy** is the entropy of the distribution of points.
    """

    relative_entropy: float
    uniform_entropy: float
    points_entropy: float


def entropy_score(
    points: NDArray[np.float64],
    bbox_sizes: Sequence[float],
    bbox: BoundingBoxBase,
    num_simulations: int,
    binning_method: Literal["auto", "sturges", "fd", "scott", "rice", "sqrt", "stone", "doane", "unique"],
) -> EntropyResult:
    """
    Calculate entropy score for shapefile point pattern robustness analysis.

    Args:
        points: Array of shape (n_points, n_dims)
        bbox_scales: List of quadrat sizes, can be multidimensional, it will create a bbox respecting the sizes
        bbox: Bounding box defining the study area
        num_simulations: Number of random quadrats to generate for each scale
        binning_method: Method for binning the counts

    Returns:
        EntropyResult: Dataclass containing relative_entropy, uniform_entropy, and points_entropy.
    """
    counts = []
    random_bboxes = bbox.create_random_bboxes(
        bbox_sizes=bbox_sizes, n_quadrats=num_simulations
    )

    for bbox in random_bboxes:
        points_in_bbox = bbox.points_inside(points)
        counts.append(points_in_bbox.count)

    entropy: EntropyResult
    if binning_method == "unique":
        entropy = calculate_entropy_unique(counts)
    else:
        entropy = calculate_entropy(counts, binning_method)

    return entropy


def calculate_entropy(
    count_in_quadrats: list[int],
    binning_method: Literal["auto", "sturges", "fd", "scott", "rice", "sqrt", "stone", "doane"],
) -> EntropyResult:
    """
    Calculate the entropy of a counts distribution.
    These counts represent the number of points in each quadrat sampled earlier.

    Args:
        count_in_quadrats: List of counts of points in each quadrat.

    Returns:
        EntropyResult: Dataclass containing relative_entropy, uniform_entropy, and points_entropy.
    """

    # There are some methods that can be used for binning
    # "auto": sturges + freedman-diaconis corrected
    # "sturges": good for normal distributions
    # "fd": less accurate for long tails, but robust in general
    # "scott": similar to fd, but more sensitive to outliers
    # "rice": like Sturges but always gives more bins (good for larger n)
    # "sqrt": simple, but not very accurate
    # "stone": minimizes the integrated mean squared error
    # "doane": modification of sturges, works better for non-normal data
    # OBS: edges are [min, max), then size of edges is len(hist) + 1 -> The last edge is [min, max]
    hist, edges = np.histogram(count_in_quadrats, binning_method)

    # Probability of each bin
    probabilities = hist / sum(hist)

    # Filter out zero probabilities to avoid log(0)
    probabilities = probabilities[probabilities > 0]

    # Calculate points entropy
    points_entropy = -np.sum(probabilities * np.log2(probabilities))

    # Calculate uniform entropy
    num_bins = len(hist)
    uniform_entropy = np.log2(num_bins)

    # Calculate relative entropy
    relative_entropy = points_entropy / uniform_entropy if uniform_entropy > 0 else 1.0

    return EntropyResult(
        relative_entropy=relative_entropy,
        uniform_entropy=uniform_entropy,
        points_entropy=points_entropy,
    )
    
    
def calculate_entropy_unique(
    count_in_quadrats: list[int],
) -> EntropyResult:
    """
    Entropy of the distribution of counts divided by the uniform entropy calculated from the number of quadrats, not binned.
    """
    counter = Counter(count_in_quadrats)
    distribution = np.array(list(counter.values()), dtype=float)
    
    if len(distribution) == 0:
        return EntropyResult(
            relative_entropy=1.0,
            uniform_entropy=0.0,
            points_entropy=0.0,
        )
    
    num_quadrats = len(count_in_quadrats)

    probabilities = distribution / num_quadrats
    probabilities = probabilities[probabilities > 0]
    points_entropy = -np.sum(probabilities * np.log2(probabilities)) 
    
    num_bins_distribution = len(distribution)

    uniform_entropy: float = np.log2(num_bins_distribution)
    
    relative_entropy = points_entropy / uniform_entropy if uniform_entropy > 0 else 1.0
    
    return EntropyResult(
        relative_entropy=relative_entropy,
        uniform_entropy=uniform_entropy,
        points_entropy=points_entropy,
    )

