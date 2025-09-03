from optimal_granularity.utils import create_random_points, BoundingBox
from optimal_granularity import get_optimal_granularity


bbox = BoundingBox.from_coords(0, 0, 1000, 1000)
points = create_random_points(bbox, 300)

optimal_granularity = get_optimal_granularity(
    points,
    tradeoff_method="product",
    size_scale=15,
    signif=0.99,
    uniformity_num_random_quadrats_per_scale=400,
    robustness_num_simulations=200,
    robustness_num_bootstrap=50,
    verbose=True,
)

print(f"Optimal granularity: {optimal_granularity}")
