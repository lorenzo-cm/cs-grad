from dataclasses import dataclass
from typing import Sequence

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
        raise NotImplementedError("Not implemented yet.")

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
            points: array (n, 3) with columns [x, y, t]
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
        Return points inside box (x in [minx,maxx), y in [miny,maxy), t in [mint,maxt))
        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points must be array (n, 3) with [x, y, t].")

        inside_x = (points[:, 0] >= self.minx) & (points[:, 0] < self.maxx)
        inside_y = (points[:, 1] >= self.miny) & (points[:, 1] < self.maxy)
        inside_t = (points[:, 2] >= self.mint) & (points[:, 2] < self.maxt)

        mask = inside_x & inside_y & inside_t
        pts_in = points[mask]
        return self.PointsInside(count=pts_in.shape[0], points=pts_in)

    def create_random_points(self, n_points: int) -> NDArray[np.float64]:
        """
        Generate uniform points (x, y, t) inside the box.
        Returns array (n_points, 3).
        """
        x = np.random.uniform(self.minx, self.maxx, n_points)
        y = np.random.uniform(self.miny, self.maxy, n_points)
        t = np.random.uniform(self.mint, self.maxt, n_points)
        return np.column_stack((x, y, t)).astype(np.float64)

    def create_random_quadrats(
        self,
        quadrat_size: float,
        n_quadrats: int,
    ) -> list["BoundingBoxSpatioTemporal"]:
        """
        Generate cubic sub-boxes (voxels) with edge `quadrat_size` inside AABB (x, y, t).

        Note: To match 2D signature, the same `quadrat_size`
        is used for all 3 dimensions (x, y, t). For different sizes,
        a variant method could be added with (sx, sy, st).
        """
        max_x = self.maxx - quadrat_size
        max_y = self.maxy - quadrat_size
        max_t = self.maxt - quadrat_size

        if (max_x < self.minx) or (max_y < self.miny) or (max_t < self.mint):
            raise ValueError("Quadrat size too large for 3D bounding box.")

        off_x = np.random.uniform(self.minx, max_x, n_quadrats)
        off_y = np.random.uniform(self.miny, max_y, n_quadrats)
        off_t = np.random.uniform(self.mint, max_t, n_quadrats)

        voxels: list[BoundingBoxSpatioTemporal] = []
        for i in range(n_quadrats):
            minx = float(off_x[i])
            miny = float(off_y[i])
            mint = float(off_t[i])

            maxx = minx + quadrat_size
            maxy = miny + quadrat_size
            maxt = mint + quadrat_size

            vol = quadrat_size * quadrat_size * quadrat_size

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

    def gen_scales_from_bbox(self, size: int = 10, as_int: bool = False) -> NDArray:
        """
        Generate analysis scales based ONLY on spatial dimensions (x,y),
        same as 2D. Useful when grid is spatial and time is a separate window.

        stop = 0.5 * min_side
        start = 0.025 * stop
        """
        side_x = self.maxx - self.minx
        side_y = self.maxy - self.miny
        min_side = min(side_x, side_y)

        stop = 0.5 * min_side
        start = 0.025 * stop
        scales = np.linspace(start, stop, size)

        if as_int:
            scales = np.round(scales).astype(int)
            scales = np.unique(scales)

        return scales
