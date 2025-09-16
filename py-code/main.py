from optimal_granularity import get_optimal_granularity
from utils import load_shapefile_points


shapefile_path = "../data/chicago/points/chicago_crimes.shp"

points = load_shapefile_points(shapefile_path)

optimal_granularity = get_optimal_granularity(
    points,
    tradeoff_method="product",
    size_scale=15,
    signif=0.99,
    uniformity_num_random_quadrats_per_scale=200,
    robustness_num_simulations=200,
    robustness_num_bootstrap=100,
    verbose=True,
)

print(f"Optimal granularity: {optimal_granularity}")
