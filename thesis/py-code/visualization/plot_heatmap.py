from dataclasses import dataclass

import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class HeatmapStats:
    mean_all_cells: float
    mean_nonzero_cells: float


def plot_heatmap(gdf_coords, grid_gdf, optimal_scale) -> HeatmapStats:
    joined = gpd.sjoin(gdf_coords, grid_gdf, how="left", predicate="within")
    counts = joined.groupby(["row", "col"]).size().rename("count").reset_index()

    grid_gdf = grid_gdf.merge(counts, on=["row", "col"], how="left")
    grid_gdf["count"] = grid_gdf["count"].fillna(0).astype(int)

    mean_all_cells = grid_gdf["count"].mean()
    nonzero = grid_gdf.loc[grid_gdf["count"] > 0, "count"]
    mean_nonzero_cells = float(nonzero.mean()) if not nonzero.empty else 0.0

    heatmap_matrix = grid_gdf.pivot(index="row", columns="col", values="count").fillna(
        0
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        heatmap_matrix.iloc[::-1],
        cmap="inferno",
        cbar_kws={"label": "Número de pontos"},
        # square=True,
    )

    plt.title(f"Heatmap for cell size = {optimal_scale:.2f}")
    plt.xlabel("Columns (X)")
    plt.ylabel("Lines (Y)")
    plt.tight_layout()
    plt.show()

    return HeatmapStats(
        mean_all_cells=mean_all_cells, mean_nonzero_cells=mean_nonzero_cells
    )
