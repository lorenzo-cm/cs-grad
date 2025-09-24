import matplotlib.pyplot as plt


def plot_grid(gdf_coords, grid_gdf, optimal_scale):
    fig, ax = plt.subplots(figsize=(8, 8))

    grid_gdf.boundary.plot(ax=ax, linewidth=0.5)

    gdf_coords.plot(ax=ax, markersize=2)

    ax.set_title(f"Points and grid for cell size = {optimal_scale:.2f}")
    ax.set_aspect("auto")
    ax.set_xlabel("X (meters in EPSG:3857)")
    ax.set_ylabel("Y (meters in EPSG:3857)")
    plt.tight_layout()
    plt.show()
