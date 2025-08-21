from dataclasses import dataclass
import numpy as np

@dataclass
class BoundingSquare:
    minx: float
    miny: float
    maxx: float
    maxy: float
    area: float

def bounding_square_from_points(points: np.ndarray, eps: float = 1e-12) -> BoundingSquare:
    """
    Build axis-aligned bounding square of a 2D point set.
    Returns BoundingSquare with coordinates and area.
    """
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be array (n,2).")
    if points.shape[0] < 2:
        raise ValueError("Need at least 2 points.")

    minx = float(points[:, 0].min())
    maxx = float(points[:, 0].max())
    miny = float(points[:, 1].min())
    maxy = float(points[:, 1].max())

    range_x = maxx - minx
    range_y = maxy - miny
    side = max(range_x, range_y)
    if side < eps:
        side = eps  # avoid zero-area square

    # Expand the smaller dimension so the box is square
    if range_x < side:
        maxx = minx + side
    if range_y < side:
        maxy = miny + side

    area = side * side

    return BoundingSquare(minx=minx, miny=miny, maxx=maxx, maxy=maxy, area=area)
