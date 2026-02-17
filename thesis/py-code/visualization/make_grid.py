import math

import geopandas as gpd
from shapely.geometry import box


def make_aligned_grid(gdf_points: gpd.GeoDataFrame, cell_size: float) -> gpd.GeoDataFrame:
    """
    bounds: (minx, miny, maxx, maxy)
    cell_size: lado da célula (mesma unidade do CRS)
    crs: CRS da grade (igual ao dos pontos)
    """
    bounds = gdf_points.total_bounds
    crs = gdf_points.crs
    
    minx, miny, maxx, maxy = bounds

    # Alinhar os limites a múltiplos inteiros de cell_size
    start_x = math.floor(minx / cell_size) * cell_size
    start_y = math.floor(miny / cell_size) * cell_size
    end_x   = math.ceil (maxx / cell_size) * cell_size
    end_y   = math.ceil (maxy / cell_size) * cell_size

    # Construir as células
    boxes = []
    rows = []
    cols = []

    nx = int(round((end_x - start_x) / cell_size))
    ny = int(round((end_y - start_y) / cell_size))

    for j in range(ny):
        y0 = start_y + j * cell_size
        y1 = y0 + cell_size
        for i in range(nx):
            x0 = start_x + i * cell_size
            x1 = x0 + cell_size
            boxes.append(box(x0, y0, x1, y1))
            rows.append(j)
            cols.append(i)

    grid = gpd.GeoDataFrame(
        {"row": rows, "col": cols},
        geometry=boxes,
        crs=crs
    )
    return grid
