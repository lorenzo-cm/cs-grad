import numpy as np
from typing import Literal
from numpy.typing import NDArray
from scipy.stats import norm

from .entropy import entropy_score
from ..utils import BoundingBoxBase, scales_permutation


def robustness(
    points: NDArray[np.float64],
    scales: NDArray[np.float64],
    bbox: BoundingBoxBase,
    num_simulations: int = 200,
    num_bootstrap: int = 50,
    binning_method: Literal["auto", "sturges", "fd", "scott", "rice", "sqrt", "stone", "doane", "unique"] = "auto",
    signif: float = 0.99,
    verbose: bool = False,
) -> NDArray[np.float64]:
    """
    Calculate robustness scores for different scales using entropy-based approach.

    Args:
        points: Array of shape (n_points, n_dims)
        scales: List of scales (quadrat sizes) to evaluate
        bbox: Bounding box defining the study area
        num_simulations: Number of random quadrats to generate for each scale
        binning_method: Method for binning the counts
        num_bootstrap: Number of bootstrap samples for statistical testing
        signif: Significance level for statistical testing (default 0.99)
        verbose: Whether to print detailed information

    Returns:
        List of robustness values (relative entropy) for each scale
    """
    robustness_values, iter_product = scales_permutation(scales)

    for idx, scale_combo in enumerate(iter_product):
        relative_entropies = []

        for _ in range(num_bootstrap):
            entropy = entropy_score(
                points=points,
                bbox_sizes=scale_combo,
                bbox=bbox,
                num_simulations=num_simulations,
                binning_method=binning_method,
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
            print(f"Scale: {scale_combo}, Robustness: {robustness_value:.4f}")
            print(f"95% CI: ({ci_lower:.4f}, {ci_upper:.4f})")

        robustness_values[idx] = robustness_value

    return np.array(robustness_values)
