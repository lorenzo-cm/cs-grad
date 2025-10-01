import numpy as np
from dataclasses import dataclass
from numpy.typing import NDArray

from ..utils import BoundingBox


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
    quadrat_size: float,
    bbox: BoundingBox,
    num_simulations: int,
) -> EntropyResult:

    counts = []
    bboxes = bbox.create_random_quadrats(
        quadrat_size=quadrat_size, n_quadrats=num_simulations
    )

    for bbox in bboxes:
        points_in_bbox = bbox.points_inside(points)
        counts.append(points_in_bbox.count)

    entropy: EntropyResult = calculate_entropy(counts)

    return entropy


def calculate_entropy(
    count_in_quadrats: list[int],
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
    hist, edges = np.histogram(count_in_quadrats, "auto")

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
