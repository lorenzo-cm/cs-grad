import numpy as np
from attr import dataclass
from numpy.typing import NDArray

from .bounding_box import BoundingBox


@dataclass
class PointsInside:
    count: int
    points: NDArray[np.float64]


def points_in_quadrat(points: NDArray[np.float64], bbox: BoundingBox) -> PointsInside:
    """
    Count how many points are inside a given square quadrat.

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_position: BoundingBox class

    Returns:
        PointsInside dataclass with number of points and their coordinates
    """
    inside_x = (points[:, 0] >= bbox.minx) & (points[:, 0] < bbox.maxx)
    inside_y = (points[:, 1] >= bbox.miny) & (points[:, 1] < bbox.maxy)
    inside_quadrat = inside_x & inside_y

    points_inside = points[inside_quadrat]
    num_points_inside = points_inside.shape[0]

    return PointsInside(count=num_points_inside, points=points_inside)


def points_in_quadrat_vectorized(
    points: NDArray[np.float64], list_bboxes: list[BoundingBox]
) -> list[PointsInside]:
    """
    Count points in multiple quadrats at once (vectorized version).

    Args:
        points: Array of shape (n_points, 2) with point coordinates
        quadrat_positions: Array of shape (n_quadrats, 2) with bottom-left corners
        quadrat_size: Size of the square quadrats

    Returns:
        List of PointsInside dataclasses for each quadrat
    """
    return_list = []

    for bbox in list_bboxes:
        points_inside = points_in_quadrat(points, bbox)
        return_list.append(points_inside)

    return return_list
