from dataclasses import dataclass
from typing import Literal, Optional, Sequence

import numpy as np
from numpy.typing import NDArray

from ..bbox_base import BoundingBoxBase


@dataclass
class BoundingBoxSpatioTemporal(BoundingBoxBase):
    minx: float
    miny: float
    maxx: float
    maxy: float
    mint: float
    maxt: float
    _volume: float

    def __str__(self):
        return f"BoundingBoxSpatioTemporal(minx={self.mins[0]}, miny={self.mins[1]}, mint={self.mins[2]}, maxx={self.maxs[0]}, maxy={self.maxs[1]}, maxt={self.maxs[2]}, volume={self.volume})"

    # ------------------------------
    # Properties
    # ------------------------------

    @property
    def mins(self) -> Sequence[float]:
        return self.minx, self.miny, self.mint

    @property
    def maxs(self) -> Sequence[float]:
        return self.maxx, self.maxy, self.maxt

    @property
    def volume(self) -> float:
        return self._volume

    # ------------------------------
    # Constructors
    # ------------------------------

    @classmethod
    def from_coords(
        cls,
        mins: Sequence[float],
        maxs: Sequence[float],
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBoxSpatioTemporal":
        """
        Create spatiotemporal bounding box from explicit coordinates.

        Args:
            mins: Sequence of (minx, miny, mint) coordinates
            maxs: Sequence of (maxx, maxy, maxt) coordinates
            eps: Minimum dimension to avoid zero-volume box
            margin: Small increment added to extremes to avoid boundary conflicts

        Returns:
            BoundingBoxSpatioTemporal object with coordinates and volume
        """
        if len(mins) != 3 or len(maxs) != 3:
            raise ValueError(
                "BoundingBox spatiotemporal requires mins/maxs with size 3."
            )

        minx, miny, mint = float(mins[0]), float(mins[1]), float(mins[2])
        maxx, maxy, maxt = float(maxs[0]), float(maxs[1]), float(maxs[2])

        minx -= margin
        maxx += margin
        miny -= margin
        maxy += margin
        mint -= margin
        maxt += margin

        range_x = maxx - minx
        range_y = maxy - miny
        range_t = maxt - mint

        if range_x < eps or range_y < eps or range_t < eps:
            raise ValueError(
                "Degenerate spatiotemporal bounding box. Points too close/equal."
            )

        volume = range_x * range_y * range_t

        return cls(
            minx=minx,
            miny=miny,
            maxx=maxx,
            maxy=maxy,
            mint=mint,
            maxt=maxt,
            _volume=volume,
        )

    @classmethod
    def from_points(
        cls,
        points: np.ndarray,
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBoxSpatioTemporal":
        """
        Build a 3D AABB (x, y, t) from a set of points.

        Args:
            points: Array of shape (n_points, n_dims) where n_dims=3 for (x,y,t)
        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points must be array (n, 3) with [x, y, t].")
        if points.shape[0] < 2:
            raise ValueError("At least 2 points are required.")

        minx = float(points[:, 0].min()) - margin
        maxx = float(points[:, 0].max()) + margin
        miny = float(points[:, 1].min()) - margin
        maxy = float(points[:, 1].max()) + margin
        mint = float(points[:, 2].min()) - margin
        maxt = float(points[:, 2].max()) + margin

        range_x = maxx - minx
        range_y = maxy - miny
        range_t = maxt - mint

        if range_x < eps or range_y < eps or range_t < eps:
            raise ValueError(
                "Degenerate spatiotemporal bounding box. Points too close/equal."
            )

        volume = range_x * range_y * range_t

        return cls(
            minx=minx,
            miny=miny,
            maxx=maxx,
            maxy=maxy,
            mint=mint,
            maxt=maxt,
            _volume=volume,
        )

    # ------------------------------
    # Utils
    # ------------------------------

    def points_inside(
        self, points: NDArray[np.float64]
    ) -> BoundingBoxBase.PointsInside:
        """
        Return points inside spatiotemporal box (x in [minx,maxx), y in [miny,maxy), t in [mint,maxt)).

        Args:
            points: Array of shape (n_points, n_dims) with shapefile point coordinates where:
                   - n_points: number of geographic features from shapefile
                   - n_dims: spatiotemporal dimensions (3 for x,y,t coordinates)
        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points must be array (n, 3) with [x, y, t].")

        inside_x = (points[:, 0] >= self.mins[0]) & (points[:, 0] < self.maxs[0])
        inside_y = (points[:, 1] >= self.mins[1]) & (points[:, 1] < self.maxs[1])
        inside_t = (points[:, 2] >= self.mins[2]) & (points[:, 2] < self.maxs[2])

        mask = inside_x & inside_y & inside_t
        pts_in = points[mask]
        return self.PointsInside(count=pts_in.shape[0], points=pts_in)

    def create_random_points(self, n_points: int) -> NDArray[np.float64]:
        """
        Generate uniform points (x, y, t) inside the box.
        Returns array (n_points, 3).
        """
        x = np.random.uniform(self.mins[0], self.maxs[0], n_points)
        y = np.random.uniform(self.mins[1], self.maxs[1], n_points)
        t = np.random.uniform(self.mins[2], self.maxs[2], n_points)
        return np.column_stack((x, y, t)).astype(np.float64)

    def create_random_bboxes(
        self,
        bbox_scales: Sequence[float],
        n_quadrats: int,
    ) -> list["BoundingBoxSpatioTemporal"]:
        """
        Generate random spatiotemporal boxes (voxels) within the bounding box.
        
        Scales: bbox_scales = [spatial_scale, temporal_scale]
        """
        if len(bbox_scales) != 2:
            raise ValueError("For spatiotemporal bbox: bbox_scales must be a sequence of two floats [spatial, temporal].")
        
        max_x = self.maxs[0] - bbox_scales[0]
        max_y = self.maxs[1] - bbox_scales[0]
        max_t = self.maxs[2] - bbox_scales[1]

        if (max_x < self.mins[0]) or (max_y < self.mins[1]) or (max_t < self.mins[2]):
            raise ValueError("Quadrat size too large for 3D bounding box.")

        off_x = np.random.uniform(self.mins[0], max_x, n_quadrats)
        off_y = np.random.uniform(self.mins[1], max_y, n_quadrats)
        off_t = np.random.uniform(self.mins[2], max_t, n_quadrats)

        voxels: list[BoundingBoxSpatioTemporal] = []
        for i in range(n_quadrats):
            minx = float(off_x[i])
            miny = float(off_y[i])
            mint = float(off_t[i])

            maxx = minx + bbox_scales[0]
            maxy = miny + bbox_scales[0]
            maxt = mint + bbox_scales[1]

            vol = bbox_scales[0] * bbox_scales[0] * bbox_scales[1]

            voxel = BoundingBoxSpatioTemporal(
                minx=minx,
                miny=miny,
                maxx=maxx,
                maxy=maxy,
                mint=mint,
                maxt=maxt,
                _volume=vol,
            )
            voxels.append(voxel)

        return voxels

    def gen_scales_from_bbox(self,
                             size: int = 10,
                             num_points: Optional[int] = None,
                             min_points_per_square=1,
                             max_percentage_points_per_square=20,
                             method: Literal["side", "density"] = "density") -> NDArray:
        """
        Generate analysis scales based ONLY on spatial dimensions (x,y),
        same as 2D. Useful when grid is spatial and time is a separate window.
        """
        if method == "density":
            if num_points is None or num_points <= 0:
                raise ValueError("num_points must be greater than 0 when method is 'density'")
            area = (self.maxs[0] - self.mins[0]) * (self.maxs[1] - self.mins[1])
            points_density = num_points / area
            inv_points_density = 1 / points_density
            s_min = np.sqrt(min_points_per_square * inv_points_density)
            max_points = num_points * max_percentage_points_per_square / 100
            s_max = np.sqrt(max_points * inv_points_density)
            geo_scales = np.linspace(s_min, s_max, size)
            
        elif method == "side":
            min_side = min(self.maxs[0] - self.mins[0], self.maxs[1] - self.mins[1])
            stop = 0.5 * min_side
            start = 0.025 * stop
            geo_scales = np.linspace(start, stop, size)

        # max_t - min_t = D_t
        # time_scale[0] = Division of D_t in two parts
        # time_scale[1] = Division of D_t in three parts
        # ...
        time_scales = [(self.maxs[2] - self.mins[2]) / (i + 2) for i in np.arange(size)]

        scales = np.vstack((geo_scales, time_scales))

        return scales

    def divide_into_quadrats(
        self, number_of_quadrats_per_side: int
    ) -> list["BoundingBoxSpatioTemporal"]:
        """
        Divide the 3D spatiotemporal bounding box into a regular grid of voxels.

        Creates ``number_of_quadrats_per_side``^3 boxes. For example, if
        ``number_of_quadrats_per_side=3``, it creates 3x3x3 = 27 boxes that
        completely fill the original bounding box. Voxels are axis-aligned
        rectangular cuboids; they are not forced to be cubes
        (x, y are in the same scale but t is nopt).

        Args:
            number_of_quadrats_per_side: Number of quadrats along each dimension (x, y, t). Must be >= 1.

        Returns:
            List of BoundingBoxSpatioTemporal objects representing the voxels.
        """
        if number_of_quadrats_per_side < 1:
            raise ValueError("number_of_quadrats_per_side must be >= 1")

        # Use linspace to avoid floating accumulation error and ensure exact coverage.
        xs = np.linspace(self.mins[0], self.maxs[0], number_of_quadrats_per_side + 1)
        ys = np.linspace(self.mins[1], self.maxs[1], number_of_quadrats_per_side + 1)
        ts = np.linspace(self.mins[2], self.maxs[2], number_of_quadrats_per_side + 1)

        bboxes: list[BoundingBoxSpatioTemporal] = []
        for t_idx in range(number_of_quadrats_per_side):
            for y_idx in range(number_of_quadrats_per_side):
                for x_idx in range(number_of_quadrats_per_side):
                    mins = (float(xs[x_idx]), float(ys[y_idx]), float(ts[t_idx]))
                    maxs = (
                        float(xs[x_idx + 1]),
                        float(ys[y_idx + 1]),
                        float(ts[t_idx + 1]),
                    )
                    temp_bbox = self.from_coords(mins, maxs, margin=0.0)
                    bboxes.append(temp_bbox)

        return bboxes
