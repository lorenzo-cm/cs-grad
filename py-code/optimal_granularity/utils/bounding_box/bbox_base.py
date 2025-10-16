from abc import ABC, abstractmethod
from typing import Sequence, Self
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


class BoundingBoxBase(ABC):
    _maxs: Sequence[float]
    _mins: Sequence[float]
    _volume: float

    # ------------------------------
    # Properties
    # ------------------------------

    @property
    @abstractmethod
    def mins(self) -> Sequence[float]:
        """
        Minimum values per axis (len == 2 in 2D, len == 3 in 3D).
        Equivalent to (minx, miny) or (minx, miny, minz) in 2D/3D.
        """

    @property
    @abstractmethod
    def maxs(self) -> Sequence[float]:
        """
        Maximum values per axis (same dimension as `mins`).
        Equivalent to (maxx, maxy) or (maxx, maxy, maxz) in 2D/3D.
        """

    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Hypervolume measure:
          - 2D: area
          - 3D: volume
        """

    @property
    def ndim(self) -> int:
        """Dimensionality (derived)."""
        return len(self.mins)

    # ------------------------------
    # Factory methods
    # ------------------------------

    @classmethod
    @abstractmethod
    def from_coords(
        cls,
        mins: Sequence[float],
        maxs: Sequence[float],
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBoxBase":
        """
        Create the bounding box from explicit coordinates.

        It automatically return the appropriate subclass based on the dimensionality of mins/maxs.
        """
        ndim = len(mins)

        if ndim == 2:
            from .spatio import BoundingBox2d

            return BoundingBox2d.from_coords(mins, maxs, eps=eps, margin=margin)

        elif ndim == 3:
            from .spatiotemporal import BoundingBoxSpatioTemporal

            return BoundingBoxSpatioTemporal.from_coords(
                mins, maxs, eps=eps, margin=margin
            )

        else:
            raise ValueError(
                f"Unsupported dimensionality: {ndim}. Only 2D and 3D are supported."
            )

    @classmethod
    @abstractmethod
    def from_points(
        cls,
        points: np.ndarray,
        eps: float = 1e-12,
        margin: float = 1e-6,
    ) -> "BoundingBoxBase":
        """
        Create the bounding box from a set of points in nD.

        Points must be of shape (n_points, ndim)

        It automatically return the appropriate subclass based on the dimensionality of mins/maxs.
        """
        ndim = points.shape[1]

        if ndim == 2:
            from .spatio import BoundingBox2d

            return BoundingBox2d.from_points(points, eps=eps, margin=margin)

        elif ndim == 3:
            from .spatiotemporal import BoundingBoxSpatioTemporal

            return BoundingBoxSpatioTemporal.from_points(points, eps=eps, margin=margin)

        else:
            raise ValueError(
                f"Unsupported dimensionality: {ndim}. Only 2D and 3D are supported."
            )

    # ------------------------------
    # Utils
    # ------------------------------

    @dataclass
    class PointsInside:
        count: int
        points: NDArray[np.float64]

    @abstractmethod
    def points_inside(self, points: NDArray[np.float64]) -> PointsInside:
        """Return the points that are inside the bounding box."""

    @abstractmethod
    def create_random_points(self, n_points: int) -> NDArray[np.float64]:
        """Generate random points inside the bounding box."""

    @abstractmethod
    def create_random_bboxes(
        self,
        bbox_scales: Sequence[float],
        n_quadrats: int,
    ) -> list[Self]:
        """
        Generate random sub-bounding boxes inside the bounding box.
        
        It accept multiple scales for the quadrats, assuming the first dimension is spatial.
        """

    @abstractmethod
    def gen_scales_from_bbox(self, size: int = 10) -> NDArray:
        """
        Generate spatial analysis scales from the bounding box dimensions.

        Since the scales can difer in each dimension, the return array can be multidimensional:
        - 2D: (1, n_scales) with (scale_geo,)
        - 3D: (2, n_scales) with (scale_geo, scale_time)
        """

    @abstractmethod
    def divide_into_quadrats(self, number_of_quadrats_per_side: int) -> list[Self]:
        """
        Divide the bounding box into a regular grid of bboxes.
        It preserves the dimensionality of the original bbox.

        Args:
            number_of_quadrats_per_side: Number of bboxes along each side

        Returns:
            List of BoundingBox objects representing the quadrats
        """
