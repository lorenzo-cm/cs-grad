import numpy as np
from numpy.typing import NDArray

from ..utils import BoundingBox2d


def quadrat_count_csr_vectorized(
    points: NDArray[np.float64],
    list_bboxes: list[BoundingBox2d],
    signif: float,
    num_simulations: int,
    ) -> NDArray[np.bool_]:
    
    list_passed = []
    for bbox in list_bboxes:
        
        inside_x = (points[:, 0] >= bbox.minx) & (points[:, 0] < bbox.maxx)
        inside_y = (points[:, 1] >= bbox.miny) & (points[:, 1] < bbox.maxy)
        inside_quadrat = inside_x & inside_y

        quadrat_points = points[inside_quadrat]
        
        passed = quadrat_count_monte_carlo_csr(
            points=quadrat_points,
            bbox=bbox,
            signif=signif,
            number_of_quadrats_per_side=5,
            num_simulations=num_simulations,
        )
        
        list_passed.append(passed)
        
    return np.array(list_passed)


def quadrat_count_monte_carlo_csr(
    points: NDArray[np.float64],
    bbox: BoundingBox2d,
    signif,
    num_simulations,
    number_of_quadrats_per_side: int = 5,
) -> bool | None:
    """
    Monte Carlo quadrat count CSR test.
    
    Method Idea:
    - We want to check if the spatial distribution of points is consistent with Complete Spatial Randomness (CSR).
    - In this method, we divide the bounding box into a grid of quadrats 
    - We expect, under CSR, that points are uniformly distributed across these quadrats
    - Hence, the number of points in each quadrat should be TOTAL_POINTS / TOTAL_QUADRATS
    - We then compare the point counts in each quadrat to this expected count using a chi-square statistic.
    - In normal quadrat counts, this is enough, but in Monte Carlo, we go further:
        - We simulate many random point patterns under CSR
        - We compute the chi-square statistic for each simulated pattern
        - We then compare these chi-square stastistics from the random patterns to the original pattern's chi-square statistic
        - If the new chi-squares are often larger than the original, we fail to reject the null hypothesis of CSR
        - Otherwise, if the new chi-squares are rarely larger, we reject the null hypothesis of CSR
        
    Args:
        points: Array of shape (n_points, 2) with point coordinates
        bbox: BoundingBox defining the study area
        signif: Significance level for the hypothesis test (default 0.95)
        number_of_quadrats_per_side: Number of quadrats along each side of the bounding box (default 5)
        num_simulations: Number of Monte Carlo simulations to perform (default 999)
    
    Returns:
        True if the point pattern is consistent with CSR (p-value >= signif), False otherwise
    """
    
    #TODO if is instance of bbox spatio temporal, convert number of quadrats per side to 2 or 3

    # Get the number of points
    points_inside: BoundingBox2d.PointsInside = bbox.points_inside(points)
    
    # If number of pointes is less than 5, we cannot perform the test reliably
    if points_inside.count < 5:
        return True

    # Calculate the expected number of points per quadrat
    expected_count = (points_inside.count / (number_of_quadrats_per_side ** 2))

    # Divide in quadrats
    bboxes = _divide_into_quadrats(bbox, number_of_quadrats_per_side)
    
    # Count points in each quadrat
    observed_counts = []
    for quadrat in bboxes:
        points_in_input: BoundingBox2d.PointsInside = quadrat.points_inside(points)
        observed_counts.append(points_in_input.count)
    
    observed_counts_np = np.array(observed_counts)

    # Chi-square statistic from observed and expected counts
    chi_square_og = np.sum((observed_counts_np - expected_count) ** 2 / expected_count)
    
    # Monte Carlo simulations
    chi_squares_sims = []
    for i in range(num_simulations):
        points_random = bbox.create_random_points(points_inside.count)
        counts_random = []
        for quadrat in bboxes:
            points_in_random: BoundingBox2d.PointsInside = quadrat.points_inside(points_random)
            counts_random.append(points_in_random.count)
        counts_random_np = np.array(counts_random)
        chi_square_sim = np.sum((counts_random_np - expected_count) ** 2 / expected_count)
        chi_squares_sims.append(chi_square_sim)
        
    chi_square_sims_np = np.array(chi_squares_sims)
    
    # Calculate p-value
    p_value = (np.sum(chi_square_sims_np >= chi_square_og) + 1) / (num_simulations + 1)
    
    # Determine if we reject the null hypothesis
    return p_value >= (1 - signif)


def _divide_into_quadrats(
    bbox: BoundingBox2d, number_of_quadrats_per_side: int
) -> list[BoundingBox2d]:
    """
    Divide the bounding box into a grid of quadrats.

    Args:
        bbox: Bounding box
        number_of_quadrats_per_side: Number of quadrats along each side

    Returns:
        List of BoudingBox representing the quadrats
    """
    side = bbox.maxx - bbox.minx  # assuming square bounding box
    quadrat_size: float = side / number_of_quadrats_per_side

    quadrats = []
    for row in range(number_of_quadrats_per_side):
        for col in range(number_of_quadrats_per_side):
            temp_bbox = BoundingBox2d(
                minx=bbox.minx + col * quadrat_size,
                miny=bbox.miny + row * quadrat_size,
                maxx=bbox.minx + (col + 1) * quadrat_size,
                maxy=bbox.miny + (row + 1) * quadrat_size,
                _area=quadrat_size * quadrat_size,
            )
            quadrats.append(temp_bbox)

    return quadrats
