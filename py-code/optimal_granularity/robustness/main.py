import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from .entropy import entropy_score
from ..utils import BoundingBox2d


def robustness(
    points: NDArray[np.float64],
    scales: NDArray[np.float64],
    bbox: BoundingBox2d,
    num_simulations: int = 200,
    num_bootstrap: int = 50,
    signif: float = 0.99,
    verbose: bool = False,
) -> NDArray[np.float64]:
    """
    Calculate robustness scores for different scales using entropy-based approach.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        scales: List of scales (quadrat sizes) to evaluate
        bbox: Bounding box defining the study area
        num_simulations: Number of random quadrats to generate for each scale
        signif: Significance level for statistical testing (default 0.99)
        verbose: Whether to print detailed information

    Returns:
        List of robustness values (relative entropy) for each scale
    """
    robustness_values = []

    for scale in scales:
        relative_entropies = []

        for _ in range(num_bootstrap):
            entropy = entropy_score(
                points=points,
                quadrat_size=scale,
                bbox=bbox,
                num_simulations=num_simulations,
            )
            relative_entropies.append(entropy.relative_entropy)

        # Calculate statistics for significance assessment
        relative_entropies_np = np.array(relative_entropies)
        mean_entropy = np.mean(relative_entropies_np)
        std_entropy = np.std(relative_entropies_np)

        # Calculate confidence interval based on significance level
        alpha = 1 - signif
        z_score = norm.ppf(1 - alpha / 2)

        margin_error = z_score * (std_entropy / np.sqrt(num_bootstrap))
        ci_lower = mean_entropy - margin_error
        ci_upper = mean_entropy + margin_error

        # Use mean entropy as the robustness value
        robustness_value = mean_entropy

        if verbose:
            print(
                f"Scale: {scale}, Robustness: {robustness_value:.4f}"
                f"95% CI: ({ci_lower:.4f}, {ci_upper:.4f})"
            )

        robustness_values.append(robustness_value)

    return np.array(robustness_values)
