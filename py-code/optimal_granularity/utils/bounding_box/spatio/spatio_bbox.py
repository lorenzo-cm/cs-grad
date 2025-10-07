from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ..bbox_base import BoundingBoxBase


@dataclass
class BoundingBox2d(BoundingBoxBase):
    minx: float
    miny: float
    maxx: float
    maxy: float
    _area: float

    def __str__(self):
        return f"BoundingBox(minx={self.mins[0]}, miny={self.mins[1]}, maxx={self.maxs[0]}, maxy={self.maxs[1]}, area={self._area}, width={self.maxs[0] - self.mins[0]}, height={self.maxs[1] - self.mins[1]})"

    # ------------------------------
    # Properties exigidas pela base
    # ------------------------------

    @property
    def mins(self):
        return (self.minx, self.miny)

    @property
    def maxs(self):
        return (self.maxx, self.maxy)

    @property
    def volume(self) -> float:
        return self._area
    

    # ------------------------------
    # Construtores
    # ------------------------------

    @classmethod
    def from_coords(
        cls,
        mins,
        maxs,
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBox2d":
        """
        Receives mins=(minx,miny), maxs=(maxx,maxy)
        """
        if len(mins) != 2 or len(maxs) != 2:
            raise ValueError("BoundingBox 2D require mins/maxs with size 2.")

        minx, miny = float(mins[0]), float(mins[1])
        maxx, maxy = float(maxs[0]), float(maxs[1])

        minx -= margin
        maxx += margin
        miny -= margin
        maxy += margin

        range_x = maxx - minx
        range_y = maxy - miny

        if range_x < eps or range_y < eps:
            raise ValueError(
                "Bounding box has zero area. Points may be too close or identical."
            )

        area = range_x * range_y
        return cls(minx=minx, miny=miny, maxx=maxx, maxy=maxy, _area=area)

    @classmethod
    def from_points(
        cls, points: np.ndarray, eps: float = 1e-12, margin: float = 1e-6
    ) -> "BoundingBox2d":
        """
        Build axis-aligned bounding box of a 2D point set.
        Returns BoundingBox2d with coordinates and area.

        Args:
            points: Array of shape (n_points, n_dims)
            eps: Minimum dimension to avoid zero-area box
            margin: Small increment added to extremes to avoid boundary conflicts

        Returns:
            BoundingBox2d object with coordinates and area
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

        return cls(minx=minx, miny=miny, maxx=maxx, maxy=maxy, _area=area)

    def points_inside(
        self, points: NDArray[np.float64]
    ) -> BoundingBoxBase.PointsInside:
        """
        Check which points are inside the bounding box.

        Args:
            points: Array of shape (n_points, n_dims)

        Returns:
            PointsInside object with boolean mask and count of points inside
        """
        inside_x = (points[:, 0] >= self.mins[0]) & (points[:, 0] < self.maxs[0])
        inside_y = (points[:, 1] >= self.mins[1]) & (points[:, 1] < self.maxs[1])
        inside_quadrat = inside_x & inside_y

        points_inside = points[inside_quadrat]
        num_points_inside = points_inside.shape[0]

        return self.PointsInside(count=num_points_inside, points=points_inside)

    def create_random_points(self, n_points: int) -> NDArray[np.float64]:
        """
        Generate random points within the bounding box.

        Args:
            bbox: BoundingBox object defining the sampling area
            n_points: Number of points to generate

        Returns:
            Array of shape (n_points, ndims) with x, y coordinates
        """
        # Generate random x coordinates within bbox
        x_coords = np.random.uniform(self.mins[0], self.maxs[0], n_points)

        # Generate random y coordinates within bbox
        y_coords = np.random.uniform(self.mins[1], self.maxs[1], n_points)

        # Stack coordinates into (n_points, 2) array
        points = np.column_stack((x_coords, y_coords))

        return points

    def create_random_quadrats(
        self, quadrat_size: float, n_quadrats: int
    ) -> list["BoundingBox2d"]:
        """
        Generate random quadrat positions for sampling within the bounding box.

        Args:
            quadrat_size: Size of the quadrat (assuming square quadrats)
            bbox: BoundingBox object defining the sampling area
            n_quadrats: Number of random quadrats to generate

        Returns:
            List of BoundingBox objects representing the quadrats
        """
        # Calculate available space for quadrat placement
        # Quadrat must fit entirely within the bounding box
        max_x = self.maxs[0] - quadrat_size
        max_y = self.maxs[1] - quadrat_size

        if max_x < self.mins[0] or max_y < self.mins[1]:
            raise ValueError("Quadrat size is too large for the bounding box")

        # Generate random bottom-left corner positions
        offset_x = np.random.uniform(self.mins[0], max_x, n_quadrats)
        offset_y = np.random.uniform(self.mins[1], max_y, n_quadrats)

        # Create list of BoundingBox objects for each quadrat
        quadrat_bboxes: list[BoundingBox2d] = []
        for i in range(n_quadrats):
            minx = offset_x[i]
            miny = offset_y[i]
            maxx = minx + quadrat_size
            maxy = miny + quadrat_size
            area = quadrat_size * quadrat_size

            quadrat_bbox = BoundingBox2d(
                minx=minx, miny=miny, maxx=maxx, maxy=maxy, _area=area
            )
            quadrat_bboxes.append(quadrat_bbox)

        return quadrat_bboxes

    def gen_scales_from_bbox(self, size: int = 10, as_int: bool = False) -> NDArray:
        """
        Generate a range of scales for spatial analysis based on bounding box.

        Args:
            bbox: BoundingBox object containing the study area bounds
            size: Number of scales to generate
            as_int: If True, round scales to integers; if False, keep as floats

        Returns:
            Array of scales ranging from start to stop values

        Notes:
            - stop = 0.5 * min_side: Maximum scale at 50% of study min side to ensure coverage
            - start = 0.05 * stop: Minimum scale at 5% of maximum to avoid overly fine granularity
        """
        # 1000x1000 = 1_000_000
        # stop = 1000 * 0.35 = 350
        # start = 350 * 0.1 = 35

        min_side = min(self.maxs[0] - self.mins[0], self.maxs[1] - self.mins[1])
        stop = 0.5 * min_side
        start = 0.025 * stop
        scales = np.linspace(start, stop, size)

        if as_int:
            scales = np.round(scales).astype(int)
            scales = np.unique(scales)

        return scales

    def divide_into_quadrats(self, number_of_quadrats_per_side: int) -> list["BoundingBox2d"]:
        """
        Divide the 2D bounding box into a regular grid of quadrats.
        
        Args:
            number_of_quadrats_per_side: Number of quadrats along each side
            
        Returns:
            List of BoundingBox2d objects representing the quadrats
        """
        side = self.maxs[0] - self.mins[0]  # assuming square bounding box
        quadrat_size: float = side / number_of_quadrats_per_side

        quadrats = []
        for row in range(number_of_quadrats_per_side):
            for col in range(number_of_quadrats_per_side):
                mins = (
                    self.mins[0] + col * quadrat_size,
                    self.mins[1] + row * quadrat_size,
                )
                maxs = (
                    self.mins[0] + (col + 1) * quadrat_size,
                    self.mins[1] + (row + 1) * quadrat_size,
                )
                temp_bbox = self.from_coords(mins, maxs)
                quadrats.append(temp_bbox)

        return quadrats
