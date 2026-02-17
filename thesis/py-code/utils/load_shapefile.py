import geopandas as gpd
import numpy as np


def load_shapefile_points(
    shapefile_path, epsg=3857
) -> tuple[np.ndarray, gpd.GeoDataFrame]:
    gdf = gpd.read_file(shapefile_path)

    gdf = gdf[gdf.geometry.notna()]
    if gdf.empty:
        raise ValueError("No valid geometries found in the shapefile.")

    gdf = gdf.to_crs(epsg=epsg)

    coords = np.array(gdf.get_coordinates())

    return coords, gdf
