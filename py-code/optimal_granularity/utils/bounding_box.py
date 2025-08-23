from dataclasses import dataclass
import numpy as np


@dataclass
class BoundingSquare:
    minx: float
    miny: float
    maxx: float
    maxy: float
    area: float


def bounding_square_from_points(
    points: np.ndarray, eps: float = 1e-12, margin: float = 1e-6
) -> BoundingSquare:
    """
    Build axis-aligned bounding box of a 2D point set.
    Returns BoundingSquare with coordinates and area.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        eps: Minimum dimension to avoid zero-area box
        margin: Small increment added to extremes to avoid boundary conflicts

    Returns:
        BoundingSquare object with coordinates and area
    """
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be array (n,2).")
    if points.shape[0] < 2:
        raise ValueError("Need at least 2 points.")

    minx = float(points[:, 0].min()) - margin
    maxx = float(points[:, 0].max()) + margin
    miny = float(points[:, 1].min()) - margin
    maxy = float(points[:, 1].max()) + margin

    range_x = maxx - minx
    range_y = maxy - miny

    if range_x < eps or range_y < eps:
        raise ValueError(
            "Bounding box has zero area. Points may be too close or identical."
        )

    area = range_x * range_y

    return BoundingSquare(minx=minx, miny=miny, maxx=maxx, maxy=maxy, area=area)
