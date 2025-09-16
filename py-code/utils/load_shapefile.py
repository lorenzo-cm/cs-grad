import geopandas as gpd
import numpy as np


def load_shapefile_points(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf[gdf.geometry.notna()]
    
    if len(gdf) == 0:
        raise ValueError("Nenhum registro válido encontrado no shapefile")
    
    point_gdf = gdf[gdf.geometry.geom_type == 'Point']
    coords = np.array([[geom.x, geom.y] for geom in point_gdf.geometry if geom is not None])
    
    return coords
